#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Password Manager for CraxCore Location Tracker
---------------------------------------------
This module provides secure password handling.
"""

import os
import sys
import hashlib
import configparser
import random
import string
import time
from getpass import getpass
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

# Password salting and extra security
PASSWORD_SALT_FILE = ".salt"
CONFIG_FILE = "config.ini"
console = Console()

def generate_salt(length=32):
    """Generate a random salt for password hashing"""
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

def load_or_create_salt():
    """Load existing salt or create a new one"""
    if os.path.exists(PASSWORD_SALT_FILE):
        with open(PASSWORD_SALT_FILE, 'r') as f:
            return f.read().strip()
    else:
        salt = generate_salt()
        with open(PASSWORD_SALT_FILE, 'w') as f:
            f.write(salt)
        return salt

def secure_hash_password(password):
    """Hash password with salt using SHA-256"""
    salt = load_or_create_salt()
    salted_password = (password + salt).encode()
    return hashlib.sha256(salted_password).hexdigest()

def check_password(password):
    """Check if password matches stored hash"""
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    
    stored_hash = config['SECURITY']['password_hash']
    
    # Calculate hash without salt for backward compatibility with initial setup
    basic_hash = hashlib.sha256(password.encode()).hexdigest()
    
    # If salt file exists, use secure hashing
    if os.path.exists(PASSWORD_SALT_FILE):
        password_hash = secure_hash_password(password)
    else:
        password_hash = basic_hash
    
    return password_hash == stored_hash or basic_hash == stored_hash

def set_password(new_password):
    """Set a new password"""
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    
    # Create secure hash
    password_hash = secure_hash_password(new_password)
    
    # Update config
    config['SECURITY']['password_hash'] = password_hash
    
    with open(CONFIG_FILE, 'w') as f:
        config.write(f)
    
    console.print("[bold green]✅ Password changed successfully![/bold green]")
    return True

def get_password_hint():
    """Return a hint for the default password without revealing it"""
    return "The default password is 'CraxCoreLocat'. Please change it after login."

if __name__ == "__main__":
    # Test functions
    print(f"Default password check: {check_password('CraxCoreLocat')}")
    
    # Help for command line
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("Password Manager for CraxCore Location Tracker")
        print("Usage:")
        print("  python password_manager.py check [password]")
        print("  python password_manager.py set [new_password]")
        print("  python password_manager.py hint")
        sys.exit(0)
    
    # Command line interface
    if len(sys.argv) > 1:
        if sys.argv[1] == "check" and len(sys.argv) > 2:
            result = check_password(sys.argv[2])
            print(f"Password check: {'✅ Valid' if result else '❌ Invalid'}")
        
        elif sys.argv[1] == "set" and len(sys.argv) > 2:
            set_password(sys.argv[2])
            print("Password changed successfully!")
            
        elif sys.argv[1] == "hint":
            print(get_password_hint())
            
        else:
            print("Invalid command. Use --help for usage information.")
