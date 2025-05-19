#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Launcher Script for CraxCore Location Tracker with Virtual Environment Support
-----------------------------------------------------------------------------
This script activates the virtual environment and launches the main application
"""

import os
import sys
import subprocess
import time
from pathlib import Path

# Path to virtual environment
VENV_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "venv")
VENV_PYTHON = os.path.join(VENV_DIR, "bin", "python")

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

def check_venv():
    """Check if the virtual environment exists and is activated"""
    if not os.path.exists(VENV_DIR):
        print("[!] Virtual environment not found")
        print("[*] Creating virtual environment...")
        try:
            subprocess.check_call([sys.executable, "-m", "venv", "venv"])
            print("[+] Virtual environment created successfully")
        except Exception as e:
            print(f"[-] Failed to create virtual environment: {e}")
            print("    Please create it manually with:")
            print(f"    {sys.executable} -m venv venv")
            return False

    # Check if requirements are installed
    print("[*] Checking requirements...")
    try:
        subprocess.check_call([VENV_PYTHON, "-c", "import requests, rich, geopy, termcolor, configparser, cryptography, dotenv"],
                             stderr=subprocess.DEVNULL)
        print("[+] All dependencies found")
    except:
        print("[!] Installing missing dependencies...")
        try:
            subprocess.check_call([os.path.join(VENV_DIR, "bin", "pip"), "install", "-r", "requirements.txt"])
            print("[+] Dependencies installed successfully")
        except Exception as e:
            print(f"[-] Failed to install dependencies: {e}")
            print("    Please install them manually with:")
            print(f"    {os.path.join(VENV_DIR, 'bin', 'pip')} install -r requirements.txt")
            return False
    
    return True

def launch_application():
    """Launch the main application using the virtual environment Python"""
    print("[*] Starting CraxCore Location Tracker...")
    print("[*] Press Ctrl+C to exit")
    time.sleep(1)
    
    try:
        # Run the main.py script with the virtual environment Python
        os.execv(VENV_PYTHON, [VENV_PYTHON, os.path.join(os.path.dirname(os.path.abspath(__file__)), "main.py")])
    except Exception as e:
        print(f"[-] Failed to launch application: {e}")
        return False
    
    return True

def main():
    print_banner()
    
    if not check_venv():
        print("[-] Failed to set up environment")
        print("    Please fix the issues and try again")
        return 1
    
    if not launch_application():
        print("[-] Application failed to start")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
