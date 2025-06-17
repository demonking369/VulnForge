#!/bin/bash

# ╔══════════════════════════════════════════════════════════╗
# ║ VulnForge - Built with Blood by DemonKing369.0 👑        ║
# ║ GitHub: https://github.com/Arunking9                     ║
# ║ AI-Powered Security Framework for Bug Bounty Warriors ⚔️║
# ╚══════════════════════════════════════════════════════════╝

echo "Installing VulnForge..."

# Check if Python 3.8+ is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required but not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
if (( $(echo "$PYTHON_VERSION < 3.8" | bc -l) )); then
    echo "Python 3.8 or higher is required. Current version: $PYTHON_VERSION"
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-test.txt

# Install VulnForge globally
echo "Installing VulnForge globally..."
pip install -e .

# Install required tools
echo "Installing required tools..."

# Check if apt is available (Debian/Ubuntu)
if command -v apt &> /dev/null; then
    sudo apt update
    sudo apt install -y nmap dnsutils
fi

# Check if yum is available (RHEL/CentOS)
if command -v yum &> /dev/null; then
    sudo yum install -y nmap bind-utils
fi

# Install Go tools
echo "Installing Go tools..."
if ! command -v go &> /dev/null; then
    echo "Go is required but not installed. Please install Go first."
    exit 1
fi

# Install Go tools
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

# Install Ollama
echo "Installing Ollama..."
if ! command -v ollama &> /dev/null; then
    curl -fsSL https://ollama.com/install.sh | sh
fi

# Pull required models
echo "Pulling required AI models..."
ollama pull deepseek-coder-v2:16b-lite-base-q4_0
ollama pull mistral:7b-instruct-v0.2-q4_0

# Create necessary directories
echo "Creating necessary directories..."
mkdir -p ~/.vulnforge/{configs,sessions,custom_tools}

# Create initial config files
echo "Creating initial configuration..."
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

echo "Installation complete! You can now use VulnForge from anywhere by typing 'vulnforge'"
echo "For help, run: vulnforge -h"