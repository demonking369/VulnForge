#!/bin/bash
# NeuroRift Web Mode Troubleshooting Script

echo "🔍 NeuroRift Web Mode Diagnostics"
echo "=================================="
echo ""

# Check if virtual environment exists
echo "1. Checking virtual environment..."
if [ -d ".venv" ]; then
    echo "   ✅ Virtual environment found at .venv/"
else
    echo "   ❌ Virtual environment not found"
    echo "   Create one with: python3 -m venv .venv"
fi
echo ""

# Check if streamlit is installed
echo "2. Checking Streamlit installation..."
if [ -d ".venv" ]; then
    source .venv/bin/activate
    if python -c "import streamlit" 2>/dev/null; then
        STREAMLIT_VERSION=$(python -c "import streamlit; print(streamlit.__version__)")
        echo "   ✅ Streamlit installed (version $STREAMLIT_VERSION)"
    else
        echo "   ❌ Streamlit not installed in venv"
        echo "   Install with: pip install streamlit"
    fi
else
    if python3 -c "import streamlit" 2>/dev/null; then
        echo "   ✅ Streamlit installed globally"
    else
        echo "   ❌ Streamlit not installed"
        echo "   Install with: pip install streamlit"
    fi
fi
echo ""

# Check if langchain dependencies are installed
echo "3. Checking langchain dependencies..."
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi
if python -c "import langchain_core" 2>/dev/null; then
    echo "   ✅ langchain-core installed"
else
    echo "   ❌ langchain-core not installed"
    echo "   Install with: pip install langchain-core langchain-openai langchain-ollama"
fi
echo ""

# Check if Robin UI file exists
echo "4. Checking Robin UI file..."
if [ -f "modules/darkweb/robin/ui.py" ]; then
    echo "   ✅ Robin UI file found"
else
    echo "   ❌ Robin UI file not found at modules/darkweb/robin/ui.py"
fi
echo ""

# Check if port 8501 is in use
echo "5. Checking port 8501..."
if command -v netstat &> /dev/null; then
    if netstat -tuln | grep -q ":8501 "; then
        echo "   ⚠️  Port 8501 is already in use"
        echo "   Kill the process or use a different port: --web-port 8502"
    else
        echo "   ✅ Port 8501 is available"
    fi
elif command -v ss &> /dev/null; then
    if ss -tuln | grep -q ":8501 "; then
        echo "   ⚠️  Port 8501 is already in use"
        echo "   Kill the process or use a different port: --web-port 8502"
    else
        echo "   ✅ Port 8501 is available"
    fi
else
    echo "   ⚠️  Cannot check port (netstat/ss not found)"
fi
echo ""

# Check if Streamlit is running
echo "6. Checking for running Streamlit processes..."
if ps aux | grep -i streamlit | grep -v grep > /dev/null; then
    echo "   ✅ Streamlit process found:"
    ps aux | grep -i streamlit | grep -v grep | awk '{print "      PID: "$2" | "$11" "$12" "$13}'
else
    echo "   ❌ No Streamlit process running"
    echo "   Start with: neurorift --webmod"
fi
echo ""

echo "=================================="
echo "📋 Quick Start Commands:"
echo ""
echo "  # Activate venv and start web mode:"
echo "  source .venv/bin/activate"
echo "  python neurorift_main.py --webmod"
echo ""
echo "  # Or use custom port:"
echo "  python neurorift_main.py --webmod --web-port 8502"
echo ""
echo "  # Install missing dependencies:"
echo "  pip install streamlit langchain-core langchain-openai langchain-ollama"
echo ""
