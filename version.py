#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Version and Metadata for CraxCore Location Tracker
-------------------------------------------------
This file contains version information and metadata for the application
"""

# Version information
VERSION = "1.0.0"
BUILD_DATE = "May 19, 2025"
AUTHOR = "CraxCore Team"

# Contact information
CONTACT_INFO = {
    "GitHub": "https://github.com/craxcore/location-tracker",
    "Telegram": "https://t.me/craxcore",
    "Facebook": "https://facebook.com/craxcore",
    "YouTube": "https://youtube.com/@craxcore",
    "TikTok": "https://tiktok.com/@craxcore",
    "Email": "contact@craxcore.com"
}

# Application metadata
APP_METADATA = {
    "name": "CraxCore Location Tracker",
    "description": "A secure Python-based CLI tool for tracking Bangladeshi mobile numbers",
    "purpose": "Educational purposes only",
    "language": "Python 3.8+",
    "platform": "Termux/Linux",
    "license": "MIT License"
}

def get_version_string():
    """Return formatted version string"""
    return f"CraxCore Location Tracker v{VERSION} (build {BUILD_DATE})"

def get_license_info():
    """Return license information"""
    return """
MIT License with Restrictions

Copyright (c) 2025 CraxCore Team

THIS SOFTWARE IS PROVIDED FOR EDUCATIONAL PURPOSES ONLY.
"""

def get_about_text():
    """Return formatted about text"""
    return f"""
CraxCore Location Tracker v{VERSION}
Created by {AUTHOR} on {BUILD_DATE}

A secure Python-based CLI tool for tracking mobile numbers through
cell tower information. This tool is created for educational purposes only.

DISCLAIMER: Using this tool to track individuals without consent
may be illegal in your jurisdiction. The creators assume no responsibility
for any misuse of this software.
"""

def print_contact_info():
    """Print contact information"""
    print("\nConnect with CraxCore:")
    for platform, url in CONTACT_INFO.items():
        print(f"• {platform}: {url}")
    print()

if __name__ == "__main__":
    # If run directly, print version info
    print(get_version_string())
    print(get_about_text())
    print_contact_info()
