#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Initialize API Keys Script for CraxCore Location Tracker
-------------------------------------------------------
This script initializes API keys and updates the config file
"""

import os
import sys
import configparser
from pathlib import Path

def main():
    env_file = '.env'
    config_file = 'config.ini'
    
    # Check if .env file exists
    if not os.path.exists(env_file):
        print("[!] No .env file found. Creating one...")
        
        # Ask user for API keys
        print("\n[*] You need an OpenCellID API key for full functionality")
        print("[*] You can get one for free at https://opencellid.org/register.php")
        
        opencellid_key = input("\nEnter your OpenCellID API key (or press Enter to skip): ")
        
        # Use default if user doesn't provide one
        if not opencellid_key:
            opencellid_key = 'your_opencellid_api_key_here'
            
        # Save to .env file
        with open(env_file, 'w') as f:
            f.write(f"OPENCELLID_API_KEY={opencellid_key}\n")
            f.write("GOOGLE_MAPS_API_KEY=your_google_maps_api_key_here\n")
            
        print("[+] .env file created with your API key")
    else:
        print("[+] .env file already exists")
        
    # Now update the config.ini file
    if os.path.exists(config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        
        # Read API key from .env file
        api_key = None
        with open(env_file, 'r') as f:
            for line in f:
                if line.startswith('OPENCELLID_API_KEY='):
                    api_key = line.strip().split('=', 1)[1]
                    break
        
        if api_key and api_key != 'your_opencellid_api_key_here' and 'API' in config:
            config['API']['opencellid_key'] = api_key
            with open(config_file, 'w') as f:
                config.write(f)
            print(f"[+] Updated config.ini with API key")
        else:
            print("[!] API key not found or already set in config.ini")
            
    print("\n[+] API key setup complete")

if __name__ == "__main__":
    main()
