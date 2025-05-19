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

# Show branding information
echo
echo "📱 Connect with CraxCore:"
echo "   GitHub: https://github.com/craxcore/location-tracker"
echo "   Telegram: https://t.me/craxcore"
echo "   Facebook: https://facebook.com/craxcore"
echo "   YouTube: https://youtube.com/@craxcore"
echo "   TikTok: https://tiktok.com/@craxcore"
echo "   Email: contact@craxcore.com"
echo

# Launch the main application
python main.py

# Deactivate virtual environment when done
deactivate
