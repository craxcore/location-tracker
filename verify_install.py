#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Installation Verification for CraxCore Location Tracker
------------------------------------------------------
This script verifies that the CraxCore Location Tracker is installed correctly.
"""

import os
import sys
import importlib
import platform
import subprocess

# Required modules to check
REQUIRED_MODULES = [
    "rich",
    "geopy",
    "requests",
    "termcolor",
    "configparser",
    "hashlib",
    "json",
    "datetime",
    "random"
]

# Required files to check
REQUIRED_FILES = [
    "main.py",
    "password_manager.py",
    "version.py",
    "api_key_handler.py",
    "config.ini",
    "run.sh",
    "tracker.sh",
    "setup_security.py"
]

def print_status(message, status):
    """Print a formatted status message"""
    if status:
        print(f"✅ {message}")
    else:
        print(f"❌ {message}")
    return status

def check_python_version():
    """Check Python version is 3.6+"""
    version = sys.version_info
    status = version.major == 3 and version.minor >= 6
    return print_status(f"Python version {version.major}.{version.minor}.{version.micro}", status)

def check_modules():
    """Check if required modules are installed"""
    missing = []
    for module in REQUIRED_MODULES:
        try:
            importlib.import_module(module)
        except ImportError:
            missing.append(module)
    
    if missing:
        print_status(f"Required modules: {', '.join(missing)} missing", False)
        return False
    else:
        print_status("All required modules are installed", True)
        return True

def check_files():
    """Check if required files exist"""
    missing = []
    for file in REQUIRED_FILES:
        if not os.path.exists(file):
            missing.append(file)
    
    if missing:
        print_status(f"Required files: {', '.join(missing)} missing", False)
        return False
    else:
        print_status("All required files are present", True)
        return True

def check_permissions():
    """Check if script files are executable"""
    not_executable = []
    for file in [f for f in REQUIRED_FILES if f.endswith('.py') or f.endswith('.sh')]:
        if os.path.exists(file) and not os.access(file, os.X_OK):
            not_executable.append(file)
    
    if not_executable:
        print_status(f"Scripts not executable: {', '.join(not_executable)}", False)
        return False
    else:
        print_status("All scripts have executable permissions", True)
        return True

def check_virtual_env():
    """Check if running in a virtual environment"""
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    return print_status("Running in virtual environment", in_venv)

def main():
    """Run all verification checks"""
    print("\n📊 CraxCore Location Tracker - Installation Verification")
    print("======================================================")
    
    system_ok = True
    
    # System checks
    print("\n🖥️  System Checks:")
    system_ok &= check_python_version()
    system_ok &= check_modules()
    
    # File checks
    print("\n📁 File Checks:")
    system_ok &= check_files()
    system_ok &= check_permissions()
    
    # Environment checks
    print("\n🌍 Environment Checks:")
    # We don't require virtual env, just inform
    check_virtual_env()
    
    # Summary
    print("\n📋 Summary:")
    if system_ok:
        print("✅ Your installation appears to be working correctly!")
        print("🚀 You can run the application with: ./run.sh")
    else:
        print("❌ There are issues with your installation.")
        print("📘 Please check the documentation or run: ./install.sh")
    
    return 0 if system_ok else 1

if __name__ == "__main__":
    sys.exit(main())
