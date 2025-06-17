# VulnForge

An AI-powered vulnerability research framework for authorized security testing and bug bounty hunting.

## Features

- **AI-Autonomous Operation**
  - Fully autonomous mode with `--ai-only` flag
  - AI-driven decision making for tool selection and attack sequencing
  - Real-time analysis and adaptation based on scan results
  - Automatic tool installation and updates
  - Detailed decision logging and reasoning

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

- **Notification System**
  - Multi-channel alerts (Email, Discord, Webhooks)
  - Severity levels (info, warning, high, critical)
  - Customizable notification settings

- **AI Assistant**
  - Interactive AI queries with `ask-ai` command
  - Context-aware responses
  - Security-focused guidance
  - Tool recommendations

- **Custom Tool Generation**
  - AI-powered tool creation
  - Automatic script generation
  - Tool metadata tracking
  - Success rate monitoring

- **Development Mode**
  - AI-assisted code improvements
  - Live module modifications
  - Modification history tracking
  - Backup and revert capabilities

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Arunking9/VulnForge.git
   cd VulnForge
   ```

2. Run the installation script:
   ```bash
   ./install_script.sh
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install Required Tools:
   - Ensure the following tools are installed and in your `PATH`:
     - `nmap`
     - `subfinder`
     - `httpx`
     - `nuclei`
     - `gobuster`
     - `ffuf`
     - `whatweb`
     - `dig`
   - For tools installed via Go (like `nuclei`), ensure `$HOME/go/bin` is in your `PATH` or move the binary to `/usr/local/bin`.

5. **Ollama Setup:**
   - VulnForge uses Ollama for model serving to optimize resource utilization.
   - Ensure Ollama is installed and running on your system.
   - The main model used is `deepseek-coder`, with `mistral` serving as the assistant model.

## Usage

### Basic Reconnaissance
```bash
vulnforge -t example.com -m recon
```

### AI-Autonomous Mode
```bash
vulnforge -t example.com --ai-only
```
This mode enables the AI to:
- Automatically select and install required tools
- Make decisions about which modules to activate
- Sequence attacks based on findings
- Adapt to resistance and try alternate approaches
- Generate comprehensive reports

### Ask AI Questions
```bash
vulnforge ask-ai "What should I do if port 8080 is open?"
```
Options:
- `--verbose`: Show detailed model logs and prompts
- `--dangerous`: Enable dangerous mode (requires `--confirm-danger`)

### Development Mode
```bash
vulnforge --dev-mode
```
Available commands:
- `analyze <module>`: Analyze a module for improvements
- `modify <module> <changes>`: Apply changes to a module
- `list`: Show modification history
- `help`: Show available commands
- `exit`: Exit dev mode

### Tool Management
```bash
# Check and install tools
vulnforge --check

# List custom tools
vulnforge list-tools

# Generate custom tool
vulnforge generate-tool "DNS tunnel for exfiltration"
```

### Debug AI Decisions
```bash
vulnforge -t example.com --ai-only --ai-debug
```
This will show detailed AI reasoning and decision-making process.

### With Stealth Mode
```bash
vulnforge -t example.com -m recon -s
```

## Configuration

- **Config Files Location:** `~/.vulnforge/configs/`
  - `tools.json`: Tool-specific settings
  - `proxies.txt`: List of proxies (optional)
  - `scan_config.json`: Target and scan settings

## Session Data

All session data is stored in:
```
~/.vulnforge/sessions/<target>/<timestamp>/
├── logs/
│   └── ai_controller.log
├── data/
│   └── <step_outputs>.json
├── tools/
├── exploits/
└── report.md
```

## Custom Tools

AI-generated tools are stored in:
```
~/.vulnforge/custom_tools/
├── metadata.json
└── <tool_name>.py
```

## Development

- **Code Style:** Follow PEP 8 guidelines
- **Testing:** Run tests with `pytest`
- **Linting:** Use `pylint` for code quality
- **Formatting:** Use `black` for code formatting

## Requirements

- Python 3.8+
- Kali Linux (recommended)
- All required tools installed and in your `PATH`
- Ollama installed and running for model serving

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Disclaimer

This tool is for educational purposes and authorized security testing only. Always obtain proper authorization before testing any system.

## License

MIT License - See LICENSE file for details 