#!/data/data/com.termux/files/usr/bin/bash

# CraxCore Mobile Tracker Launcher
# This script provides a quick way to launch the tracker

clear
echo "🔒 CraxCore Location Tracker Launcher"
echo "====================================="
echo

# Check if Python is installed
if ! command -v python &>/dev/null; then
    echo "❌ Python is not installed. Please run install.sh first."
    exit 1
fi

# Change to the script directory
cd "$(dirname "$0")"

# Make sure all scripts are executable
chmod +x main.py check_root.py crypto_utils.py export_utils.py map_view.py init_api_keys.py

# Check for API keys
if [ ! -f .env ]; then
    echo "🔑 Setting up API keys..."
    python init_api_keys.py
    echo
fi

# Launch the main application
echo "🚀 Launching CraxCore Location Tracker..."
echo
python main.py
