#!/bin/bash
set -e

echo "🧠 NeuroRift Web Mode - Dependency Installation"
echo "================================================"
echo ""

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo "⚠️  Please do not run this script as root"
    exit 1
fi

# Install Rust
echo "📦 Checking Rust installation..."
if ! command -v rustc &> /dev/null; then
    echo "Installing Rust toolchain..."
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
    source "$HOME/.cargo/env"
    echo "✅ Rust installed"
else
    echo "✅ Rust already installed ($(rustc --version))"
fi

# Install npm
echo ""
echo "📦 Checking npm installation..."
if ! command -v npm &> /dev/null; then
    echo "Installing npm..."
    if command -v apt-get &> /dev/null; then
        sudo apt-get update
        sudo apt-get install -y npm
    elif command -v yum &> /dev/null; then
        sudo yum install -y npm
    elif command -v pacman &> /dev/null; then
        sudo pacman -S --noconfirm npm
    else
        echo "❌ Could not install npm automatically. Please install manually."
        exit 1
    fi
    echo "✅ npm installed"
else
    echo "✅ npm already installed ($(npm --version))"
fi

# Build Rust core
echo ""
echo "🔨 Building Rust orchestration core..."
cd core
cargo build --release
cd ..
echo "✅ Rust core built"

# Install frontend dependencies
echo ""
echo "📦 Installing frontend dependencies..."
cd web-ui
npm install
cd ..
echo "✅ Frontend dependencies installed"

# Install Python dependencies
echo ""
echo "🐍 Installing Python dependencies..."

# Check if we're on Kali Linux or similar with externally-managed environment
if pip3 install --help 2>&1 | grep -q "break-system-packages"; then
    echo "Detected externally-managed Python environment (Kali Linux)"
    echo "Installing via system package manager..."
    
    if command -v apt-get &> /dev/null; then
        sudo apt-get update -qq
        sudo apt-get install -y python3-fastapi python3-uvicorn 2>/dev/null || {
            echo "System packages not available, using --break-system-packages flag..."
            pip3 install fastapi uvicorn --break-system-packages --quiet
        }
    else
        echo "Using --break-system-packages flag..."
        pip3 install fastapi uvicorn --break-system-packages --quiet
    fi
else
    # Normal pip install
    pip3 install fastapi uvicorn --quiet
fi

echo "✅ Python dependencies installed"

echo ""
echo "================================================"
echo "✅ Installation complete!"
echo ""
echo "To launch NeuroRift Web Mode:"
echo "  neurorift --webmod"
echo ""
echo "Or use the launch script:"
echo "  ./scripts/launch_web.sh"
echo "================================================"
