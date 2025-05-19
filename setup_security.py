#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Security Setup Script for CraxCore Location Tracker
--------------------------------------------------
This script sets up security features for the application.
"""

import os
import sys
import random
import string
import hashlib
import configparser
import time

CONFIG_FILE = "config.ini"
SALT_FILE = ".salt"
DEFAULT_PASSWORD = "CraxCoreLocat"

def generate_salt(length=32):
    """Generate a random salt for password hashing"""
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

def setup_salt():
    """Set up salt file for password hashing"""
    print("[*] Setting up password salt...")
    
    if os.path.exists(SALT_FILE):
        with open(SALT_FILE, 'r') as f:
            salt = f.read().strip()
        print("[+] Using existing salt")
    else:
        salt = generate_salt()
        with open(SALT_FILE, 'w') as f:
            f.write(salt)
        print("[+] Generated new salt")
    
    return salt

def hash_password(password, salt):
    """Hash password with salt"""
    salted_password = (password + salt).encode()
    return hashlib.sha256(salted_password).hexdigest()

def secure_password():
    """Ensure the password is properly secured"""
    print("[*] Securing password...")
    
    # Get salt
    salt = setup_salt()
    
    # Load config
    config = configparser.ConfigParser()
    if os.path.exists(CONFIG_FILE):
        config.read(CONFIG_FILE)
    else:
        print("[-] Config file not found!")
        return False
    
    # Check if password hash matches unsalted default
    current_hash = config['SECURITY']['password_hash']
    default_unsalted_hash = "eeed676313bd043bf65b7970d5641d94da9fe5c908f64a2b58851269d622c6c3" # CraxCoreLocat
    
    if current_hash == default_unsalted_hash:
        # Update to salted hash
        print("[*] Upgrading to salted password hash...")
        salted_hash = hash_password(DEFAULT_PASSWORD, salt)
        config['SECURITY']['password_hash'] = salted_hash
        
        # Save config
        with open(CONFIG_FILE, 'w') as f:
            config.write(f)
        
        print("[+] Password security upgraded")
    else:
        # Already using a custom password
        print("[+] Password already secure")
    
    return True

def secure_file_permissions():
    """Set proper file permissions for security files"""
    print("[*] Setting secure file permissions...")
    
    # Make security files readable only by owner
    security_files = [".env", ".salt", "config.ini"]
    for file in security_files:
        if os.path.exists(file):
            try:
                # 0o600 = readable/writable only by owner
                os.chmod(file, 0o600)
                print(f"[+] Secured {file}")
            except:
                print(f"[-] Could not secure {file}")
    
    return True

def main():
    print("\n🔒 CraxCore Location Tracker - Security Setup")
    print("=============================================")
    
    # Setup salt
    if not setup_salt():
        print("[-] Failed to set up salt")
        return 1
    
    # Secure password
    if not secure_password():
        print("[-] Failed to secure password")
        return 1
    
    # Set file permissions
    if not secure_file_permissions():
        print("[-] Failed to set file permissions")
        return 1
    
    print("\n[+] Security setup completed successfully!")
    print("[i] Default password: CraxCoreLocat")
    print("[i] It is recommended to change this password after first login.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
