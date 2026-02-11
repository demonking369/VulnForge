#!/bin/bash
set -e

echo "🌐 NeuroRift Tunnel Provider Installation"
echo "=========================================="
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" &> /dev/null
}

# ngrok
echo "📦 Checking ngrok..."
if ! command_exists ngrok; then
    echo "Installing ngrok..."
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
        echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
        sudo apt update
        sudo apt install ngrok
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew install ngrok/ngrok/ngrok
    else
        echo "Please install ngrok manually from https://ngrok.com/download"
    fi
else
    echo "✅ ngrok already installed ($(ngrok version))"
fi

# Cloudflare Tunnel
echo ""
echo "📦 Checking cloudflared..."
if ! command_exists cloudflared; then
    echo "Installing cloudflared..."
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
        sudo dpkg -i cloudflared-linux-amd64.deb
        rm cloudflared-linux-amd64.deb
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew install cloudflared
    else
        echo "Please install cloudflared manually from https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/installation/"
    fi
else
    echo "✅ cloudflared already installed ($(cloudflared --version))"
fi

# localtunnel
echo ""
echo "📦 Checking localtunnel..."
if ! command_exists lt; then
    echo "Installing localtunnel..."
    npm install -g localtunnel
else
    echo "✅ localtunnel already installed"
fi

# Python dependencies
echo ""
echo "🐍 Installing Python dependencies..."
pip3 install aiohttp --break-system-packages --quiet 2>/dev/null || pip3 install aiohttp --quiet

echo ""
echo "=========================================="
echo "✅ Tunnel providers installed!"
echo ""
echo "Available providers:"
python3 -m modules.web.tunnel_manager list
echo ""
echo "Usage:"
echo "  neurorift --webmod --online [provider]"
echo "  neurorift --webmod --online ngrok"
echo "  neurorift --webmod --online cloudflare"
echo "  neurorift --webmod --online auto"
echo "=========================================="
