#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Launcher Script for CraxCore Location Tracker
----------------------------------------------
This script checks for requirements and launches the main application
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def print_banner():
    """Print the launcher banner"""
    os.system('clear')
    print("""
█▀▀ █▀█ ▄▀█ ▀▄▀   █▀▀ █▀█ █▀█ █▀▀
█▄▄ █▀▄ █▀█ █░█   █▄▄ █▄█ █▀▄ ██▄

🔒 LOCATION TRACKER LAUNCHER 🔒
""")
    print("===============================")
    print()

def check_requirements():
    """Check if all required packages are installed"""
    try:
        import requests
        import geopy
        import rich
        import termcolor
        import configparser
        return True
    except ImportError as e:
        print(f"[!] Missing dependency: {str(e)}")
        print("[*] Installing dependencies...")
        
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                          check=True,
                          stdout=subprocess.PIPE, 
                          stderr=subprocess.PIPE)
            print("[+] Dependencies installed successfully")
            return True
        except Exception as e:
            print(f"[!] Error installing dependencies: {str(e)}")
            print("[*] Please run: pip install -r requirements.txt")
            return False

def check_api_keys():
    """Check if API keys are configured and set them up if needed"""
    env_path = Path(".env")
    
    if not env_path.exists():
        print("[*] API keys not configured")
        print("[*] Running API key setup...")
        
        try:
            subprocess.run([sys.executable, "init_api_keys.py"], 
                          check=True)
            return True
        except Exception as e:
            print(f"[!] Error setting up API keys: {str(e)}")
            return False
    
    return True

def main():
    """Main function to launch the application"""
    print_banner()
    
    print("[*] Checking requirements...")
    if not check_requirements():
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    print("[*] Checking API keys configuration...")
    if not check_api_keys():
        input("\nPress Enter to continue without API keys or Ctrl+C to exit...")
    
    print("[*] Launching CraxCore Location Tracker...")
    time.sleep(1)
    
    try:
        os.system('python main.py')
    except Exception as e:
        print(f"[!] Error launching application: {str(e)}")
        input("\nPress Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()
