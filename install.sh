#!/data/data/com.termux/files/usr/bin/bash

# CraxCore Location Tracker - Termux Installation Script
# This script will install all necessary dependencies for the tracker

echo "🔒 CraxCore Location Tracker - Termux Setup"
echo "=========================================="
echo

# Update repositories
echo "📦 Updating package repositories..."
pkg update -y

# Install required packages
echo "📦 Installing required packages..."
pkg install -y python git termux-api

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Make scripts executable
chmod +x main.py check_root.py crypto_utils.py init_api_keys.py

# Set up API keys
echo
echo "🔑 Setting up API keys..."
python init_api_keys.py

# Run system check
echo
echo "🔍 Running system capability check..."
python check_root.py

echo
echo "✅ Installation completed successfully!"
echo "📱 Run the tracker with: python main.py"
echo "🔑 Default password: CraxCoreLocat"
echo
echo "⚠️ DISCLAIMER: This tool is for EDUCATIONAL PURPOSES ONLY."
echo "   Using this tool to track individuals without consent may be illegal."
echo
