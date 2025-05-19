#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Setup Dependencies for CraxCore Location Tracker
-----------------------------------------------
This script installs all the required dependencies for the application.
"""

import os
import sys
import subprocess
import platform

def print_colored(text, color="white"):
    """Print colored text using termcolor if available"""
    try:
        from termcolor import colored
        print(colored(text, color))
    except ImportError:
        print(text)

def check_pip():
    """Check if pip is installed"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "--version"], 
                             stdout=subprocess.DEVNULL,
                             stderr=subprocess.DEVNULL)
        return True
    except:
        return False

def main():
    print_colored("\n[*] CraxCore Location Tracker - Dependency Setup", "cyan")
    print_colored("================================================", "cyan")
    
    # Check if we're running in Termux
    in_termux = os.environ.get('TERMUX_VERSION') is not None
    
    if in_termux:
        print_colored("\n[+] Termux environment detected", "green")
        
        # Install required Termux packages
        print_colored("\n[*] Installing required Termux packages...", "yellow")
        try:
            subprocess.check_call(["pkg", "update", "-y"], 
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL)
            subprocess.check_call(["pkg", "install", "-y", "python", "python-pip", "git"], 
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL)
            print_colored("[+] Termux packages installed successfully", "green")
        except:
            print_colored("[-] Failed to install Termux packages", "red")
            print_colored("    Please run 'pkg update && pkg install python python-pip git' manually", "yellow")
    
    # Check and install pip if needed
    if not check_pip():
        print_colored("\n[-] pip not found, attempting to install...", "red")
        try:
            subprocess.check_call([sys.executable, "-m", "ensurepip", "--default-pip"],
                                stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL)
            print_colored("[+] pip installed successfully", "green")
        except:
            print_colored("[-] Failed to install pip automatically", "red")
            print_colored("    Please install pip manually for your system", "yellow")
            sys.exit(1)
    
    # Install required Python packages
    print_colored("\n[*] Installing required Python packages...", "yellow")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL)
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.PIPE)
        print_colored("[+] All Python dependencies installed successfully", "green")
    except subprocess.CalledProcessError as e:
        print_colored(f"[-] Error installing dependencies: {e}", "red")
        print_colored("    You can try installing them manually with:", "yellow")
        print_colored(f"    {sys.executable} -m pip install -r requirements.txt", "yellow")
        sys.exit(1)
    
    # Initialize API keys
    print_colored("\n[*] Initializing API keys...", "yellow")
    try:
        subprocess.check_call([sys.executable, "init_api_keys.py"],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
        print_colored("[+] API keys initialized", "green")
    except:
        print_colored("[-] Failed to initialize API keys", "red")
        print_colored("    You can initialize them manually with:", "yellow")
        print_colored(f"    {sys.executable} init_api_keys.py", "yellow")
    
    # Final success message
    print_colored("\n[+] Setup completed successfully!", "green")
    print_colored("[+] You can now run the application with:", "green")
    print_colored(f"    {sys.executable} main.py", "cyan")
    print_colored("\n================================================", "cyan")

if __name__ == "__main__":
    main()
