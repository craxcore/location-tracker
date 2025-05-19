#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Password Checker for CraxCore Location Tracker
----------------------------------------------
This script verifies if a given password matches the password hash in config.ini.
"""

import sys
import hashlib
import configparser

def load_config_hash():
    """Load password hash from config.ini"""
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config['SECURITY']['password_hash']

def hash_password(password):
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(password):
    """Check if the password matches the stored hash"""
    stored_hash = load_config_hash()
    hashed = hash_password(password)
    if hashed == stored_hash:
        return True, stored_hash
    return False, stored_hash

def main():
    if len(sys.argv) > 1:
        # Get password from command line
        password = sys.argv[1]
    else:
        # Prompt for password
        password = input("Enter password to verify: ")
    
    is_correct, stored_hash = check_password(password)
    
    if is_correct:
        print(f"\n✅ Success! '{password}' is the correct password!")
    else:
        print(f"\n❌ '{password}' is NOT the correct password.")
        print(f"\nStored hash: {stored_hash}")
        print(f"Your hash:   {hash_password(password)}")
        
        # Try the default
        if check_password('CraxCoreLocat')[0]:
            print("\nℹ️ The default password is 'CraxCoreLocat'")

if __name__ == "__main__":
    main()
