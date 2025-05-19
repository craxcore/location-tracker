#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Map Visualization Utility for CraxCore Location Tracker
-----------------------------------------------------
This module generates HTML map visualizations of tracking data.
"""

import os
import sys
import json
import hashlib
import getpass
import datetime
import configparser
import webbrowser
import tempfile
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

def generate_map_html(logs, map_type="all"):
    """Generate HTML with leaflet map"""
    # Filter logs based on map type
    if map_type == "latest" and logs:
        logs = [logs[-1]]  # Only the most recent log
    
    # Check if we have coordinates
    if not logs or not all(['location' in log and 'latitude' in log['location'] for log in logs]):
        return None
    
    # Map HTML template with Leaflet.js
    html_template = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CraxCore Location Tracker Map</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
    <style>
        body { padding: 0; margin: 0; }
        html, body, #map { height: 100%; width: 100%; }
        .info-content { font-family: Arial, sans-serif; }
    </style>
</head>
<body>
    <div id="map"></div>
    <script>
        var map = L.map('map');
        
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);
        
        var markers = [];
        var bounds = L.latLngBounds();
        
        // Define a custom icon
        var mobileIcon = L.icon({
            iconUrl: 'https://cdn-icons-png.flaticon.com/512/0/747.png',
            iconSize: [32, 32],
            iconAnchor: [16, 32],
            popupAnchor: [0, -32]
        });
        
        // Add markers for each tracking point
        var trackingData = {tracking_data};
        
        trackingData.forEach(function(point) {
            var lat = point.location.latitude;
            var lon = point.location.longitude;
            var latlng = L.latLng(lat, lon);
            
            bounds.extend(latlng);
            
            var timestamp = new Date(point.timestamp).toLocaleString();
            var popupContent = 
                '<div class="info-content">' +
                '<h3>Target: ' + point.target + '</h3>' +
                '<p><strong>Time:</strong> ' + timestamp + '</p>' +
                '<p><strong>Operator:</strong> ' + point.operator.operator + '</p>' +
                '<p><strong>Network:</strong> ' + point.operator.network_type + '</p>' +
                '<p><strong>LAC:</strong> ' + point.cell_info.lac + '</p>' +
                '<p><strong>CID:</strong> ' + point.cell_info.cid + '</p>' +
                '<p><strong>Coordinates:</strong> ' + lat.toFixed(6) + ', ' + lon.toFixed(6) + '</p>' +
                '<p><strong>Address:</strong> ' + point.location.address + '</p>' +
                '</div>';
            
            var marker = L.marker(latlng, {icon: mobileIcon}).addTo(map)
                .bindPopup(popupContent);
                
            markers.push(marker);
        });
        
        // Fit map to bounds of all markers
        if (markers.length > 0) {
            map.fitBounds(bounds, {padding: [30, 30]});
            
            // If only one marker, set a reasonable zoom
            if (markers.length === 1) {
                map.setZoom(15);
            }
            
            // Open popup for the last (most recent) marker
            markers[markers.length - 1].openPopup();
        }
    </script>
</body>
</html>"""

    # Replace tracking data placeholder with actual data
    html_content = html_template.replace("{tracking_data}", json.dumps(logs))
    
    return html_content

def open_map_in_browser(html_content):
    """Save HTML content to a temporary file and open in browser"""
    try:
        # Create a temporary HTML file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as f:
            f.write(html_content.encode('utf-8'))
            temp_path = f.name
        
        # Check if we're in Termux
        is_termux = 'TERMUX_VERSION' in os.environ
        
        # Try to open browser
        if is_termux:
            # In Termux, try using termux-open-url or xdg-open
            try:
                os.system(f'termux-open-url "file://{temp_path}"')
            except:
                os.system(f'xdg-open "{temp_path}"')
        else:
            # On regular Linux
            webbrowser.open(f'file://{temp_path}')
            
        console.print(f"[bold green]✅ Map opened in browser[/bold green]")
        console.print(f"[bold]If the map didn't open automatically, browse to:[/bold]")
        console.print(f"[bold blue]file://{temp_path}[/bold blue]")
        
        return temp_path
    except Exception as e:
        console.print(f"[bold red]Error opening browser: {str(e)}[/bold red]")
        return None

def main():
    """Main function for the map visualization utility"""
    
    os.system('clear')
    
    console.print(Panel.fit("[bold blue]CraxCore Location Tracker - Map Visualization[/bold blue]", 
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
            import time
            time.sleep(0.01)
    
    logs = decrypt_logs(config, password_hash)
    if not logs:
        return
    
    console.print(f"[bold green]✅ Found {len(logs)} log entries[/bold green]")
    
    # Map visualization menu
    console.print("\n[bold yellow]Select map type:[/bold yellow]")
    console.print("[1] Show latest tracking location only")
    console.print("[2] Show all tracking locations")
    console.print("[3] Cancel")
    
    choice = input("\nEnter your choice (1-3): ")
    
    if choice == "3":
        console.print("[bold yellow]Operation cancelled.[/bold yellow]")
        return
    
    map_type = "latest" if choice == "1" else "all"
    
    # Generate and open map
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold green]Generating map...[/bold green]"),
        transient=True,
    ) as progress:
        task = progress.add_task("", total=100)
        for i in range(101):
            progress.update(task, completed=i)
            import time
            time.sleep(0.01)
    
    html_content = generate_map_html(logs, map_type)
    
    if html_content:
        temp_path = open_map_in_browser(html_content)
        
        # Keep file reference for user if needed
        if temp_path:
            console.print(f"\n[bold]Map saved temporarily to:[/bold]")
            console.print(f"[bold blue]{temp_path}[/bold blue]")
            console.print("[bold yellow]Note: This file will be deleted when your system reboots.[/bold yellow]")
    else:
        console.print("[bold red]Error: Could not generate map. No valid location data.[/bold red]")
    
if __name__ == "__main__":
    main()
