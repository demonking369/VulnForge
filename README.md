# VulnForge

An AI-powered vulnerability research framework for authorized security testing and bug bounty hunting.

## Features

- **Reconnaissance Module**
  - Subdomain discovery using multiple tools
  - Port scanning with stealth options
  - Web service enumeration
  - Vulnerability scanning
  - AI-powered analysis

- **Stealth Capabilities**
  - Random delays between requests
  - User agent rotation
  - Proxy support
  - Human-like behavior simulation

- **Reporting**
  - Markdown reports
  - JSON output
  - Detailed vulnerability information
  - AI-powered analysis and recommendations

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/vulnforge.git
cd vulnforge
```

2. Run the installation script:
```bash
./install_script.sh
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Basic reconnaissance:
```bash
vulnforge -t example.com -m recon
```

With stealth mode:
```bash
vulnforge -t example.com -m recon -s
```

Check tool availability:
```bash
vulnforge --check
```

## Requirements

- Python 3.8+
- Kali Linux (recommended)
- Required tools:
  - nmap
  - subfinder
  - httpx
  - nuclei
  - gobuster
  - ffuf
  - whatweb
  - dig

## Configuration

Configuration files are stored in `~/.vulnforge/configs/`:
- `tools.json`: Tool configurations
- `proxies.txt`: Proxy list (optional)

## Disclaimer

This tool is for educational purposes and authorized security testing only. Always obtain proper authorization before testing any system.

## License

MIT License - See LICENSE file for details 