#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Encryption Utility for CraxCore Location Tracker
-----------------------------------------------
This module provides encryption and decryption functions for secure data handling.
"""

import os
import sys
import base64
import hashlib
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from getpass import getpass

class CryptoUtils:
    """Utility class for encryption and decryption operations"""
    
    @staticmethod
    def generate_key(password, salt=None):
        """
        Generate a Fernet key from a password and salt
        
        Args:
            password (str): The password to derive the key from
            salt (bytes, optional): The salt for key derivation. If None, a random salt is generated.
            
        Returns:
            tuple: (key, salt) where key is the Fernet key and salt is the salt used
        """
        if salt is None:
            salt = os.urandom(16)
        elif isinstance(salt, str):
            salt = salt.encode()
            
        # Generate a key using PBKDF2
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key, salt
    
    @staticmethod
    def encrypt_data(data, key):
        """
        Encrypt data using Fernet symmetric encryption
        
        Args:
            data (str or bytes): The data to encrypt
            key (bytes): The Fernet key to use for encryption
            
        Returns:
            bytes: The encrypted data
        """
        if isinstance(data, str):
            data = data.encode()
            
        f = Fernet(key)
        return f.encrypt(data)
    
    @staticmethod
    def decrypt_data(encrypted_data, key):
        """
        Decrypt data using Fernet symmetric encryption
        
        Args:
            encrypted_data (bytes): The encrypted data to decrypt
            key (bytes): The Fernet key to use for decryption
            
        Returns:
            bytes: The decrypted data
        """
        f = Fernet(key)
        return f.decrypt(encrypted_data)
    
    @staticmethod
    def encrypt_file(input_file, output_file, password):
        """
        Encrypt a file using a password
        
        Args:
            input_file (str): The path to the file to encrypt
            output_file (str): The path to save the encrypted file
            password (str): The password to use for encryption
            
        Returns:
            bool: True if encryption was successful, False otherwise
        """
        try:
            # Generate a key from the password
            key, salt = CryptoUtils.generate_key(password)
            
            # Read the input file
            with open(input_file, 'rb') as f:
                data = f.read()
            
            # Encrypt the data
            encrypted_data = CryptoUtils.encrypt_data(data, key)
            
            # Write the salt and encrypted data to the output file
            with open(output_file, 'wb') as f:
                f.write(salt)  # First 16 bytes are the salt
                f.write(encrypted_data)
                
            return True
        except Exception as e:
            print(f"Encryption error: {str(e)}")
            return False
    
    @staticmethod
    def decrypt_file(input_file, output_file, password):
        """
        Decrypt a file using a password
        
        Args:
            input_file (str): The path to the encrypted file
            output_file (str): The path to save the decrypted file
            password (str): The password to use for decryption
            
        Returns:
            bool: True if decryption was successful, False otherwise
        """
        try:
            # Read the encrypted file
            with open(input_file, 'rb') as f:
                salt = f.read(16)  # First 16 bytes are the salt
                encrypted_data = f.read()
            
            # Generate the key from the password and salt
            key, _ = CryptoUtils.generate_key(password, salt)
            
            # Decrypt the data
            decrypted_data = CryptoUtils.decrypt_data(encrypted_data, key)
            
            # Write the decrypted data to the output file
            with open(output_file, 'wb') as f:
                f.write(decrypted_data)
                
            return True
        except Exception as e:
            print(f"Decryption error: {str(e)}")
            return False
    
    @staticmethod
    def hash_password(password):
        """
        Hash a password using SHA-256
        
        Args:
            password (str): The password to hash
            
        Returns:
            str: The hexadecimal digest of the hash
        """
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def verify_password(password, hash_value):
        """
        Verify a password against a hash
        
        Args:
            password (str): The password to verify
            hash_value (str): The hash to compare against
            
        Returns:
            bool: True if the password matches the hash, False otherwise
        """
        return CryptoUtils.hash_password(password) == hash_value


def main():
    """Command-line interface for the encryption utility"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python crypto_utils.py encrypt <input_file> <output_file>")
        print("  python crypto_utils.py decrypt <input_file> <output_file>")
        print("  python crypto_utils.py hash <password>")
        print("  python crypto_utils.py verify <password> <hash>")
        return
    
    command = sys.argv[1].lower()
    
    if command == "encrypt" and len(sys.argv) == 4:
        input_file = sys.argv[2]
        output_file = sys.argv[3]
        
        password = getpass("Enter encryption password: ")
        confirm = getpass("Confirm password: ")
        
        if password != confirm:
            print("Passwords do not match!")
            return
        
        if CryptoUtils.encrypt_file(input_file, output_file, password):
            print(f"File encrypted successfully: {output_file}")
        
    elif command == "decrypt" and len(sys.argv) == 4:
        input_file = sys.argv[2]
        output_file = sys.argv[3]
        
        password = getpass("Enter decryption password: ")
        
        if CryptoUtils.decrypt_file(input_file, output_file, password):
            print(f"File decrypted successfully: {output_file}")
    
    elif command == "hash" and len(sys.argv) == 3:
        password = sys.argv[2]
        print(f"Hash: {CryptoUtils.hash_password(password)}")
    
    elif command == "verify" and len(sys.argv) == 4:
        password = sys.argv[2]
        hash_value = sys.argv[3]
        
        if CryptoUtils.verify_password(password, hash_value):
            print("Password is correct!")
        else:
            print("Password is incorrect!")
    
    else:
        print("Invalid command or arguments!")
        

if __name__ == "__main__":
    main()
