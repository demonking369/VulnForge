#!/bin/bash

# ╔══════════════════════════════════════════════════════════╗
# ║                       VulnForge                          ║
# ║         Built with Blood by DemonKing369.0 👑            ║
# ║         GitHub: https://github.com/Arunking9             ║
# ║ AI-Powered Security Framework for Bug Bounty Warriors ⚔️ ║
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

# Function to start Ollama in background if not running
start_ollama_service() {
    # Check if ollama command exists first
    if ! command -v ollama &> /dev/null; then
        return 1
    fi

    if ! pgrep -x "ollama" > /dev/null; then
        echo -e "${YELLOW}Starting Ollama service in background...${NC}"
        ollama serve > /dev/null 2>&1 &
    fi

    # Wait for service to be responsive (applies even if already running)
    echo -e "${YELLOW}Waiting for Ollama service to be responsive...${NC}"
    local retries=0
    while ! ollama list > /dev/null 2>&1 && [ $retries -lt 15 ]; do
        sleep 2
        ((retries++))
    done

    if [ $retries -eq 15 ]; then
        echo -e "${RED}[✗] Ollama service not responding. Please start it manually.${NC}"
        return 1
    fi
    echo -e "${GREEN}[✓] Ollama service is responsive.${NC}"
    return 0
}

# Check Ollama and configure models
OLLAMA_INSTALLED=false
if check_command ollama; then
    OLLAMA_INSTALLED=true
    echo -e "\n${YELLOW}Setting up Ollama Service...${NC}"
    if start_ollama_service; then
        echo -e "\n${YELLOW}Fetching available models...${NC}"
        # Improved fetching: ensure we only get the names and ignore errors
        AVAILABLE_MODELS=($(ollama list 2>/dev/null | tail -n +2 | awk '{print $1}' | grep -v '^$'))
        
        if [ ${#AVAILABLE_MODELS[@]} -eq 0 ]; then
            echo -e "${YELLOW}[!] No models found installed in Ollama.${NC}"
        else
            echo -e "${GREEN}[✓] Successfully fetched ${#AVAILABLE_MODELS[@]} models:${NC}"
            for m in "${AVAILABLE_MODELS[@]}"; do
                echo -e " - $m"
            done
        fi
    else
        OLLAMA_INSTALLED=false
    fi
    
    RECOMMENDED_MODELS=(
        "deepseek-coder-v2:16b-lite-base-q4_0"
        "mistral:7b-instruct-v0.2-q4_0"
        "llama3:8b"
        "codellama:7b"
        "phi3:mini"
    )

    # Combine and deduplicate
    ALL_AVAILABLE_MODELS=($(echo "${RECOMMENDED_MODELS[@]} ${AVAILABLE_MODELS[@]}" | tr ' ' '\n' | sort -u | tr '\n' ' '))

    echo -e "\n${BLUE}--- Model Configuration ---${NC}"
    echo -e "Please select your preferred models by their number:"
    
    i=1
    for m in "${ALL_AVAILABLE_MODELS[@]}"; do
        status=""
        if [[ " ${AVAILABLE_MODELS[@]} " =~ " ${m} " ]]; then
            status="${GREEN}(Installed)${NC}"
        else
            status="${YELLOW}(Not Installed)${NC}"
        fi
        echo -e "$i) $m $status"
        ((i++))
    done
    CUSTOM_OPTION=$i
    echo -e "$CUSTOM_OPTION) Enter custom model name"

    # Selection function
    get_selection() {
        local type=$1
        local default=$2
        local choice
        
        read -p "Select $type Model (Number) [Default: $default]: " choice
        
        if [ -z "$choice" ]; then
            echo "$default"
        elif [[ "$choice" =~ ^[0-9]+$ ]] && [ "$choice" -eq "$CUSTOM_OPTION" ]; then
            read -p "Enter custom model name: " custom_val
            echo "$custom_val"
        elif [[ "$choice" =~ ^[0-9]+$ ]] && [ "$choice" -ge 1 ] && [ "$choice" -lt "$CUSTOM_OPTION" ]; then
            echo "${ALL_AVAILABLE_MODELS[$((choice-1))]}"
        else
            echo "$default"
        fi
    }

    # Select models
    MAIN_MODEL=$(get_selection "Main Logic" "deepseek-coder-v2:16b-lite-base-q4_0")
    ASSISTANT_MODEL=$(get_selection "Assistant/Chat" "mistral:7b-instruct-v0.2-q4_0")
    
    echo -e "\n${GREEN}Final Configuration:${NC}"
    echo -e "Main Model: ${BLUE}$MAIN_MODEL${NC}"
    echo -e "Assistant Model: ${BLUE}$ASSISTANT_MODEL${NC}"
    
    # Save to .env
    if [ -d ".env" ]; then rm -rf .env; fi
    echo "OLLAMA_MAIN_MODEL=$MAIN_MODEL" > .env
    echo "OLLAMA_ASSISTANT_MODEL=$ASSISTANT_MODEL" >> .env
    echo -e "${GREEN}[✓] Saved model configuration to .env${NC}"

    # Pre-pull selected models if they are not installed
    if ! [[ " ${AVAILABLE_MODELS[@]} " =~ " ${MAIN_MODEL} " ]]; then
        echo -e "${YELLOW}Pulling $MAIN_MODEL...${NC}"
        ollama pull "$MAIN_MODEL"
    fi
    if ! [[ " ${AVAILABLE_MODELS[@]} " =~ " ${ASSISTANT_MODEL} " ]]; then
        echo -e "${YELLOW}Pulling $ASSISTANT_MODEL...${NC}"
        ollama pull "$ASSISTANT_MODEL"
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

# Install Python dependencies and CLI
echo -e "\n${BLUE}Installing Python dependencies and CLI...${NC}"

python3 -m pip install -r requirements.txt --break-system-packages 2>/dev/null || python3 -m pip install -r requirements.txt
python3 -m pip install -r requirements-test.txt --break-system-packages 2>/dev/null || python3 -m pip install -r requirements-test.txt
python3 -m pip install . --break-system-packages 2>/dev/null || python3 -m pip install .

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

# Setting up VulnForge directories...
echo -e "\n${BLUE}Setting up VulnForge directories...${NC}"
mkdir -p ~/.vulnforge/{results,tools,sessions}

# Create global wrapper script and symlink
echo -e "${BLUE}Creating global command...${NC}"
INSTALL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cat > vulnforge << EOF
#!/bin/bash
# VulnForge Global Wrapper Script

# Absolute path to the main script
MAIN_SCRIPT="$INSTALL_DIR/vulnforge_main.py"

if [ ! -f "\$MAIN_SCRIPT" ]; then
    echo "❌ Error: Could not find vulnforge_main.py at \$MAIN_SCRIPT"
    exit 1
fi

# Activate virtual environment if it exists
if [ -f "$INSTALL_DIR/.venv/bin/activate" ]; then
    source "$INSTALL_DIR/.venv/bin/activate"
fi

# Run the script
exec python3 "\$MAIN_SCRIPT" "\$@"
EOF

chmod +x vulnforge

# Try to create symlink in /usr/local/bin
if command -v sudo &> /dev/null; then
    echo -e "${YELLOW}[!] Creating global symlink (requires sudo)...${NC}"
    sudo ln -sf "$INSTALL_DIR/vulnforge" /usr/local/bin/vulnforge && \
        echo -e "${GREEN}[✓] Created global command: vulnforge${NC}" || \
        echo -e "${YELLOW}[!] Could not create symlink manual action needed.${NC}"
else
    echo -e "${YELLOW}[!] sudo not available. Add to PATH manually: export PATH=\"$INSTALL_DIR:\$PATH\"${NC}"
fi

# Create initial config files
echo -e "${BLUE}Creating configuration files...${NC}"
mkdir -p ~/.vulnforge/configs
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