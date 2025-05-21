#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OpenCellID Configuration Utility for CraxCore Location Tracker
This utility helps users set up OpenCellID for accurate location tracking.
"""

import os
import sys
import configparser
import webbrowser
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.prompt import Prompt
from dotenv import load_dotenv

# Import API key handler
try:
    from api_key_handler import update_config_with_api_keys
except ImportError:
    def update_config_with_api_keys(api_keys):
        """Fallback function if api_key_handler import fails"""
        config = configparser.ConfigParser()
        if os.path.exists("config.ini"):
            config.read("config.ini")
            if 'API' not in config:
                config['API'] = {}
            config['API']['opencellid_key'] = api_keys.get('opencellid_key', '')
            with open("config.ini", 'w') as f:
                config.write(f)
            return True
        return False

CONFIG_FILE = "config.ini"
ENV_FILE = ".env"
console = Console()

def setup_opencellid():
    """Set up OpenCellID API for more accurate location tracking"""
    console.print(Panel.fit(
        "[bold cyan]📡 OpenCellID Setup[/bold cyan]\n\n"
        "This utility will help you configure OpenCellID for accurate location tracking.\n"
        "OpenCellID provides real cell tower data instead of simulated locations.",
        title="🌍 Real Location Tracking", 
        border_style="cyan"
    ))
    
    # Check current configuration
    config = configparser.ConfigParser()
    current_key = None
    
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)
        if 'API' in config and 'opencellid_key' in config['API']:
            config_key = config['API']['opencellid_key']
            
            # If using environment variable, check for the actual key
            if config_key == "use_env_variable":
                load_dotenv()
                env_key = os.getenv('OPENCELLID_API_KEY')
                if env_key and env_key != "your_opencellid_api_key_here":
                    current_key = env_key
                    console.print(f"[bold green]✅ OpenCellID API key found in environment variables: {current_key[:4]}...{current_key[-4:]}[/bold green]")
            # Otherwise use the key from config if it's valid
            elif config_key and config_key != "your_opencellid_api_key_here":
                current_key = config_key
                console.print(f"[bold green]✅ OpenCellID API key is already configured: {current_key[:4]}...{current_key[-4:]}[/bold green]")
    
    if current_key:
        update = Prompt.ask("Would you like to update your API key?", choices=["y", "n"], default="n")
        if update.lower() != "y":
            console.print("[bold yellow]Keeping existing API key.[/bold yellow]")
            
            # Make sure the key is also saved to .env file
            env_path = Path(ENV_FILE)
            if env_path.exists():
                # Read existing .env and check for key
                found_key = False
                with open(ENV_FILE, 'r') as f:
                    lines = f.readlines()
                    for line in lines:
                        if line.startswith("OPENCELLID_API_KEY="):
                            found_key = True
                            break
                
                if not found_key:
                    # Add key to .env file
                    with open(ENV_FILE, 'a') as f:
                        f.write(f"\nOPENCELLID_API_KEY={current_key}\n")
                    console.print("[bold green]✅ Also saved API key to .env file for better compatibility.[/bold green]")
            else:
                # Create .env file
                with open(ENV_FILE, 'w') as f:
                    f.write(f"OPENCELLID_API_KEY={current_key}\n")
                console.print("[bold green]✅ Also saved API key to .env file for better compatibility.[/bold green]")
            
            # Ask about enabling real data
            if 'API' in config and 'use_real_data' in config['API']:
                if config['API']['use_real_data'].lower() != "true":
                    console.print("\n[bold red]Warning: Real location data is currently DISABLED![/bold red]")
                    enable_real = Prompt.ask("Enable real location data?", choices=["y", "n"], default="y")
                    if enable_real.lower() == "y":
                        config['API']['use_real_data'] = "true"
                        with open(CONFIG_FILE, 'w') as f:
                            config.write(f)
                        console.print("[bold green]✅ Real location data has been ENABLED.[/bold green]")
                    else:
                        console.print("[bold yellow]Real location data remains DISABLED. You will see simulated locations.[/bold yellow]")
                else:
                    console.print("[bold green]✅ Real location data is already enabled.[/bold green]")
            return
    
    # Show information about OpenCellID
    console.print("\n[bold]What is OpenCellID?[/bold]")
    console.print("OpenCellID is an open database of cell towers worldwide. Using this data allows\n"
                  "the location tracker to show your real location instead of simulated data.")
    
    # Provide instructions to get an API key
    console.print("\n[bold]How to get an OpenCellID API key:[/bold]")
    console.print("1. Go to [link]https://opencellid.org/register.php[/link]")
    console.print("2. Register for a free account")
    console.print("3. After login, go to your account page")
    console.print("4. Copy your API key")
    
    # Ask if user wants to open website
    open_browser = Prompt.ask("\nOpen the OpenCellID website now?", choices=["y", "n"], default="y")
    if open_browser.lower() == "y":
        try:
            webbrowser.open("https://opencellid.org/register.php")
            console.print("[bold green]Opening website in your browser...[/bold green]")
        except:
            console.print("[bold yellow]Could not open browser. Please visit https://opencellid.org/register.php manually.[/bold yellow]")
    
    # Get API key from user
    api_key = Prompt.ask("\nEnter your OpenCellID API key", default="")
    
    if not api_key:
        console.print("[bold red]No API key provided. Location tracking will use simulated data.[/bold red]")
        return
    
    # Save the API key
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)
        if 'API' not in config:
            config['API'] = {}
        
        # Verify the API key before saving
        console.print("\n[bold]Verifying API key with OpenCellID...[/bold]")
        try:
            import requests
            
            # Try a simple query to OpenCellID with the provided key
            url = "https://opencellid.org/cell/get"
            params = {
                "key": api_key,
                "mcc": 470,    # Bangladesh MCC
                "mnc": 1,      # Example MNC (GrameenPhone)
                "lac": 42001,  # Example LAC
                "cellid": 12345, # Example Cell ID
                "format": "json"
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                console.print("[bold green]✅ API key is valid and working![/bold green]")
            elif response.status_code == 401 or response.status_code == 403:
                console.print("[bold red]❌ API key validation failed. The key may be invalid or expired.[/bold red]")
                retry = Prompt.ask("Continue saving this key anyway?", choices=["y", "n"], default="n")
                if retry.lower() != "y":
                    console.print("[bold yellow]OpenCellID setup cancelled.[/bold yellow]")
                    return
            else:
                console.print(f"[bold yellow]⚠️ API returned status code {response.status_code}. Continuing anyway.[/bold yellow]")
        except Exception as e:
            console.print(f"[bold yellow]⚠️ Could not verify API key: {str(e)}. Continuing anyway.[/bold yellow]")
        
        # Save the API key to config.ini
        config['API']['opencellid_key'] = api_key
        
        # Enable real data by default
        config['API']['use_real_data'] = "true"
        
        with open(CONFIG_FILE, 'w') as f:
            config.write(f)
            
        # Also save to .env file for better compatibility
        env_path = Path(ENV_FILE)
        if not env_path.exists():
            with open(ENV_FILE, 'w') as f:
                f.write(f"OPENCELLID_API_KEY={api_key}\n")
        else:
            # Read existing .env and update/add the key
            with open(ENV_FILE, 'r') as f:
                lines = f.readlines()
                
            key_set = False
            with open(ENV_FILE, 'w') as f:
                for line in lines:
                    if line.startswith("OPENCELLID_API_KEY="):
                        f.write(f"OPENCELLID_API_KEY={api_key}\n")
                        key_set = True
                    else:
                        f.write(line)
                        
                if not key_set:
                    f.write(f"\nOPENCELLID_API_KEY={api_key}\n")
        
        console.print("\n[bold green]✅ OpenCellID API key has been saved successfully![/bold green]")
        console.print("[bold green]✅ Real location data has been ENABLED.[/bold green]")
        console.print("[bold green]✅ Key saved to both config.ini and .env files.[/bold green]")
        console.print("\n[bold]Your tracker will now show your actual location in Dhaka instead of simulated data.[/bold]")
    else:
        console.print("[bold red]Error: Could not find config file.[/bold red]")
        
    input("\nPress Enter to return to the main menu...")

if __name__ == "__main__":
    setup_opencellid()