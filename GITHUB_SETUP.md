# GitHub Repository Setup Instructions

Follow these steps to prepare your project for GitHub push:

## 1. Initialize Git Repository

```zsh
cd /data/Code/CraxCore/location
git init
```

## 2. Create .gitignore and Environmental Setup

The `.gitignore` file and `.env.example` have already been created for you.
Make sure `.env` is in your `.gitignore` file to prevent committing your API keys.

## 3. Make First Commit

```zsh
git add .
git commit -m "Initial commit: CraxCore Location Tracker"
```

## 4. Create GitHub Repository

Create a new repository on GitHub without initializing it with any files.

## 5. Connect and Push to GitHub

```zsh
git remote add origin https://github.com/yourusername/craxcore-location-tracker.git
git branch -M main
git push -u origin main
```

## 6. After Cloning on a New Device

When someone clones your repository, they should:

1. Run the installer first: `bash install.sh`
2. Enter their own API keys when prompted
3. Use `python launch.py` to start the application

## API Key Security

-   The real API keys are stored in `.env` (not committed)
-   The config.ini uses placeholders that refer to the env file
-   The init_api_keys.py script handles setup of API keys on first run

Your project now safely separates API keys from the code that gets pushed to GitHub!
