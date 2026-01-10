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

# Check Ollama and configure models
OLLAMA_INSTALLED=false
if check_command ollama; then
    OLLAMA_INSTALLED=true
    echo -e "\n${YELLOW}Checking Ollama Setup...${NC}"
    
    # Get available models
    AVAILABLE_MODELS=$(ollama list | tail -n +2 | awk '{print $1}')
    
    if [ -z "$AVAILABLE_MODELS" ]; then
        echo -e "${YELLOW}[!] No models found installed.${NC}"
    else
        echo -e "${GREEN}Available models:${NC}"
        echo "$AVAILABLE_MODELS"
    fi

    # Function to select model
    select_model() {
        local type=$1
        local default=$2
        local selection=""
        
        echo -e "\n${BLUE}Select $type Model:${NC}"
        echo "1) Use Default ($default)"
        echo "2) Select from installed models"
        echo "3) Enter custom model name"
        
        read -p "Choice [1]: " choice
        choice=${choice:-1}
        
        case $choice in
            2)
                echo -e "\nInstalled models:"
                select m in $AVAILABLE_MODELS; do
                    if [ -n "$m" ]; then
                        selection=$m
                        break
                    fi
                done
                ;;
            3)
                read -p "Enter model name: " selection
                ;;
            *)
                selection=$default
                ;;
        esac
        echo "$selection"
    }

    # Select models
    echo -e "\n${YELLOW}Configuring AI Models...${NC}"
    MAIN_MODEL=$(select_model "Main (Logic/Reasoning)" "deepseek-coder-v2:16b-lite-base-q4_0")
    ASSISTANT_MODEL=$(select_model "Assistant (Fast/Chat)" "mistral:7b-instruct-v0.2-q4_0")
    
    echo -e "\n${GREEN}Selected Configuration:${NC}"
    echo -e "Main Model: $MAIN_MODEL"
    echo -e "Assistant Model: $ASSISTANT_MODEL"
    
    # Save to .env (remove if it's a directory)
    if [ -d ".env" ]; then
        echo -e "${YELLOW}[!] .env is a directory, removing it...${NC}"
        rm -rf .env
    fi
    echo "OLLAMA_MAIN_MODEL=$MAIN_MODEL" > .env
    echo "OLLAMA_ASSISTANT_MODEL=$ASSISTANT_MODEL" >> .env
    echo -e "${GREEN}[✓] Saved model configuration to .env${NC}"
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

# Install Python dependencies and CLI globally/for user
echo -e "\n${BLUE}Installing Python dependencies and CLI...${NC}"

# Prefer system-wide install when sudo is available and user consents
INSTALL_SCOPE="user"
if command -v sudo &> /dev/null; then
    read -p "Install system-wide using sudo? (y/N): " INSTALL_SYSTEM
    if [[ $INSTALL_SYSTEM =~ ^[Yy]$ ]]; then
        INSTALL_SCOPE="system"
    fi
fi

if [ "$INSTALL_SCOPE" = "system" ]; then
    echo -e "${YELLOW}Using sudo to install system-wide...${NC}"
    sudo python3 -m pip install --upgrade pip setuptools wheel
    sudo python3 -m pip install -r requirements.txt
    sudo python3 -m pip install -r requirements-test.txt
    sudo python3 -m pip install .
    # Determine system scripts directory
    SYSTEM_BIN=$(python3 -c 'import sysconfig; print(sysconfig.get_path("scripts"))' 2>/dev/null || echo "/usr/local/bin")
else
    echo -e "${YELLOW}Installing for current user (~/.local) or via pipx...${NC}"

    # Prefer pipx if available to avoid PEP 668 restrictions
    if command -v pipx &> /dev/null; then
        echo -e "${YELLOW}Using pipx to install in an isolated venv...${NC}"
        
        # Uninstall first if exists
        pipx uninstall vulnforge 2>/dev/null || true
        
        # Install the app with all dependencies
        pipx install . --force
        
        # Ensure shim is linked
        pipx ensurepath || true
        
        echo -e "${GREEN}[✓] Installed via pipx${NC}"
    else
        echo -e "${YELLOW}pipx not found, using pip with --break-system-packages...${NC}"
        # Fallback to user installation, with --break-system-packages for PEP 668 distros (Kali/Debian)
        python3 -m pip install --user --upgrade pip setuptools wheel --break-system-packages 2>/dev/null || python3 -m pip install --user --upgrade pip setuptools wheel
        python3 -m pip install --user -r requirements.txt --break-system-packages 2>/dev/null || python3 -m pip install --user -r requirements.txt
        python3 -m pip install --user -r requirements-test.txt --break-system-packages 2>/dev/null || python3 -m pip install --user -r requirements-test.txt
        python3 -m pip install --user . --break-system-packages 2>/dev/null || python3 -m pip install --user .
        echo -e "${GREEN}[✓] Installed via pip --user${NC}"
    fi

    # Ensure ~/.local/bin is on PATH for bash and zsh
    for RC in ~/.bashrc ~/.zshrc; do
        if [ -f "$RC" ]; then
            if ! grep -q "\.local/bin" "$RC"; then
                echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$RC"
            fi
        fi
    done

    # Update current shell PATH if needed
    if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
        export PATH="$HOME/.local/bin:$PATH"
    fi
    USER_BIN="$HOME/.local/bin"
fi

# Post-install verification and fallback
echo -e "\n${BLUE}Verifying CLI installation...${NC}"
if command -v vulnforge &> /dev/null; then
    echo -e "${GREEN}[✓] 'vulnforge' is available on PATH${NC}"
else
    echo -e "${YELLOW}[!] 'vulnforge' not found on PATH yet.${NC}"
    if [ "$INSTALL_SCOPE" = "system" ]; then
        # Try to create a symlink in /usr/local/bin
        SRC_PATH="${SYSTEM_BIN:-/usr/local/bin}/vulnforge"
        if [ ! -x "$SRC_PATH" ]; then
            # Some distros place console_scripts under /usr/bin
            [ -x "/usr/bin/vulnforge" ] && SRC_PATH="/usr/bin/vulnforge"
        fi
        if [ -x "$SRC_PATH" ]; then
            echo -e "${YELLOW}Creating symlink in /usr/local/bin for global access...${NC}"
            sudo ln -sf "$SRC_PATH" /usr/local/bin/vulnforge
        else
            echo -e "${RED}Could not locate installed script to symlink. Check your pip scripts directory.${NC}"
        fi
    else
        echo -e "${YELLOW}Adding ~/.local/bin to your PATH in the current session...${NC}"
        if [ -n "$USER_BIN" ]; then
            export PATH="$USER_BIN:$PATH"
        fi
        echo -e "${YELLOW}Open a new shell or 'source' your shell rc file to persist.${NC}"
    fi
    if command -v vulnforge &> /dev/null; then
        echo -e "${GREEN}[✓] 'vulnforge' is now available on PATH${NC}"
    else
        echo -e "${RED}[✗] 'vulnforge' still not on PATH. Try reloading your shell or check pip install logs.${NC}"
    fi
fi

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
INSTALL_DIR="$(pwd)"
cat > vulnforge << 'EOF'
#!/bin/bash
# VulnForge Global Wrapper Script

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Activate virtual environment if it exists
if [ -f "$SCRIPT_DIR/.venv/bin/activate" ]; then
    source "$SCRIPT_DIR/.venv/bin/activate"
    exec python3 "$SCRIPT_DIR/vulnforge_main.py" "$@"
else
    # Fallback to direct execution
    exec python3 "$SCRIPT_DIR/vulnforge_main.py" "$@"
fi
EOF

chmod +x vulnforge

# Try to create symlink in /usr/local/bin
if command -v sudo &> /dev/null; then
    if sudo -n true 2>/dev/null; then
        sudo ln -sf "$INSTALL_DIR/vulnforge" /usr/local/bin/vulnforge
        echo -e "${GREEN}[✓] Created global command: vulnforge${NC}"
    else
        echo -e "${YELLOW}[!] Creating global symlink (requires sudo)...${NC}"
        sudo ln -sf "$INSTALL_DIR/vulnforge" /usr/local/bin/vulnforge && \
            echo -e "${GREEN}[✓] Created global command: vulnforge${NC}" || \
            echo -e "${YELLOW}[!] Could not create symlink. Run manually: sudo ln -sf $INSTALL_DIR/vulnforge /usr/local/bin/vulnforge${NC}"
    fi
else
    echo -e "${YELLOW}[!] sudo not available. Add to PATH manually: export PATH=\"$INSTALL_DIR:\$PATH\"${NC}"
fi

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