#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Setting up VulnForge repository...${NC}"

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo -e "${RED}Git is not installed. Please install git first.${NC}"
    exit 1
fi

# Initialize git repository if not already initialized
if [ ! -d ".git" ]; then
    echo -e "${YELLOW}Initializing git repository...${NC}"
    git init
fi

# Add all files
echo -e "${YELLOW}Adding files to git...${NC}"
git add .

# Create initial commit
echo -e "${YELLOW}Creating initial commit...${NC}"
git commit -m "Initial commit: VulnForge AI-powered vulnerability research framework"

# Add remote repository
echo -e "${YELLOW}Adding remote repository...${NC}"
git remote add origin https://github.com/Arunking9/VulnForge.git

# Push to GitHub
echo -e "${YELLOW}Pushing to GitHub...${NC}"
git push -u origin main

echo -e "${GREEN}Repository setup complete!${NC}"
echo -e "You can now access your repository at: ${YELLOW}https://github.com/Arunking9/VulnForge${NC}" 