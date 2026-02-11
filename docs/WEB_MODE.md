# NeuroRift Web Mode

## Quick Start

Launch the NeuroRift web interface with a single command:

```bash
# Launch web interface (default: localhost:8501)
neurorift --webmod

# Customize host and port
neurorift --webmod --web-host 0.0.0.0 --web-port 8080

# Or use the standalone launcher
python3 launch_web.py
```

## Features

The web interface provides:

- 🕵️ **AI-Powered Dark Web OSINT** - Interactive search and analysis
- 🔍 **Query Refinement** - LLM-powered query optimization
- 📊 **Real-time Results** - Live filtering and scraping
- 📝 **Automated Summaries** - AI-generated investigation reports
- 💾 **Export Reports** - Download results in Markdown format
- 🎨 **Modern UI** - Dark-themed, responsive interface

## Access

Once launched, access the web interface at:
- **Default**: http://localhost:8501
- **Custom**: http://your-host:your-port

## Requirements

Ensure Streamlit is installed:
```bash
pip install streamlit
```

## Configuration

The web interface uses the same configuration as the CLI:
- AI models from `~/.neurorift/.env`
- Tor proxy at `127.0.0.1:9050`
- API keys for OpenAI/Anthropic/Google/Ollama

## Stopping the Server

Press `Ctrl+C` in the terminal to stop the web server.
