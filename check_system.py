#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
System Capability Checker for CraxCore Location Tracker
------------------------------------------------------
This script checks if the system has the required capabilities
for full functionality of the location tracker.
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

def check_api_keys():
    """Check if API keys are configured"""
    env_file_exists = os.path.exists('.env')
    config_file_exists = os.path.exists('config.ini')
    api_key_status = "Not configured"
    
    if env_file_exists:
        with open('.env', 'r') as f:
            for line in f:
                if line.startswith('OPENCELLID_API_KEY='):
                    api_key = line.strip().split('=', 1)[1]
                    if api_key and api_key != 'your_opencellid_api_key_here':
                        api_key_status = "Configured and valid"
                    else:
                        api_key_status = "Configured but empty or default"
    
    return api_key_status, env_file_exists, config_file_exists

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
    
    # Check API keys
    api_key_status, env_exists, config_exists = check_api_keys()
    
    if api_key_status == "Configured and valid":
        console.print("[bold green]✅ API Keys: Properly configured[/bold green]")
    elif api_key_status == "Configured but empty or default":
        console.print("[bold yellow]⚠️ API Keys: Default or empty values found[/bold yellow]")
    else:
        console.print("[bold red]❌ API Keys: Not configured[/bold red]")
        console.print("   Run 'python init_api_keys.py' to set up API keys")
    
    # Configuration files
    if env_exists:
        console.print("[bold green]✅ Environment File: .env found[/bold green]")
    else:
        console.print("[bold red]❌ Environment File: .env not found[/bold red]")
    
    if config_exists:
        console.print("[bold green]✅ Configuration: config.ini found[/bold green]")
    else:
        console.print("[bold red]❌ Configuration: config.ini not found[/bold red]")
    
    # Summary
    console.print("\n[bold]Summary:[/bold]")
    
    if can_exec_root and api_works and api_key_status == "Configured and valid":
        console.print("[bold green]✅ Full functionality available[/bold green]")
        console.print("Your device is optimally configured for the location tracker.")
    elif api_key_status == "Configured and valid":
        console.print("[bold blue]ℹ️ Basic functionality available with API integration[/bold blue]")
        console.print("The tracker will work with API integration but without root features.")
    else:
        console.print("[bold yellow]⚠️ Limited functionality: Will use simulation only[/bold yellow]")
        console.print("Consider configuring API keys for better results.")
    
    # Recommendations
    console.print("\n[bold]Recommendations:[/bold]")
    
    if not has_api:
        console.print("1. Install Termux:API app from F-Droid or Google Play")
        console.print("2. Install Termux:API package: pkg install termux-api")
    
    if not can_exec_root and has_su:
        console.print("- Check your root manager's settings and grant Termux proper permissions")
    
    if api_key_status != "Configured and valid":
        console.print("- Run 'python init_api_keys.py' to set up your OpenCellID API key")
        console.print("  (Get a free key at: https://opencellid.org/register.php)")
    
    console.print("\nRun 'python main.py' or 'python launch.py' to start the location tracker.")

if __name__ == "__main__":
    main()
