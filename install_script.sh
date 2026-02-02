#!/bin/bash
set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🧠 NeuroRift Unified Installer${NC}"
echo "=================================="

# 1. System Checks
echo -e "\n${BLUE}[1/9] System Checks...${NC}"

if [ "$EUID" -eq 0 ]; then 
    echo -e "${YELLOW}⚠️  Warning: Running as root. This script installs user-level tools (Rust, Go, Node).${NC}"
    echo -e "${YELLOW}    It is recommended to run as a normal user with sudo privileges for system packages.${NC}"
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Detect OS
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$NAME
    echo "Detected OS: $OS"
else
    echo "Unknown OS. Assuming generic Linux."
    OS="Linux"
fi

# 2. System Dependencies
echo -e "\n${BLUE}[2/9] Installing System Dependencies...${NC}"
if command -v apt-get &> /dev/null; then
    echo "Updating package list..."
    sudo apt-get update -qq
    echo "Installing base dependencies..."
    sudo apt-get install -y build-essential curl git python3-pip python3-venv python3-full unzip tor libssl-dev pkg-config
elif command -v yum &> /dev/null; then
    sudo yum install -y gcc gcc-c++ make curl git python3-pip python3-devel unzip tor openssl-devel
elif command -v pacman &> /dev/null; then
    sudo pacman -S --noconfirm base-devel curl git python python-pip unzip tor openssl
else
    echo -e "${YELLOW}Could not detect package manager. Please ensure basic dependencies are installed manually.${NC}"
fi

# 3. Rust Toolchain
echo -e "\n${BLUE}[3/9] Setting up Rust...${NC}"
if ! command -v rustc &> /dev/null; then
    echo "Installing Rust..."
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
    source "$HOME/.cargo/env"
else
    echo "Rust is already installed."
    # Ensure it's in path
    if [ -f "$HOME/.cargo/env" ]; then
        source "$HOME/.cargo/env"
    fi
fi

# 4. Go Toolchain (for Security Tools)
echo -e "\n${BLUE}[4/9] Setting up Go & Security Tools...${NC}"
if ! command -v go &> /dev/null; then
    echo "Go not found. Installing Go..."
    # Download generic linux amd64 - simplistic approach, might need version check
    GO_VER="1.21.6"
    wget https://go.dev/dl/go${GO_VER}.linux-amd64.tar.gz -O /tmp/go.tar.gz
    sudo rm -rf /usr/local/go && sudo tar -C /usr/local -xzf /tmp/go.tar.gz
    rm /tmp/go.tar.gz
    export PATH=$PATH:/usr/local/go/bin
    
    # Add to shell profile if not present
    if ! grep -q "/usr/local/go/bin" "$HOME/.bashrc"; then
         echo 'export PATH=$PATH:/usr/local/go/bin:$HOME/go/bin' >> "$HOME/.bashrc"
    fi
else
    echo "Go is already installed."
fi

# Need to ensure GOPATH/bin is in path for this session
export PATH=$PATH:$(go env GOPATH)/bin:/usr/local/go/bin

echo "Installing ProjectDiscovery tools..."
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest

# 5. Node.js & npm (Frontend)
echo -e "\n${BLUE}[5/9] Setting up Node.js...${NC}"
if ! command -v npm &> /dev/null; then
    echo "Installing Node.js..."
    # Using NVM is cleaner but apt is easier for a script
    if command -v apt-get &> /dev/null; then
        curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
        sudo apt-get install -y nodejs
    else
        echo -e "${YELLOW}Please install Node.js v18+ manually.${NC}"
    fi
else
    echo "Node.js is already installed."
fi

# 6. Python Environment
echo -e "\n${BLUE}[6/9] Setting up Python Environment...${NC}"
VENV_DIR=".venv"
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"

echo "Installing Python requirements..."
# Ensure pip is up to date
pip install --upgrade pip

# Core dependencies (recreating requirements.txt list here for safety)
pip install fastapi uvicorn requests python-dotenv rich dashmap httpx ollama beautifulsoup4 duckduckgo-search

# 7. Build Rust Core
echo -e "\n${BLUE}[7/9] Building Rust Core...${NC}"
cd core
cargo build --release
cd ..

# 8. Setup Web UI
echo -e "\n${BLUE}[8/9] Building Web UI...${NC}"
cd web-ui
if [ ! -d "node_modules" ]; then
    echo "Installing npm packages..."
    npm install
fi
echo "Building Next.js app..."
npm run build
cd ..

# 9. Configuration
echo -e "\n${BLUE}[9/9] Finalizing Configuration...${NC}"

# Create default .env if missing
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cat > .env <<EOL
# NeuroRift Configuration
LOG_LEVEL=INFO
AI_ENABLED=true
OLLAMA_MAIN_MODEL=llama3.2
OLLAMA_ASSISTANT_MODEL=llama3.2
NEURORIFT_HOME=$HOME/.neurorift
EOL
fi

# Setup Scripts
chmod +x scripts/*.sh

echo -e "\n${GREEN}✅ Installation Complete!${NC}"
echo "=================================="
echo -e "To start NeuroRift Web Mode:"
echo -e "  ${BLUE}./scripts/launch_web.sh${NC}"
echo -e "\nTo start CLI Mode with Wizard:"
echo -e "  ${BLUE}source .venv/bin/activate${NC}"
echo -e "  ${BLUE}./neurorift_main.py --configure${NC}"
echo "=================================="