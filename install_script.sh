#!/bin/bash

# ╔══════════════════════════════════════════════════════════╗
# ║ VulnForge - Built with Blood by DemonKing369.0 👑        ║
# ║ GitHub: https://github.com/Arunking9                     ║
# ║ AI-Powered Security Framework for Bug Bounty Warriors ⚔️║
# ╚══════════════════════════════════════════════════════════╝

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to check if a command exists
check_command() {
    if command -v $1 &> /dev/null; then
        echo -e "${GREEN}[✓] $1 is installed${NC}"
        return 0
    else
        echo -e "${RED}[✗] $1 is not installed${NC}"
        return 1
    fi
}

# Function to check Python package
check_python_package() {
    if python3 -c "import $1" &> /dev/null; then
        echo -e "${GREEN}[✓] Python package $1 is installed${NC}"
        return 0
    else
        echo -e "${RED}[✗] Python package $1 is not installed${NC}"
        return 1
    fi
}

echo -e "${BLUE}Starting VulnForge Installation...${NC}"
echo -e "${YELLOW}Checking system requirements...${NC}\n"

# Check Python
if ! check_command python3; then
    echo -e "${RED}Python 3 is required but not installed. Please install Python 3.8 or higher.${NC}"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 8 ]); then
    echo -e "${RED}Python 3.8 or higher is required. Current version: $PYTHON_VERSION${NC}"
    exit 1
fi

echo -e "${GREEN}Found Python $PYTHON_VERSION${NC}"

# Check required tools
echo -e "\n${YELLOW}Checking required tools...${NC}"
TOOLS=("nmap" "dig" "go" "git")
MISSING_TOOLS=()

for tool in "${TOOLS[@]}"; do
    if ! check_command $tool; then
        MISSING_TOOLS+=($tool)
    fi
done

# Check Ollama
OLLAMA_INSTALLED=false
if check_command ollama; then
    OLLAMA_INSTALLED=true
    echo -e "\n${YELLOW}Checking Ollama models...${NC}"
    if ollama list | grep -q "deepseek-coder-v2:16b-lite-base-q4_0"; then
        echo -e "${GREEN}[✓] Main model (deepseek-coder) is installed${NC}"
    else
        echo -e "${YELLOW}[!] Main model is not installed${NC}"
    fi
    if ollama list | grep -q "mistral:7b-instruct-v0.2-q4_0"; then
        echo -e "${GREEN}[✓] Assistant model (mistral) is installed${NC}"
    else
        echo -e "${YELLOW}[!] Assistant model is not installed${NC}"
    fi
fi

# Installation summary
echo -e "\n${BLUE}Installation Summary:${NC}"
echo -e "Python Version: ${GREEN}$PYTHON_VERSION${NC}"
echo -e "Missing Tools: ${RED}${MISSING_TOOLS[@]}${NC}"
echo -e "Ollama Status: ${GREEN}$([ "$OLLAMA_INSTALLED" = true ] && echo "Installed" || echo "Not Installed")${NC}"

# Ask for installation preferences
echo -e "\n${YELLOW}Installation Options:${NC}"
read -p "Do you want to install missing tools? (y/N): " INSTALL_TOOLS
read -p "Do you want to install/update Ollama and AI models? (y/N): " INSTALL_AI

# Create virtual environment
echo -e "\n${BLUE}Setting up Python environment...${NC}"
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo -e "\n${BLUE}Installing Python dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-test.txt

# Install VulnForge globally
echo -e "\n${BLUE}Installing VulnForge globally...${NC}"
pip install -e .

# Install missing tools if requested
if [[ $INSTALL_TOOLS =~ ^[Yy]$ ]]; then
    echo -e "\n${BLUE}Installing missing tools...${NC}"
    
    # Install system tools
    if command -v apt &> /dev/null; then
        sudo apt update
        sudo apt install -y ${MISSING_TOOLS[@]}
    elif command -v yum &> /dev/null; then
        sudo yum install -y ${MISSING_TOOLS[@]}
    fi

    # Install Go tools if Go is available
    if check_command go; then
        echo -e "\n${BLUE}Installing Go tools...${NC}"
        go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
        go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
        go install -v github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest
        go install -v github.com/ffuf/ffuf@latest
        go install -v github.com/OJ/gobuster/v3@latest

        # Add Go bin to PATH if not already there
        if [[ ":$PATH:" != *":$HOME/go/bin:"* ]]; then
            echo 'export PATH=$PATH:$HOME/go/bin' >> ~/.bashrc
            source ~/.bashrc
        fi
    fi
fi

# Install Ollama and models if requested
if [[ $INSTALL_AI =~ ^[Yy]$ ]]; then
    echo -e "\n${BLUE}Setting up AI components...${NC}"
    
    if ! $OLLAMA_INSTALLED; then
        echo -e "${YELLOW}Installing Ollama...${NC}"
        curl -fsSL https://ollama.com/install.sh | sh
    fi

    echo -e "${YELLOW}Pulling required AI models...${NC}"
    ollama pull deepseek-coder-v2:16b-lite-base-q4_0
    ollama pull mistral:7b-instruct-v0.2-q4_0
fi

# Create necessary directories
echo -e "\n${BLUE}Setting up VulnForge directories...${NC}"
mkdir -p ~/.vulnforge/{configs,sessions,custom_tools}

# Create initial config files
echo -e "${BLUE}Creating configuration files...${NC}"
cat > ~/.vulnforge/configs/tools.json << EOL
{
    "nmap": {
        "enabled": true,
        "args": "-sV -sC --min-rate 1000"
    },
    "subfinder": {
        "enabled": true,
        "args": "-silent"
    },
    "httpx": {
        "enabled": true,
        "args": "-silent -title -status-code"
    }
}
EOL

# Make scripts executable
chmod +x vulnforge_main.py

echo -e "\n${GREEN}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                    Installation Complete!                  ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════╝${NC}"
echo -e "\nYou can now use VulnForge from anywhere by typing: ${GREEN}vulnforge${NC}"
echo -e "For help, run: ${GREEN}vulnforge -h${NC}"