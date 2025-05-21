#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OpenCellID Configuration Checker for CraxCore Location Tracker
This utility helps verify that OpenCellID is correctly configured.
"""

import os
import sys
import configparser
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from dotenv import load_dotenv

CONFIG_FILE = "config.ini"
ENV_FILE = ".env"
console = Console()

def check_opencellid_configuration():
    """Check and verify OpenCellID configuration in both config.ini and .env"""
    console.print(Panel.fit(
        "[bold cyan]🔍 OpenCellID Configuration Checker[/bold cyan]\n\n"
        "This tool will check your OpenCellID configuration across all files.",
        title="🌍 Configuration Verification", 
        border_style="cyan"
    ))
    
    # Check .env file first
    env_path = Path(ENV_FILE)
    env_key = None
    env_exists = env_path.exists()
    
    if env_exists:
        console.print("[bold green]✓[/bold green] .env file exists")
        load_dotenv(env_path)
        env_key = os.getenv('OPENCELLID_API_KEY')
        
        if env_key:
            if env_key != "your_opencellid_api_key_here":
                console.print(f"[bold green]✓[/bold green] OpenCellID API key found in .env: {env_key[:4]}...{env_key[-4:]}")
            else:
                console.print("[bold red]✗[/bold red] OpenCellID API key in .env file is set to default placeholder value")
        else:
            console.print("[bold yellow]![/bold yellow] No OpenCellID API key found in .env file")
    else:
        console.print("[bold yellow]![/bold yellow] .env file does not exist")
    
    # Check config.ini file
    config_exists = os.path.exists(CONFIG_FILE)
    config_key = None
    
    if config_exists:
        console.print("[bold green]✓[/bold green] config.ini file exists")
        
        config = configparser.ConfigParser()
        config.read(CONFIG_FILE)
        
        if 'API' in config and 'opencellid_key' in config['API']:
            config_key = config['API']['opencellid_key']
            
            if config_key == "use_env_variable":
                console.print("[bold green]✓[/bold green] config.ini is set to use environment variable")
                
                if env_key and env_key != "your_opencellid_api_key_here":
                    console.print("[bold green]✓[/bold green] Environment variable contains valid API key")
                else:
                    console.print("[bold red]✗[/bold red] Environment variable is missing or invalid, but config is set to use it")
            elif config_key == "your_opencellid_api_key_here":
                console.print("[bold red]✗[/bold red] OpenCellID API key in config.ini is set to default placeholder value")
            else:
                console.print(f"[bold green]✓[/bold green] OpenCellID API key found in config.ini: {config_key[:4]}...{config_key[-4:]}")
                
                # Check if use_real_data is enabled
                if 'use_real_data' in config['API']:
                    if config['API']['use_real_data'].lower() == "true":
                        console.print("[bold green]✓[/bold green] Real data usage is enabled")
                    else:
                        console.print("[bold yellow]![/bold yellow] Real data usage is disabled")
                else:
                    console.print("[bold yellow]![/bold yellow] use_real_data setting not found")
        else:
            console.print("[bold red]✗[/bold red] No API section or opencellid_key found in config.ini")
    else:
        console.print("[bold red]✗[/bold red] config.ini file does not exist")
    
    # Summary table
    table = Table(title="OpenCellID Configuration Summary", show_header=True)
    table.add_column("Check", style="dim")
    table.add_column("Status", style="bold")
    
    # Config.ini file status
    config_status = "[bold green]VALID[/bold green]" if config_exists and config_key and config_key != "your_opencellid_api_key_here" else "[bold red]INVALID[/bold red]"
    if config_key == "use_env_variable":
        config_status = "[bold green]USING ENV[/bold green]" if env_key and env_key != "your_opencellid_api_key_here" else "[bold red]ENV NOT FOUND[/bold red]"
    
    # Env file status
    env_status = "[bold green]VALID[/bold green]" if env_exists and env_key and env_key != "your_opencellid_api_key_here" else "[bold red]INVALID[/bold red]"
    
    # Overall status
    if (config_key and config_key != "your_opencellid_api_key_here" and config_key != "use_env_variable") or \
       (config_key == "use_env_variable" and env_key and env_key != "your_opencellid_api_key_here"):
        overall_status = "[bold green]CONFIGURED[/bold green]"
    else:
        overall_status = "[bold red]NOT CONFIGURED[/bold red]"
    
    table.add_row("config.ini", config_status)
    table.add_row(".env file", env_status)
    table.add_row("Overall", overall_status)
    
    console.print("\n[bold]Configuration Summary:[/bold]")
    console.print(table)
    
    # Provide recommendations if there are issues
    if overall_status == "[bold red]NOT CONFIGURED[/bold red]":
        console.print("\n[bold yellow]Recommendation:[/bold yellow]")
        console.print("Run the OpenCellID setup utility by selecting option 'A' from the main menu.")
    else:
        console.print("\n[bold green]Your OpenCellID configuration appears to be valid.[/bold green]")

if __name__ == "__main__":
    check_opencellid_configuration()
