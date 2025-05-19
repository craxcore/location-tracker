#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Export Utility for CraxCore Location Tracker
-------------------------------------------
This module provides functionality to export tracking data to various formats.
"""

import os
import sys
import json
import csv
import datetime
import hashlib
import getpass
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

LOG_FILE = "tracker_logs.dat"
CONFIG_FILE = "config.ini"

def decrypt_logs(config, password_hash):
    """Decrypt tracking logs"""
    if not os.path.exists(LOG_FILE):
        console.print("[bold yellow]No tracking history found![/bold yellow]")
        return None
    
    try:
        # Read the encrypted logs
        tracking_logs = []
        with open(LOG_FILE, 'rb') as f:
            for line in f:
                if line.strip():
                    if config.getboolean('SECURITY', 'encrypt_logs'):
                        # Decrypt the log entry
                        key = hashlib.sha256(b"craxcore-secure-key").digest()
                        decrypted = bytes([line[i] ^ key[i % len(key)] for i in range(len(line))])
                        data = json.loads(decrypted.decode('utf-8', errors='ignore'))
                    else:
                        # Plain JSON
                        data = json.loads(line.decode('utf-8', errors='ignore'))
                    
                    tracking_logs.append(data)
        
        return tracking_logs
    except Exception as e:
        console.print(f"[bold red]Error reading logs: {str(e)}[/bold red]")
        return None

def export_to_json(logs, output_file):
    """Export logs to JSON format"""
    try:
        with open(output_file, 'w') as f:
            json.dump(logs, f, indent=2)
        return True
    except Exception as e:
        console.print(f"[bold red]Error exporting to JSON: {str(e)}[/bold red]")
        return False

def export_to_csv(logs, output_file):
    """Export logs to CSV format"""
    try:
        # Define CSV headers
        headers = [
            'Timestamp', 'Target', 'Operator', 'Network Type', 'VoLTE',
            'LAC', 'CID', 'MCC', 'MNC', 'Latitude', 'Longitude', 'Address'
        ]
        
        with open(output_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            
            # Write each log entry
            for log in logs:
                row = {
                    'Timestamp': log['timestamp'],
                    'Target': log['target'],
                    'Operator': log['operator']['operator'],
                    'Network Type': log['operator']['network_type'],
                    'VoLTE': 'Yes' if log['operator']['volte'] else 'No',
                    'LAC': log['cell_info']['lac'],
                    'CID': log['cell_info']['cid'],
                    'MCC': log['cell_info']['mcc'],
                    'MNC': log['cell_info']['mnc'],
                    'Latitude': log['location']['latitude'],
                    'Longitude': log['location']['longitude'],
                    'Address': log['location']['address']
                }
                writer.writerow(row)
                
        return True
    except Exception as e:
        console.print(f"[bold red]Error exporting to CSV: {str(e)}[/bold red]")
        return False

def export_to_kml(logs, output_file):
    """Export logs to KML format for Google Earth/Maps"""
    try:
        # KML format template
        kml_template = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document>
    <name>CraxCore Location Tracker Data</name>
    <description>Mobile tracking data export</description>
    <Style id="mobilePinStyle">
        <IconStyle>
            <Icon>
                <href>http://maps.google.com/mapfiles/ms/icons/red-dot.png</href>
            </Icon>
        </IconStyle>
    </Style>
{placemarks}
</Document>
</kml>"""

        # Generate placemark entries
        placemarks = []
        for log in logs:
            timestamp = datetime.datetime.fromisoformat(log['timestamp']).strftime("%Y-%m-%d %H:%M:%S")
            placemark = f"""    <Placemark>
        <name>{log['target']}</name>
        <description>
            <![CDATA[
            <b>Time:</b> {timestamp}<br>
            <b>Operator:</b> {log['operator']['operator']}<br>
            <b>Network:</b> {log['operator']['network_type']}<br>
            <b>Address:</b> {log['location']['address']}<br>
            <b>LAC:</b> {log['cell_info']['lac']}<br>
            <b>CID:</b> {log['cell_info']['cid']}<br>
            ]]>
        </description>
        <styleUrl>#mobilePinStyle</styleUrl>
        <Point>
            <coordinates>{log['location']['longitude']},{log['location']['latitude']},0</coordinates>
        </Point>
    </Placemark>"""
            placemarks.append(placemark)
        
        # Write KML file
        with open(output_file, 'w') as f:
            f.write(kml_template.format(placemarks="\n".join(placemarks)))
            
        return True
    except Exception as e:
        console.print(f"[bold red]Error exporting to KML: {str(e)}[/bold red]")
        return False

def main():
    """Main function for the export utility"""
    import configparser
    
    os.system('clear')
    
    console.print(Panel.fit("[bold blue]CraxCore Location Tracker - Export Utility[/bold blue]", 
                           border_style="green"))
    
    # Load config
    config = configparser.ConfigParser()
    if not os.path.exists(CONFIG_FILE):
        console.print("[bold red]Error: Configuration file not found![/bold red]")
        return
    config.read(CONFIG_FILE)
    
    # Verify password
    password = getpass.getpass("Enter password to access logs: ")
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    if password_hash != config['SECURITY']['password_hash']:
        console.print("[bold red]Invalid password![/bold red]")
        return
    
    # Load and decrypt logs
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold green]Decrypting logs...[/bold green]"),
        transient=True,
    ) as progress:
        task = progress.add_task("", total=100)
        for i in range(101):
            progress.update(task, completed=i)
            if i % 10 == 0:
                progress.refresh()
            import time
            time.sleep(0.01)
    
    logs = decrypt_logs(config, password_hash)
    if not logs:
        return
    
    console.print(f"[bold green]✅ Found {len(logs)} log entries[/bold green]")
    
    # Export menu
    console.print("\n[bold yellow]Select export format:[/bold yellow]")
    console.print("[1] JSON")
    console.print("[2] CSV")
    console.print("[3] KML (for Google Earth/Maps)")
    console.print("[4] Cancel")
    
    choice = input("\nEnter your choice (1-4): ")
    
    if choice == "4":
        console.print("[bold yellow]Export cancelled.[/bold yellow]")
        return
    
    # Get output file
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if choice == "1":
        output_file = f"tracking_export_{timestamp}.json"
        console.print(f"\nExporting to JSON: {output_file}")
        success = export_to_json(logs, output_file)
    elif choice == "2":
        output_file = f"tracking_export_{timestamp}.csv"
        console.print(f"\nExporting to CSV: {output_file}")
        success = export_to_csv(logs, output_file)
    elif choice == "3":
        output_file = f"tracking_export_{timestamp}.kml"
        console.print(f"\nExporting to KML: {output_file}")
        success = export_to_kml(logs, output_file)
    else:
        console.print("[bold red]Invalid choice![/bold red]")
        return
    
    if success:
        console.print(f"[bold green]✅ Export completed successfully to {output_file}[/bold green]")
    
if __name__ == "__main__":
    main()
