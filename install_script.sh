#!/bin/bash

# VulnForge Installation Script
# For Kali Linux systems

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    VulnForge Installer                       ║"
echo "║              Educational Security Framework                   ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if running on Kali Linux
if ! grep -q "kali" /etc/os-release 2>/dev/null; then
    echo -e "${YELLOW}Warning: This script is designed for Kali Linux${NC}"
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   echo -e "${RED}This script should not be run as root${NC}" 
   exit 1
fi

echo -e "${GREEN}[+] Starting VulnForge installation...${NC}"

# Update system packages
echo -e "${BLUE}[*] Updating system packages...${NC}"
sudo apt update

# Install Python dependencies
echo -e "${BLUE}[*] Installing Python dependencies...${NC}"
sudo apt install -y python3 python3-pip python3-venv

# Install basic tools
echo -e "${BLUE}[*] Installing basic security tools...${NC}"
sudo apt install -y \
    nmap \
    dnsutils \
    curl \
    wget \
    git \
    jq \
    whatweb \
    gobuster \
    ffuf

# Install Go if not present
if ! command -v go &> /dev/null; then
    echo -e "${BLUE}[*] Installing Go...${NC}"
    sudo apt install -y golang-go
    
    # Setup Go environment
    echo 'export GOPATH=$HOME/go' >> ~/.bashrc
    echo 'export PATH=$PATH:$GOPATH/bin' >> ~/.bashrc
    export GOPATH=$HOME/go
    export PATH=$PATH:$GOPATH/bin
    mkdir -p $GOPATH/bin
fi

# Install Go-based tools
echo -e "${BLUE}[*] Installing Go-based security tools...${NC}"

# Subfinder
if ! command -v subfinder &> /dev/null; then
    echo -e "${YELLOW}[*] Installing subfinder...${NC}"
    go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
fi

# HTTPx
if ! command -v httpx &> /dev/null; then
    echo -e "${YELLOW}[*] Installing httpx...${NC}"
    go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
fi

# Nuclei
if ! command -v nuclei &> /dev/null; then
    echo -e "${YELLOW}[*] Installing nuclei...${NC}"
    go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
fi

# Amass (alternative subdomain finder)
if ! command -v amass &> /dev/null; then
    echo -e "${YELLOW}[*] Installing amass...${NC}"
    go install -v github.com/owasp-amass/amass/v4/...@master
fi

# Create VulnForge directory structure
echo -e "${BLUE}[*] Setting up VulnForge directory structure...${NC}"
VULNFORGE_DIR="$HOME/.vulnforge"
mkdir -p "$VULNFORGE_DIR"/{modules,tools,results,configs,wordlists}

# Install Python requirements
echo -e "${BLUE}[*] Installing Python requirements...${NC}"
cat > "$VULNFORGE_DIR/requirements.txt" << EOF
requests>=2.28.0
beautifulsoup4>=4.11.0
lxml>=4.9.0
colorama>=0.4.5
rich>=12.5.0
click>=8.1.0
pydantic>=1.10.0
aiohttp>=3.8.0
asyncio-mqtt>=0.11.0
python-nmap>=0.7.1
python-whois>=0.8.0
dnspython>=2.2.0
validators>=0.20.0
urllib3>=1.26.0
EOF

pip3 install -r "$VULNFORGE_DIR/requirements.txt"

# Create configuration files
echo -e "${BLUE}[*] Creating configuration files...${NC}"

# Main config
cat > "$VULNFORGE_DIR/configs/config.json" << EOF
{
    "version": "1.0.0",
    "default_output_dir": "$VULNFORGE_DIR/results",
    "log_level": "INFO",
    "max_threads": 10,
    "timeout": 300,
    "user_agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "rate_limit": {
        "enabled": true,
        "delay": 1
    },
    "proxy": {
        "enabled": false,
        "http": "",
        "https": "",
        "socks": ""
    }
}
EOF

# Tool configurations
cat > "$VULNFORGE_DIR/configs/tools.json" << EOF
{
    "nmap": {
        "default_flags": ["-sS", "-T4", "--max-retries=1"],
        "stealth_flags": ["-sS", "-T2", "-f"],
        "aggressive_flags": ["-sS", "-T5", "-A"]
    },
    "subfinder": {
        "sources": ["bevigil", "binaryedge", "bufferover", "c99", "censys"],
        "timeout": 30
    },
    "httpx": {
        "threads": 50,
        "timeout": 10,
        "follow_redirects": true
    },
    "nuclei": {
        "update_templates": true,
        "severity": ["critical", "high", "medium"],
        "rate_limit": 150
    }
}
EOF

# Download common wordlists
echo -e "${BLUE}[*] Downloading wordlists...${NC}"
WORDLIST_DIR="$VULNFORGE_DIR/wordlists"

# SecLists (basic wordlists)
if [ ! -d "$WORDLIST_DIR/SecLists" ]; then
    echo -e "${YELLOW}[*] Downloading SecLists...${NC}"
    git clone https://github.com/danielmiessler/SecLists.git "$WORDLIST_DIR/SecLists" --depth 1
fi

# Create symbolic links for easy access
mkdir -p "$HOME/bin"
ln -sf "$PWD/vulnforge.py" "$HOME/bin/vulnforge"
chmod +x "$PWD/vulnforge.py"

# Add to PATH if not already there
if [[ ":$PATH:" != *":$HOME/bin:"* ]]; then
    echo 'export PATH="$HOME/bin:$PATH"' >> ~/.bashrc
fi

# Update nuclei templates
echo -e "${BLUE}[*] Updating Nuclei templates...${NC}"
if command -v nuclei &> /dev/null; then
    nuclei -update-templates -silent
fi

# Set up Ollama (optional)
read -p "Do you want to install Ollama for AI capabilities? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${BLUE}[*] Installing Ollama...${NC}"
    curl -fsSL https://ollama.ai/install.sh | sh
    
    echo -e "${YELLOW}[*] Installing AI models...${NC}"
    echo "This may take some time depending on your internet connection."
    
    # Install primary model
    echo -e "${BLUE}[*] Installing DeepSeek Coder v2 (Primary Model)...${NC}"
    ollama pull deepseek-coder-v2:16b-lite-base-q5_K_S
    
    # Install backup models
    echo -e "${BLUE}[*] Installing backup models...${NC}"
    ollama pull deepseek-coder:6.7b
    ollama pull codellama:7b
    ollama pull mistral:7b
    
    echo -e "${GREEN}[+] AI models installed successfully!${NC}"
    echo -e "${YELLOW}[*] You can manage models with:${NC}"
    echo "ollama list    # List installed models"
    echo "ollama rm <model>    # Remove a model"
    echo "ollama pull <model>  # Install additional models"
fi

# Create desktop shortcut
cat > "$HOME/Desktop/VulnForge.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=VulnForge
Comment=Educational Security Research Framework
Exec=gnome-terminal -- bash -c 'cd $(dirname $(readlink -f ~/.vulnforge)) && python3 vulnforge.py; exec bash'
Icon=utilities-terminal
Terminal=false
Categories=Application;Development;
EOF

chmod +x "$HOME/Desktop/VulnForge.desktop"

# Final checks
echo -e "${BLUE}[*] Running final checks...${NC}"

# Test tool availability
TOOLS=("nmap" "subfinder" "httpx" "nuclei" "gobuster" "ffuf")
MISSING_TOOLS=()

for tool in "${TOOLS[@]}"; do
    if ! command -v "$tool" &> /dev/null; then
        MISSING_TOOLS+=("$tool")
    fi
done

if [ ${#MISSING_TOOLS[@]} -eq 0 ]; then
    echo -e "${GREEN}[+] All tools installed successfully!${NC}"
else
    echo -e "${YELLOW}[!] Missing tools: ${MISSING_TOOLS[*]}${NC}"
    echo -e "${YELLOW}[!] You may need to add ~/go/bin to your PATH or install manually${NC}"
fi

echo -e "${GREEN}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    Installation Complete!                    ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo -e "${BLUE}Usage Examples:${NC}"
echo "  vulnforge --check                    # Check tool availability"
echo "  vulnforge -t example.com -m recon    # Subdomain discovery"
echo "  vulnforge -t example.com -m scan     # Port scanning"
echo "  vulnforge -t example.com -m web      # Web service discovery"
echo ""
echo -e "${YELLOW}Remember: Only use on systems you own or have explicit authorization to test!${NC}"
echo ""
echo -e "${GREEN}VulnForge directory: $VULNFORGE_DIR${NC}"
echo -e "${GREEN}Logs and results will be saved there.${NC}"

# Source bashrc to update PATH
source ~/.bashrc 2>/dev/null || true

echo -e "${BLUE}Installation completed! Restart your terminal or run 'source ~/.bashrc' to use VulnForge.${NC}"