# 🔒 CraxCore Location Tracker

A secure Python-based CLI tool for tracking real-time locations of Bangladeshi mobile numbers using cell tower information. This tool simulates or replicates behavior similar to cell tower triangulation by using mobile network metadata.

## ⚠️ Disclaimer

This tool is created for **EDUCATIONAL PURPOSES ONLY**. Using this tool to track individuals without their consent may be illegal in your jurisdiction. The creator of this tool assumes no responsibility for any misuse.

## 📋 Features

-   **Password Protection**: Secure access to the tool
-   **Bangladeshi Mobile Support**: Works with all Bangladesh operators (GP, Robi, Banglalink, Teletalk, Airtel)
-   **Tracking Simulation**: Simulates real-time tracking using:
    -   BTS tower info (LAC, CID, MCC, MNC)
    -   Coordinates mapping
    -   Reverse geocoding for address lookup
-   **Detailed Output**: Shows MSISDN, LAC, CID, coordinates, address, network status, and more
-   **Log Encryption**: Safely stores tracking history with encryption
-   **Map Visualization**: View tracking locations on interactive maps
-   **Data Export**: Export tracking data to JSON, CSV, or KML (Google Earth) formats
-   **System Check**: Verify if your device has the necessary capabilities
-   **API Integration**: OpenCellID integration for enhanced accuracy (API key required)

## 🛠️ Installation (Termux)

1. Install required packages:

```bash
apt update
apt upgrade -y
apt install python git termux-api -y
```

2. Clone this repository:

```bash
git clone https://github.com/craxcore/craxcore-location.git
cd craxcore-location
```

3. Run the installer:

```bash
bash run.sh
```

This will:

-   Create a virtual environment
-   Install all required dependencies
-   Setup your API keys (optional)
-   Start the application

### Using Virtual Environment (Alternative Setup)

If you prefer to manage the virtual environment manually:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Initialize API keys (if needed)
python init_api_keys.py

# Run the application
python main.py
```

## 🚀 Usage

### Basic Usage

Run the tool using the wrapper script:

```bash
./run.sh
```

Or using the launcher script:

```bash
./launcher.py
```

Or directly (if virtual environment is activated):

```bash
python main.py
```

-   Default password: `CraxCoreLocat`
-   You can change the password from the main menu after logging in
-   The password is securely stored using salted hashing for additional security

### API Keys

The application uses OpenCellID API for enhanced accuracy in location tracking. You can set up your API key in two ways:

1. During installation: The setup script will prompt you to enter your API key
2. Manually: You can create or edit the `.env` file with your API key

To get a free OpenCellID API key:

1. Register at https://opencellid.org/register.php
2. Copy your access token
3. Add it to the `.env` file as `OPENCELLID_API_KEY=your_key_here`

## 📍 Available Commands

-   **Track Mobile Number**: Enter a Bangladeshi mobile number to track
-   **View Tracking History**: See all previously tracked locations
-   **View Location Map**: Visualize tracking data on an interactive map
-   **Export Tracking Data**: Export tracking history to JSON, CSV, or KML formats
-   **Change Password**: Update your password for better security
-   **Clear Tracking History**: Delete all tracking logs
-   **System Capability Check**: Check if your device can support advanced features
-   **About**: Information about the application

## ⚙️ Configuration

Edit the `config.ini` file to customize:

-   API keys (for real implementation)
-   Security settings
-   Tracking preferences

## 🔍 How It Works

1. **Authentication**: Verifies user identity with password
2. **Mobile Number Validation**: Checks if the input is a valid Bangladeshi number
3. **BTS Data Collection**: Gathers or simulates cell tower information
4. **Location Triangulation**: Maps cell tower data to geographical coordinates
5. **Address Resolution**: Uses reverse geocoding to get human-readable addresses
6. **Results Display**: Shows all collected data in a formatted table

## 🚨 Advanced Features (For Rooted Devices)

For rooted devices, the tool can be extended to:

1. Read actual GSM modem data
2. Access real cell tower information
3. Monitor signal strength changes

To enable these features, set `use_real_data = true` in the config file.

## 📊 Dependencies

-   requests: For API communication
-   geopy: For geocoding and reverse geocoding
-   rich: For beautiful terminal output
-   termcolor: For colored text
-   cryptography: For secure encryption
-   webbrowser: For map visualization

## 🔒 Security

-   Password is stored as SHA-256 hash
-   Logs are encrypted using Fernet symmetric encryption
-   API keys are stored in a separate configuration file

## 🗺️ Map Visualization

The tool includes an interactive map feature that:

1. Shows the location of tracked mobile numbers on OpenStreetMap
2. Displays detailed information in popup windows
3. Allows viewing the latest location or all historical locations
4. Works directly in Termux's browser

## 📊 Data Export

You can export tracking data in multiple formats:

-   **JSON**: For developers or further processing
-   **CSV**: For spreadsheet analysis
-   **KML**: For viewing in Google Earth or Maps

## 👨‍💻 Author

CraxCore Team
