#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Root Checker for CraxCore Location Tracker
------------------------------------------
This script checks if Termux has root access and additional capabilities
that would enhance the location tracker's functionality.
"""

import os
import sys
import subprocess
from rich.console import Console
from rich.panel import Panel

console = Console()

def check_command_exists(command):
    """Check if a command exists on the system"""
    try:
        return subprocess.call(['which', command], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0
    except:
        return False

def check_root():
    """Check if the device is rooted and Termux has root access"""
    # Check if su exists
    has_su = check_command_exists('su')
    
    # Try to run a command as root
    can_exec_root = False
    if has_su:
        try:
            result = subprocess.run(['su', '-c', 'id'], 
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.PIPE, 
                                  text=True,
                                  timeout=3)
            can_exec_root = result.returncode == 0 and 'uid=0' in result.stdout
        except:
            pass
    
    return has_su, can_exec_root

def check_termux_api():
    """Check if Termux:API is installed"""
    has_api = check_command_exists('termux-location')
    
    # Try to actually use the API
    api_works = False
    if has_api:
        try:
            result = subprocess.run(['termux-location', '-p', 'once'], 
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.PIPE, 
                                  text=True,
                                  timeout=5)
            api_works = result.returncode == 0
        except:
            pass
    
    return has_api, api_works

def check_gsm_tools():
    """Check if GSM-related tools are installed"""
    tools = {
        'minicom': check_command_exists('minicom'),
        'gammu': check_command_exists('gammu'),
        'at': check_command_exists('at')
    }
    
    return tools

def main():
    """Main function"""
    console.print(Panel.fit("[bold blue]CraxCore Location Tracker - System Check[/bold blue]", 
                           border_style="green"))
    
    console.print("\n[bold yellow]Checking device capabilities...[/bold yellow]")
    
    # Check root status
    has_su, can_exec_root = check_root()
    if can_exec_root:
        console.print("[bold green]✅ Root: Available and working[/bold green]")
    elif has_su:
        console.print("[bold yellow]⚠️ Root: Su binary found but execution failed[/bold yellow]")
    else:
        console.print("[bold red]❌ Root: Not available[/bold red]")
    
    # Check Termux API
    has_api, api_works = check_termux_api()
    if api_works:
        console.print("[bold green]✅ Termux:API: Installed and working[/bold green]")
    elif has_api:
        console.print("[bold yellow]⚠️ Termux:API: Installed but not working properly[/bold yellow]")
    else:
        console.print("[bold red]❌ Termux:API: Not installed[/bold red]")
    
    # Check GSM tools
    gsm_tools = check_gsm_tools()
    console.print("[bold]GSM Tools:[/bold]")
    for tool, exists in gsm_tools.items():
        status = "[bold green]✅ Installed[/bold green]" if exists else "[bold red]❌ Not installed[/bold red]"
        console.print(f"  - {tool}: {status}")
    
    # Summary
    console.print("\n[bold]Summary:[/bold]")
    
    if can_exec_root and api_works:
        console.print("[bold green]Your device is optimally configured for the location tracker.[/bold green]")
        console.print("All features including real GSM data access should work properly.")
    elif api_works:
        console.print("[bold yellow]Your device has partial capabilities for the location tracker.[/bold yellow]")
        console.print("Basic location features will work, but advanced GSM features require root.")
    else:
        console.print("[bold red]Your device has limited capabilities for the location tracker.[/bold red]")
        console.print("The tool will run in simulation mode only.")
    
    # Recommendations
    console.print("\n[bold]Recommendations:[/bold]")
    
    if not has_api:
        console.print("1. Install Termux:API app from F-Droid or Google Play")
        console.print("2. Install Termux:API package: pkg install termux-api")
    
    if not can_exec_root and has_su:
        console.print("- Check your root manager's settings and grant Termux proper permissions")
    
    console.print("\nRun main.py to start the location tracker.")

if __name__ == "__main__":
    main()
