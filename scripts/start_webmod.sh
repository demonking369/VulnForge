#!/bin/bash
# VulnForge Web Mode Launcher
# Quick script to start the web interface

echo "🚀 Starting VulnForge Web Interface..."
echo ""

# Check if venv exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Run: python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Activate venv
source .venv/bin/activate

# Check if streamlit is installed
if ! python -c "import streamlit" 2>/dev/null; then
    echo "❌ Streamlit not installed!"
    echo "Installing Streamlit..."
    pip install streamlit
fi

# Check if langchain is installed
if ! python -c "import langchain_core" 2>/dev/null; then
    echo "❌ Langchain dependencies not installed!"
    echo "Installing dependencies..."
    pip install langchain-core langchain-openai langchain-ollama langchain-anthropic langchain-google-genai langchain-community
fi

echo "✅ All dependencies ready"
echo ""
echo "🌐 Launching web interface..."
echo "📍 Access at: http://localhost:8501"
echo "⚠️  Press Ctrl+C to stop"
echo ""

# Launch VulnForge web mode
python vulnforge_main.py --webmod
