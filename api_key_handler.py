#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
API Key Handler for CraxCore Location Tracker
-----------------------------------------------
This module provides functions for handling API keys.
"""

import os
import sys
import configparser
from pathlib import Path
from dotenv import load_dotenv, set_key

CONFIG_FILE = "config.ini"
ENV_FILE = ".env"

def load_api_keys():
    """
    Load API keys from .env file if it exists
    Otherwise, prompt user to input API keys and save them
    
    Returns:
        dict: API keys dictionary
    """
    env_path = Path(ENV_FILE)
    
    # Try to load from .env file
    if env_path.exists():
        load_dotenv(env_path)
        
        # If keys are in environment, return them
        opencellid_key = os.getenv('OPENCELLID_API_KEY')
        google_maps_key = os.getenv('GOOGLE_MAPS_API_KEY')
        
        if opencellid_key and opencellid_key != 'your_opencellid_api_key_here':
            return {
                'opencellid_key': opencellid_key,
                'google_maps_key': google_maps_key
            }
    
    # If keys not found or invalid, ask user to input them
    print("\n[!] API keys not found or invalid in .env file")
    print("[*] You can obtain a free OpenCellID API key at: https://opencellid.org/register.php")
    print("[*] The Google Maps API key is optional and not required for basic functionality")
    
    opencellid_key = input("\nEnter your OpenCellID API key (press Enter to skip): ")
    google_maps_key = input("Enter your Google Maps API key (press Enter to skip): ")
    
    # Default values if user skips
    if not opencellid_key:
        opencellid_key = 'your_opencellid_api_key_here'
    
    if not google_maps_key:
        google_maps_key = 'your_google_maps_api_key_here'
    
    # Save to .env file
    with open(env_path, 'w') as f:
        f.write(f"OPENCELLID_API_KEY={opencellid_key}\n")
        f.write(f"GOOGLE_MAPS_API_KEY={google_maps_key}\n")
    
    print("[+] API keys saved to .env file")
    
    return {
        'opencellid_key': opencellid_key,
        'google_maps_key': google_maps_key
    }

def update_config_with_api_keys(keys):
    """
    Update config.ini with API keys
    
    Args:
        keys (dict): API keys dictionary
    """
    if not os.path.exists(CONFIG_FILE):
        return False
    
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    
    if 'API' not in config:
        config['API'] = {}
    
    config['API']['opencellid_key'] = keys['opencellid_key']
    config['API']['google_maps_key'] = keys['google_maps_key']
    
    with open(CONFIG_FILE, 'w') as f:
        config.write(f)
    
    return True

if __name__ == "__main__":
    # Test functionality
    keys = load_api_keys()
    update_config_with_api_keys(keys)
    print("API keys loaded and config updated")
