#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Cell Tower Data Collector for CraxCore Location Tracker
------------------------------------------------------
This script helps collect real cell tower data from a rooted device
"""

import os
import sys
import json
import subprocess
import re
import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()

# Define file paths
OUTPUT_FILE = "real_cell_towers.json"
CELL_TOWERS_FILE = "bd_cell_towers.json"

def check_root_access():
    """Check if the device has root access"""
    try:
        result = subprocess.run(['su', '-c', 'id'], 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE, 
                               text=True,
                               timeout=3)
        return result.returncode == 0 and 'uid=0' in result.stdout
    except:
        return False

def check_tools():
    """Check if required tools are installed"""
    tools = {
        'busybox': False,
        'termux-location': False
    }
    
    for tool in tools:
        try:
            subprocess.run(['which', tool], 
                          stdout=subprocess.PIPE, 
                          stderr=subprocess.PIPE, 
                          check=True)
            tools[tool] = True
        except:
            pass
    
    return tools

def get_phone_location():
    """Get phone location using Termux API"""
    try:
        result = subprocess.run(['termux-location'], 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE, 
                               text=True,
                               timeout=10)
        
        if result.returncode == 0:
            location_data = json.loads(result.stdout)
            return {
                'latitude': location_data.get('latitude'),
                'longitude': location_data.get('longitude'),
                'accuracy': location_data.get('accuracy'),
                'timestamp': location_data.get('timestamp')
            }
    except Exception as e:
        console.print(f"[bold red]Error getting location: {str(e)}[/bold red]")
    
    return None

def get_cell_info_android():
    """Get cell tower information from Android using root"""
    cell_info = {}
    
    try:
        # Try service call phone method
        result = subprocess.run(['su', '-c', 'service call phone 27'], 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE, 
                               text=True)
        
        if result.returncode == 0:
            # Parse service call output
            output = result.stdout
            
            # Example parsing (actual parsing would depend on device and Android version)
            matches = re.findall(r"([0-9a-f]{8})", output)
            if len(matches) >= 4:
                # This is a simplified example, actual parsing is more complex
                cell_info = {
                    'mcc': int(matches[0], 16) & 0xFFFF,
                    'mnc': int(matches[1], 16) & 0xFFFF,
                    'lac': int(matches[2], 16) & 0xFFFF,
                    'cid': int(matches[3], 16) & 0xFFFFFF
                }
                return cell_info
        
        # Alternative method - read from /dev files
        result = subprocess.run(['su', '-c', 'cat /dev/radio/atcmd'],
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE)
        
        # Another alternative - dumpsys telephony
        result = subprocess.run(['su', '-c', 'dumpsys telephony.registry'],
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE, 
                               text=True)
        
        if result.returncode == 0:
            output = result.stdout
            
            # Parse MCC and MNC
            mcc_mnc = re.search(r"mNetworkInfo.*mcc (\d+).*mnc (\d+)", output)
            if mcc_mnc:
                cell_info['mcc'] = int(mcc_mnc.group(1))
                cell_info['mnc'] = int(mcc_mnc.group(2))
            
            # Parse LAC and CID
            lac_cid = re.search(r"mCellLocation.*\[(\d+),(\d+)]", output)
            if lac_cid:
                cell_info['lac'] = int(lac_cid.group(1))
                cell_info['cid'] = int(lac_cid.group(2))
            
            if 'mcc' in cell_info and 'mnc' in cell_info and 'lac' in cell_info and 'cid' in cell_info:
                return cell_info
        
        # If still no data, try AT commands if available
        result = subprocess.run(['su', '-c', 'echo "AT+CREG?" > /dev/smd0'],
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE)
        
    except Exception as e:
        console.print(f"[bold red]Error getting cell info: {str(e)}[/bold red]")
    
    return None

def get_area_name(lat, lon):
    """Get area name from coordinates"""
    try:
        import requests
        from geopy.geocoders import Nominatim
        
        # Try using Nominatim (OpenStreetMap)
        geolocator = Nominatim(user_agent="cell_tower_collector")
        location = geolocator.reverse(f"{lat}, {lon}", language="en")
        
        if location and location.address:
            address_parts = location.address.split(', ')
            
            # Extract city and area
            if len(address_parts) >= 3:
                area = f"{address_parts[1]}, {address_parts[0]}"
                return area
            else:
                return address_parts[0]
        
    except Exception as e:
        console.print(f"[bold yellow]Error getting area name: {str(e)}[/bold yellow]")
    
    return "Unknown Area"

def save_cell_tower(tower_data):
    """Save cell tower data to JSON file"""
    towers = []
    
    # Load existing towers if file exists
    if os.path.exists(OUTPUT_FILE):
        try:
            with open(OUTPUT_FILE, 'r') as f:
                data = json.load(f)
                towers = data.get('towers', [])
        except:
            pass
    
    # Check if tower already exists
    tower_exists = False
    for tower in towers:
        if (tower['mcc'] == tower_data['mcc'] and 
            tower['mnc'] == tower_data['mnc'] and 
            tower['lac'] == tower_data['lac'] and 
            tower['cid'] == tower_data['cid']):
            tower_exists = True
            break
    
    # Add tower if it doesn't exist
    if not tower_exists:
        towers.append(tower_data)
        
        # Save to file
        data = {
            'version': '1.0',
            'description': 'Real cell tower data collected from device',
            'towers': towers
        }
        
        with open(OUTPUT_FILE, 'w') as f:
            json.dump(data, f, indent=4)
        
        return True
    
    return False

def add_to_main_database():
    """Add collected towers to main database"""
    if not os.path.exists(OUTPUT_FILE):
        console.print("[bold yellow]No collected tower data found![/bold yellow]")
        return False
    
    # Load collected towers
    try:
        with open(OUTPUT_FILE, 'r') as f:
            collected_data = json.load(f)
            collected_towers = collected_data.get('towers', [])
            
        if not collected_towers:
            console.print("[bold yellow]No towers collected yet![/bold yellow]")
            return False
        
        # Load main database
        if os.path.exists(CELL_TOWERS_FILE):
            with open(CELL_TOWERS_FILE, 'r') as f:
                main_data = json.load(f)
                main_towers = main_data.get('towers', [])
        else:
            main_data = {
                'version': '1.0',
                'description': 'Bangladesh cell towers database',
                'towers': [],
                'operators': {
                    '1': {
                        'name': 'GrameenPhone',
                        'prefixes': ['017', '013']
                    },
                    '2': {
                        'name': 'Robi',
                        'prefixes': ['018', '016']
                    },
                    '3': {
                        'name': 'Banglalink',
                        'prefixes': ['019', '014']
                    },
                    '4': {
                        'name': 'Teletalk',
                        'prefixes': ['015', '011']
                    }
                }
            }
            main_towers = []
        
        # Check for duplicate towers and add new ones
        added_count = 0
        for collected_tower in collected_towers:
            tower_exists = False
            for main_tower in main_towers:
                if (main_tower['mcc'] == collected_tower['mcc'] and 
                    main_tower['mnc'] == collected_tower['mnc'] and 
                    main_tower['lac'] == collected_tower['lac'] and 
                    main_tower['cid'] == collected_tower['cid']):
                    tower_exists = True
                    break
            
            if not tower_exists:
                main_towers.append(collected_tower)
                added_count += 1
        
        if added_count > 0:
            # Save updated main database
            main_data['towers'] = main_towers
            
            with open(CELL_TOWERS_FILE, 'w') as f:
                json.dump(main_data, f, indent=4)
            
            console.print(f"[bold green]Added {added_count} new towers to main database![/bold green]")
            return True
        else:
            console.print("[bold yellow]No new towers to add to main database![/bold yellow]")
            return False
    
    except Exception as e:
        console.print(f"[bold red]Error adding to main database: {str(e)}[/bold red]")
        return False

def main():
    """Main function"""
    os.system('clear')
    
    console.print(Panel.fit("[bold blue]CraxCore Location Tracker - Tower Data Collector[/bold blue]", 
                           border_style="green"))
    
    # Check if device is rooted
    is_rooted = check_root_access()
    
    if not is_rooted:
        console.print("[bold red]⚠️ Warning: Device is not rooted or root access denied![/bold red]")
        console.print("[bold yellow]Some features may not work without root access.[/bold yellow]")
    else:
        console.print("[bold green]✅ Root access confirmed.[/bold green]")
    
    # Check for required tools
    tools = check_tools()
    tools_status = Table(title="Required Tools", show_header=True)
    
    tools_status.add_column("Tool", style="cyan")
    tools_status.add_column("Status", style="green")
    
    for tool, installed in tools.items():
        status = "[green]Installed[/green]" if installed else "[red]Not installed[/red]"
        tools_status.add_row(tool, status)
    
    console.print(tools_status)
    
    # Menu
    while True:
        console.print("\n[bold yellow]===== 📱 Tower Data Collector =====\n[/bold yellow]")
        console.print("[1] Collect Current Tower Data")
        console.print("[2] View Collected Towers")
        console.print("[3] Add Collected Towers to Main Database")
        console.print("[4] Manual Tower Entry")
        console.print("[5] Exit")
        
        choice = input("\nEnter your choice (1-5): ")
        
        if choice == "1":
            console.print("\n[bold]🔍 Collecting tower data...[/bold]")
            
            # Get location
            console.print("Getting device location...")
            location = get_phone_location()
            
            if not location:
                console.print("[bold red]Failed to get location. Using approximate coordinates.[/bold red]")
                location = {
                    'latitude': 23.8103,  # Default to Dhaka
                    'longitude': 90.4125
                }
            else:
                console.print(f"[bold green]Location: {location['latitude']}, {location['longitude']}[/bold green]")
            
            # Get cell info
            console.print("Getting cell tower information...")
            cell_info = get_cell_info_android()
            
            if not cell_info:
                console.print("[bold red]Failed to get cell tower information.[/bold red]")
                console.print("[bold yellow]Please enter manually using option 4.[/bold yellow]")
                input("\nPress Enter to continue...")
                continue
            
            console.print(f"[bold green]Cell Info: MCC={cell_info['mcc']}, MNC={cell_info['mnc']}, LAC={cell_info['lac']}, CID={cell_info['cid']}[/bold green]")
            
            # Get area name
            console.print("Getting area name...")
            area = get_area_name(location['latitude'], location['longitude'])
            
            # Combine data
            tower_data = {
                'mcc': cell_info['mcc'],
                'mnc': cell_info['mnc'],
                'lac': cell_info['lac'],
                'cid': cell_info['cid'],
                'lat': location['latitude'],
                'lon': location['longitude'],
                'area': area,
                'collected_time': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Save data
            if save_cell_tower(tower_data):
                console.print("[bold green]✅ Tower data saved successfully![/bold green]")
            else:
                console.print("[bold yellow]Tower already exists in the database.[/bold yellow]")
            
            input("\nPress Enter to continue...")
            
        elif choice == "2":
            if not os.path.exists(OUTPUT_FILE):
                console.print("[bold yellow]No collected tower data found![/bold yellow]")
                input("\nPress Enter to continue...")
                continue
            
            try:
                with open(OUTPUT_FILE, 'r') as f:
                    data = json.load(f)
                    towers = data.get('towers', [])
                
                if not towers:
                    console.print("[bold yellow]No towers collected yet![/bold yellow]")
                else:
                    towers_table = Table(title=f"Collected Towers ({len(towers)})", show_header=True)
                    
                    towers_table.add_column("MCC", style="cyan")
                    towers_table.add_column("MNC", style="cyan")
                    towers_table.add_column("LAC", style="cyan")
                    towers_table.add_column("CID", style="cyan")
                    towers_table.add_column("Area", style="green")
                    towers_table.add_column("Coordinates", style="yellow")
                    
                    for tower in towers:
                        towers_table.add_row(
                            str(tower['mcc']),
                            str(tower['mnc']),
                            str(tower['lac']),
                            str(tower['cid']),
                            tower.get('area', 'Unknown'),
                            f"{tower['lat']:.6f}, {tower['lon']:.6f}"
                        )
                    
                    console.print(towers_table)
            
            except Exception as e:
                console.print(f"[bold red]Error reading towers: {str(e)}[/bold red]")
            
            input("\nPress Enter to continue...")
            
        elif choice == "3":
            add_to_main_database()
            input("\nPress Enter to continue...")
            
        elif choice == "4":
            console.print("\n[bold]📝 Manual Tower Entry[/bold]")
            
            try:
                mcc = int(input("Enter MCC (e.g. 470 for Bangladesh): ") or "470")
                mnc = int(input("Enter MNC (1=GP, 2=Robi, 3=Banglalink, 4=Teletalk): "))
                lac = int(input("Enter LAC: "))
                cid = int(input("Enter CID: "))
                lat = float(input("Enter Latitude (e.g. 23.8103 for Dhaka): "))
                lon = float(input("Enter Longitude (e.g. 90.4125 for Dhaka): "))
                area = input("Enter Area Name (e.g. Dhaka, Gulshan): ")
                
                tower_data = {
                    'mcc': mcc,
                    'mnc': mnc,
                    'lac': lac,
                    'cid': cid,
                    'lat': lat,
                    'lon': lon,
                    'area': area,
                    'collected_time': time.strftime('%Y-%m-%d %H:%M:%S')
                }
                
                if save_cell_tower(tower_data):
                    console.print("[bold green]✅ Tower data saved successfully![/bold green]")
                else:
                    console.print("[bold yellow]Tower already exists in the database.[/bold yellow]")
                
            except ValueError as e:
                console.print(f"[bold red]Invalid input: {str(e)}[/bold red]")
            
            input("\nPress Enter to continue...")
            
        elif choice == "5":
            console.print("\n[bold green]Thank you for using Tower Data Collector![/bold green]")
            sys.exit(0)
        
        else:
            console.print("[bold red]Invalid choice. Please try again.[/bold red]")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
