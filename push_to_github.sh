#!/bin/bash
# Script to push the CraxCore Location Tracker to GitHub

# Colors for terminal output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}CraxCore Location Tracker - GitHub Push Tool${NC}"
echo "========================================"

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo -e "${RED}Error: Git is not installed. Please install git first.${NC}"
    exit 1
fi

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo -e "${YELLOW}Initializing git repository...${NC}"
    git init
    
    # Check if .gitignore exists
    if [ ! -f ".gitignore" ]; then
        echo -e "${YELLOW}Creating .gitignore file...${NC}"
        cat > .gitignore << EOL
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Environment variables
.env
.salt

# Virtual environment
venv/
env/

# Logs and databases
tracker_logs.dat
*.log
*.sqlite

# OS generated files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db
EOL
    fi
fi

# Set GitHub repository URL
read -p "Enter GitHub username (default: craxcore): " GITHUB_USER
GITHUB_USER=${GITHUB_USER:-craxcore}

read -p "Enter repository name (default: location-tracker): " REPO_NAME
REPO_NAME=${REPO_NAME:-location-tracker}

GITHUB_URL="https://github.com/${GITHUB_USER}/${REPO_NAME}.git"

# Check if the remote is already set
if ! git remote | grep -q "origin"; then
    echo -e "${YELLOW}Setting up remote repository...${NC}"
    git remote add origin $GITHUB_URL
else
    # Update the remote URL
    git remote set-url origin $GITHUB_URL
fi

# Add all files
echo -e "${YELLOW}Adding files to git...${NC}"
git add .

# Check if there are any changes to commit
if ! git diff --cached --quiet; then
    # Commit changes
    read -p "Enter commit message (default: 'Update CraxCore Location Tracker'): " COMMIT_MSG
    COMMIT_MSG=${COMMIT_MSG:-"Update CraxCore Location Tracker"}
    
    echo -e "${YELLOW}Committing changes...${NC}"
    git commit -m "$COMMIT_MSG"
else
    echo -e "${YELLOW}No changes to commit.${NC}"
fi

# Push to GitHub
echo -e "${YELLOW}Pushing to GitHub...${NC}"
echo -e "${YELLOW}Note: You may be prompted for your GitHub credentials.${NC}"
git push -u origin master

if [ $? -eq 0 ]; then
    echo -e "${GREEN}Successfully pushed to GitHub!${NC}"
    echo -e "${GREEN}Repository URL: ${GITHUB_URL}${NC}"
else
    echo -e "${RED}Failed to push to GitHub.${NC}"
    echo "Check your GitHub credentials and repository settings."
    echo "You might need to create the repository on GitHub first."
    echo "You can also try running: git push -u origin main"
fi

echo -e "${YELLOW}Done!${NC}"
