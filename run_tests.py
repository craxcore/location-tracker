#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test Script for CraxCore Location Tracker
-----------------------------------------
This script performs basic functionality tests on the location tracker.
"""

import os
import sys
import unittest
import configparser
import hashlib
import json
import tempfile
import shutil
from unittest.mock import patch, MagicMock

# Define test constants
TEST_CONFIG = "test_config.ini"
TEST_LOG = "test_logs.dat"
TEST_BD_NUMBER = "+8801712345678"
TEST_PASSWORD = "CraxCoreLocat"

class LocationTrackerTests(unittest.TestCase):
    """Test cases for the Location Tracker application"""
    
    def setUp(self):
        """Set up test environment"""
        # Create test config
        config = configparser.ConfigParser()
        config['API'] = {
            'opencellid_key': 'test_api_key',
            'google_maps_key': 'test_maps_key',
            'use_real_data': 'false'
        }
        
        config['SECURITY'] = {
            'password_hash': hashlib.sha256(TEST_PASSWORD.encode()).hexdigest(),
            'encrypt_logs': 'true',
        }
        
        config['SETTINGS'] = {
            'default_tracking_time': '30',
            'save_history': 'true',
        }
        
        with open(TEST_CONFIG, 'w') as f:
            config.write(f)
    
    def tearDown(self):
        """Clean up after tests"""
        # Remove test files
        if os.path.exists(TEST_CONFIG):
            os.remove(TEST_CONFIG)
        if os.path.exists(TEST_LOG):
            os.remove(TEST_LOG)
    
    def test_password_security(self):
        """Test password security functions"""
        try:
            from password_manager import check_password, secure_hash_password
            
            # Test with default password
            self.assertTrue(check_password(TEST_PASSWORD), "Default password should be accepted")
            
            # Test with wrong password
            self.assertFalse(check_password("wrong_password"), "Wrong password should be rejected")
            
            # Test hash generation
            password_hash = secure_hash_password("test_password")
            self.assertIsNotNone(password_hash, "Hash should be generated")
            self.assertTrue(isinstance(password_hash, str), "Hash should be a string")
            self.assertEqual(len(password_hash), 64, "Hash should be 64 characters (SHA-256)")
            
        except ImportError:
            self.skipTest("Password manager module not available")
    
    def test_bd_number_validation(self):
        """Test Bangladeshi number validation"""
        # Import main module
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        try:
            from main import LocationTracker
            
            # Create tracker instance
            tracker = LocationTracker()
            
            # Test valid numbers
            self.assertEqual(tracker.validate_bd_number("+8801712345678"), "+8801712345678")
            self.assertEqual(tracker.validate_bd_number("01712345678"), "+8801712345678")
            self.assertEqual(tracker.validate_bd_number("8801712345678"), "+8801712345678")
            
            # Test invalid numbers
            self.assertIsNone(tracker.validate_bd_number("+1234567890"), "Non-BD number should be rejected")
            self.assertIsNone(tracker.validate_bd_number("1234567890"), "Non-BD number should be rejected")
            self.assertIsNone(tracker.validate_bd_number(""), "Empty string should be rejected")
            
        except ImportError:
            self.skipTest("Main module not available")
    
    def test_operator_info(self):
        """Test operator information extraction"""
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        try:
            from main import LocationTracker
            
            # Create tracker instance
            tracker = LocationTracker()
            
            # Test operator detection
            operator_info = tracker.get_operator_info("+8801712345678")
            self.assertEqual(operator_info["operator"], "GrameenPhone")
            
            operator_info = tracker.get_operator_info("+8801912345678")
            self.assertEqual(operator_info["operator"], "Banglalink")
            
            operator_info = tracker.get_operator_info("+8801812345678")
            self.assertEqual(operator_info["operator"], "Robi")
            
        except ImportError:
            self.skipTest("Main module not available")

def run_tests():
    """Run all tests"""
    unittest.main(argv=['first-arg-is-ignored'], exit=False)

if __name__ == "__main__":
    print("🧪 Running CraxCore Location Tracker Tests")
    print("==========================================")
    run_tests()
