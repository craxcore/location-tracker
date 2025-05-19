# GitHub Repository Setup Instructions

Follow these steps to set up your CraxCore Location Tracker on GitHub:

## 1. Automated Setup (Recommended)

The easiest way to push your code to GitHub is to use the provided script:

```zsh
cd /data/Code/CraxCore/location
chmod +x push_to_github.sh
./push_to_github.sh
```

This script will:

-   Initialize a Git repository if needed
-   Set up the proper .gitignore file
-   Configure the remote repository
-   Commit all changes
-   Push to GitHub

## 2. Manual Setup

If you prefer to do it manually, follow these steps:

### Initialize Git Repository

```zsh
cd /data/Code/CraxCore/location
git init
```

### Verify .gitignore

Ensure your .gitignore file contains these entries to protect sensitive information:

```
# Environment variables
.env
.salt

# Logs and databases
tracker_logs.dat
*.log
*.sqlite

# Virtual environment
venv/
env/
```

### Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `location-tracker`
3. Description: "A secure Python-based CLI tool for tracking Bangladeshi mobile numbers"
4. Set to Public or Private as desired
5. Click "Create repository" without initializing with any files

### Configure Remote and Push

```zsh
git add .
git commit -m "Initial release: CraxCore Location Tracker v1.0"
git remote add origin https://github.com/craxcore/location-tracker.git
git branch -M main
git push -u origin main
```

## 3. After Pushing to GitHub

### Update Repository Settings

1. Go to your repository settings
2. Add topics: `python`, `location-tracking`, `cli-tool`, `termux`, `educational`
3. Enable Issues and Discussions for user feedback

### Create Documentation

Consider adding these pages to the repository Wiki:

-   Installation Guide
-   User Manual
-   API Integration Guide
-   Troubleshooting
-   Security Best Practices

## 4. For Users Cloning the Repository

When users clone your repository, they should:

1. Clone the repository:

    ```zsh
    git clone https://github.com/craxcore/location-tracker.git
    cd location-tracker
    ```

2. Run the installer:

    ```zsh
    bash install.sh
    ```

3. Set up security:

    ```zsh
    python setup_security.py
    ```

4. Run the application:
    ```zsh
    ./run.sh
    ```

## 5. Security Notes

-   API keys are stored in `.env` file, which is not committed to GitHub
-   Password salt is stored in `.salt` file, also excluded from version control
-   Default password "CraxCoreLocat" should be changed after first login
-   Always verify file permissions are correctly set with `setup_security.py`

## 6. Contact Information

All CraxCore contact information is included in the repository:

-   GitHub: https://github.com/craxcore/location-tracker
-   Telegram: https://t.me/craxcore
-   Facebook: https://facebook.com/craxcore
-   YouTube: https://youtube.com/@craxcore
-   TikTok: https://tiktok.com/@craxcore
-   Email: contact@craxcore.com
