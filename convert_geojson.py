#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GeoJSON to Cell Tower Converter for CraxCore Location Tracker
------------------------------------------------------------
This script converts GeoJSON data to cell tower database format
"""

import os
import sys
import json
import random
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

console = Console()

# Define file paths
GEOJSON_FILE = "CICO_Bangladesh_vF.geojson"
TOWERS_FILE = "bd_cell_towers.json"
OUTPUT_FILE = "combined_cell_towers.json"

def load_geojson():
    """Load and parse the GeoJSON file"""
    if not os.path.exists(GEOJSON_FILE):
        console.print(f"[bold red]Error: GeoJSON file '{GEOJSON_FILE}' not found![/bold red]")
        return None
    
    try:
        with open(GEOJSON_FILE, 'r') as f:
            geojson_data = json.load(f)
            
        return geojson_data
    except Exception as e:
        console.print(f"[bold red]Error loading GeoJSON: {str(e)}[/bold red]")
        return None

def load_tower_database():
    """Load the existing tower database"""
    if not os.path.exists(TOWERS_FILE):
        console.print(f"[bold yellow]Warning: Tower database file '{TOWERS_FILE}' not found. Creating new database.[/bold yellow]")
        return {
            "version": "1.0",
            "description": "Combined database of Bangladesh cell towers",
            "towers": [],
            "operators": {
                "1": {
                    "name": "GrameenPhone",
                    "prefixes": ["017", "013"]
                },
                "2": {
                    "name": "Robi",
                    "prefixes": ["018", "016"]
                },
                "3": {
                    "name": "Banglalink",
                    "prefixes": ["019", "014"]
                },
                "4": {
                    "name": "Teletalk",
                    "prefixes": ["015", "011"]
                }
            }
        }
    
    try:
        with open(TOWERS_FILE, 'r') as f:
            tower_data = json.load(f)
            
        return tower_data
    except Exception as e:
        console.print(f"[bold red]Error loading tower database: {str(e)}[/bold red]")
        return None

def get_area_name(lat, lon):
    """Approximate area name based on coordinates"""
    # Define regions (very approximate)
    regions = {
        "Dhaka": {
            "center": (23.8103, 90.4125),
            "radius": 0.3,
            "areas": ["Gulshan", "Dhanmondi", "Motijheel", "Banani", "Mirpur", "Uttara", "Mohakhali", "Badda", "Khilgaon"]
        },
        "Chittagong": {
            "center": (22.3569, 91.7832),
            "radius": 0.3,
            "areas": ["Agrabad", "GEC Circle", "Khulshi", "Halishahar", "Nasirabad", "Patenga", "Chawkbazar"]
        },
        "Sylhet": {
            "center": (24.8949, 91.8687),
            "radius": 0.3,
            "areas": ["Zindabazar", "Uposhohor", "Ambarkhana", "Tilagor", "Shibgonj", "Kotwali"]
        },
        "Rajshahi": {
            "center": (24.3745, 88.6042),
            "radius": 0.2,
            "areas": ["Shaheb Bazar", "Boalia", "Motihar", "Rajpara", "Upashahar"]
        },
        "Khulna": {
            "center": (22.8456, 89.5403),
            "radius": 0.2,
            "areas": ["Boyra", "Khalishpur", "Sonadanga", "Daulatpur", "Tootpara"]
        },
        "Barisal": {
            "center": (22.7010, 90.3535),
            "radius": 0.2,
            "areas": ["Natullabad", "Rupatali", "Amtala", "Kashipur", "Notullabad"]
        },
        "Rangpur": {
            "center": (25.7439, 89.2752),
            "radius": 0.2,
            "areas": ["Modern More", "Jahaj Company More", "Dhap", "Lalbag", "Station Road"]
        },
        "Comilla": {
            "center": (23.4607, 91.1809),
            "radius": 0.2,
            "areas": ["Kandirpar", "Bagichagaon", "Jhautola", "Tomsom Bridge", "Kotbari"]
        },
        "Mymensingh": {
            "center": (24.7539, 90.4073),
            "radius": 0.2,
            "areas": ["Ganginarpar", "Chorpara", "Durgabari Road", "Bolashpur", "Kachijhuli"]
        },
        "Jessore": {
            "center": (23.1698, 89.2137),
            "radius": 0.2,
            "areas": ["New Market", "M.K. Road", "Kharki", "Chanchra", "Benapole"]
        }
    }
    
    # Find closest region
    closest_region = None
    closest_distance = float('inf')
    
    for region_name, region_data in regions.items():
        region_lat, region_lon = region_data["center"]
        distance = ((lat - region_lat) ** 2 + (lon - region_lon) ** 2) ** 0.5
        
        if distance < closest_distance:
            closest_distance = distance
            closest_region = region_name
    
    # If close enough to a known region, use it with a random area
    if closest_region and closest_distance < regions[closest_region]["radius"]:
        area = random.choice(regions[closest_region]["areas"])
        return f"{closest_region}, {area}"
    
    # Default to division names based on general coordinates
    # These are very rough approximations
    if 23.5 < lat < 24.5 and 89.8 < lon < 91.0:
        return "Dhaka Division"
    elif 22.0 < lat < 23.0 and 91.0 < lon < 92.5:
        return "Chittagong Division"
    elif 24.5 < lat < 25.5 and 91.0 < lon < 92.5:
        return "Sylhet Division"
    elif 23.5 < lat < 25.0 and 88.0 < lon < 89.5:
        return "Rajshahi Division"
    elif 22.0 < lat < 23.5 and 89.0 < lon < 90.0:
        return "Khulna Division"
    elif 22.0 < lat < 23.0 and 90.0 < lon < 91.0:
        return "Barisal Division"
    elif 25.0 < lat < 26.5 and 88.5 < lon < 90.0:
        return "Rangpur Division"
    else:
        return "Bangladesh"

def generate_tower_from_geojson(feature, index):
    """Convert a GeoJSON feature to tower format"""
    # Extract coordinates
    lon, lat = feature["geometry"]["coordinates"]
    
    # Determine operator (mnc) and other fields
    mnc = (index % 3) + 1  # Cycle through 1, 2, 3 (GP, Robi, Banglalink)
    
    # Generate a unique LAC based on rough geographic area
    # This is a simplification - in reality, LACs have specific patterns
    lat_scaled = int((lat - 20.0) * 1000)  # Scale latitude to int
    lon_scaled = int((lon - 88.0) * 1000)  # Scale longitude to int
    lac_prefix = 40 + (index % 10)  # 40-49
    lac = int(f"{lac_prefix}{lat_scaled % 1000:03d}")
    
    # Generate a unique CID
    cid = 10000 + (index * 17) % 90000  # Generate a number between 10000 and 99999
    
    # Get area name
    area = get_area_name(lat, lon)
    
    # Create tower entry
    tower = {
        "mcc": 470,  # Bangladesh
        "mnc": mnc,
        "lac": lac,
        "cid": cid,
        "lat": lat,
        "lon": lon,
        "area": area
    }
    
    return tower

def convert_geojson_to_towers(geojson_data, tower_data, max_towers=None):
    """Convert GeoJSON features to tower format and merge with existing towers"""
    if not geojson_data or "features" not in geojson_data:
        console.print("[bold red]Error: Invalid GeoJSON format![/bold red]")
        return False
    
    features = geojson_data["features"]
    existing_towers = tower_data.get("towers", [])
    
    # Track existing tower coordinates to avoid duplicates
    existing_coords = set()
    for tower in existing_towers:
        coord_key = f"{tower['lat']:.6f},{tower['lon']:.6f}"
        existing_coords.add(coord_key)
    
    # Convert GeoJSON features to towers
    new_towers = []
    
    # Use progress bar
    total_features = len(features)
    if max_towers and max_towers < total_features:
        total_features = max_towers
    
    console.print(f"[bold]Processing {total_features} GeoJSON features...[/bold]")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold green]Converting GeoJSON data...[/bold green]"),
        transient=False,
    ) as progress:
        task = progress.add_task("", total=total_features)
        
        for i, feature in enumerate(features):
            if max_towers and i >= max_towers:
                break
                
            # Extract coordinates and check if tower already exists
            coords = feature["geometry"]["coordinates"]
            lon, lat = coords
            coord_key = f"{lat:.6f},{lon:.6f}"
            
            if coord_key in existing_coords:
                progress.update(task, advance=1)
                continue
            
            # Generate tower data
            tower = generate_tower_from_geojson(feature, i)
            new_towers.append(tower)
            existing_coords.add(coord_key)
            
            progress.update(task, advance=1)
    
    # Combine with existing towers
    combined_towers = existing_towers + new_towers
    tower_data["towers"] = combined_towers
    
    # Update description
    tower_data["description"] = "Combined database of Bangladesh cell towers from GeoJSON and simulation data"
    
    console.print(f"[bold green]✅ Added {len(new_towers)} new towers from GeoJSON![/bold green]")
    console.print(f"[bold green]Total towers in database: {len(combined_towers)}[/bold green]")
    
    return True

def save_tower_database(tower_data, output_file):
    """Save the updated tower database"""
    try:
        with open(output_file, 'w') as f:
            json.dump(tower_data, f, indent=4)
            
        console.print(f"[bold green]✅ Saved combined tower database to {output_file}![/bold green]")
        return True
    except Exception as e:
        console.print(f"[bold red]Error saving tower database: {str(e)}[/bold red]")
        return False

def main():
    """Main function"""
    os.system('clear')
    
    console.print(Panel.fit("[bold blue]CraxCore Location Tracker - GeoJSON Converter[/bold blue]", 
                           border_style="green"))
    
    # Load GeoJSON data
    console.print("[bold]Loading GeoJSON data...[/bold]")
    geojson_data = load_geojson()
    
    if not geojson_data:
        console.print("[bold red]Error: Failed to load GeoJSON data![/bold red]")
        return
    
    # Count features
    feature_count = len(geojson_data.get("features", []))
    console.print(f"[bold green]✅ Loaded GeoJSON file with {feature_count} features![/bold green]")
    
    # Load tower database
    console.print("[bold]Loading tower database...[/bold]")
    tower_data = load_tower_database()
    
    if not tower_data:
        console.print("[bold red]Error: Failed to load tower database![/bold red]")
        return
    
    existing_tower_count = len(tower_data.get("towers", []))
    console.print(f"[bold green]✅ Loaded tower database with {existing_tower_count} existing towers![/bold green]")
    
    # Ask user how many towers to import
    console.print("\n[bold yellow]The GeoJSON file contains many tower locations. How many would you like to import?[/bold yellow]")
    console.print("[1] Import 100 towers (quick)")
    console.print("[2] Import 500 towers (recommended)")
    console.print("[3] Import 1000 towers (comprehensive)")
    console.print("[4] Import all towers (may be slow)")
    console.print("[5] Cancel")
    
    choice = input("\nEnter your choice (1-5): ")
    
    max_towers = None
    if choice == "1":
        max_towers = 100
    elif choice == "2":
        max_towers = 500
    elif choice == "3":
        max_towers = 1000
    elif choice == "4":
        max_towers = None
    elif choice == "5":
        console.print("[bold yellow]Operation cancelled.[/bold yellow]")
        return
    else:
        console.print("[bold red]Invalid choice. Using default (500 towers).[/bold red]")
        max_towers = 500
    
    # Convert GeoJSON to tower format
    if convert_geojson_to_towers(geojson_data, tower_data, max_towers):
        # Ask if user wants to save
        save_choice = input("\nSave the combined tower database? (y/n): ")
        
        if save_choice.lower() == 'y':
            # Ask which file to save to
            console.print("\n[bold yellow]Where would you like to save the combined database?[/bold yellow]")
            console.print(f"[1] Replace existing database ({TOWERS_FILE})")
            console.print(f"[2] Create new database ({OUTPUT_FILE})")
            
            file_choice = input("\nEnter your choice (1-2): ")
            
            if file_choice == "1":
                save_tower_database(tower_data, TOWERS_FILE)
            else:
                save_tower_database(tower_data, OUTPUT_FILE)
        else:
            console.print("[bold yellow]Database not saved.[/bold yellow]")
    
    console.print("\n[bold green]GeoJSON conversion complete![/bold green]")

if __name__ == "__main__":
    main()
