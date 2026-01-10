#!/usr/bin/env python3
"""
VulnForge Web Interface Launcher
Quick launcher script for the Streamlit web UI
"""

import sys
from pathlib import Path


def main():
    """Launch the VulnForge web interface"""
    try:
        from streamlit.web import cli as stcli

        # Get the UI file path
        ui_file = Path(__file__).parent / "modules" / "darkweb" / "robin" / "ui.py"

        if not ui_file.exists():
            print(f"❌ Error: Web UI file not found at {ui_file}")
            print("Please ensure the Robin module is installed correctly.")
            return 1

        print("🌐 Launching VulnForge Web Interface...")
        print("📍 Access the UI at: http://localhost:8501")
        print("⚠️  Press Ctrl+C to stop the server\n")

        # Prepare streamlit arguments
        sys.argv = [
            "streamlit",
            "run",
            str(ui_file),
            "--server.port",
            "8501",
            "--server.address",
            "localhost",
            "--server.headless",
            "true",
            "--browser.gatherUsageStats",
            "false",
        ]

        # Launch streamlit
        sys.exit(stcli.main())

    except ImportError:
        print("❌ Error: Streamlit is not installed.")
        print("Install it with: pip install streamlit")
        return 1
    except KeyboardInterrupt:
        print("\n\n👋 Web interface stopped.")
        return 0
    except Exception as e:
        print(f"❌ Error launching web interface: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
