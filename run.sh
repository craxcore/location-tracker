#!/bin/bash
# CraxCore Location Tracker Wrapper Script

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Change to the script directory
cd "$SCRIPT_DIR"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "[*] Creating virtual environment..."
    python -m venv venv
    echo "[+] Virtual environment created"
fi

# Activate virtual environment
source venv/bin/activate

# Check if dependencies are installed
if ! python -c "import requests, rich, geopy, termcolor, configparser, cryptography" &> /dev/null; then
    echo "[*] Installing dependencies..."
    pip install -r requirements.txt
    echo "[+] Dependencies installed"
fi

# Initialize API keys if needed
if [ ! -f ".env" ]; then
    echo "[*] Initializing API keys..."
    python init_api_keys.py
fi

# Set up security features
echo "[*] Setting up security features..."
python setup_security.py

# Launch the main application
python main.py

# Deactivate virtual environment when done
deactivate
