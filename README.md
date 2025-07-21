# VulnForge

An AI-powered vulnerability research framework for authorized security testing and bug bounty hunting.

## Features

- **AI-Autonomous Operation**
  - Fully autonomous mode with `--ai-only` flag
  - AI-driven decision making for tool selection and attack sequencing
  - Real-time analysis and adaptation based on scan results
  - Automatic tool installation and updates
  - Detailed decision logging and reasoning
  - Ollama integration for efficient model serving

- **Reconnaissance Module**
  - Subdomain discovery using multiple tools
  - Port scanning with stealth options
  - Web service enumeration
  - Vulnerability scanning
  - AI-powered analysis
  - Stealth mode with request delays and user agent rotation

- **Stealth Capabilities**
  - Random delays between requests
  - User agent rotation
  - Proxy support
  - Human-like behavior simulation
  - Configurable stealth levels

- **Reporting**
  - Markdown reports with detailed findings
  - JSON output for programmatic analysis
  - HTML reports with visualizations
  - AI-powered analysis and recommendations
  - Customizable report templates

- **Notification System**
  - Multi-channel alerts (Email, Discord, Webhooks)
  - Severity levels (info, warning, high, critical)
  - Customizable notification settings
  - Asynchronous notification processing
  - Rate limiting and retry mechanisms

- **AI Assistant**
  - Interactive AI queries with `ask-ai` command
  - Context-aware responses
  - Security-focused guidance
  - Tool recommendations
  - Debug mode for AI decision transparency

- **Custom Tool Generation**
  - AI-powered tool creation
  - Automatic script generation
  - Tool metadata tracking
  - Success rate monitoring
  - Tool listing and management

- **Development Mode**
  - AI-assisted code improvements
  - Live module modifications
  - Modification history tracking
  - Backup and revert capabilities
  - Interactive development shell

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
   pip install -r requirements-test.txt  # For development
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
   - VulnForge uses Ollama for model serving to optimize resource utilization
   - Ensure Ollama is installed and running on your system
   - The main model used is `deepseek-coder`, with `mistral` serving as the assistant model
   - Models are automatically downloaded on first run

   **AI Models Used:**
   - **Primary Model**: `deepseek-coder-v2:16b-lite-base-q4_0`
     - 16B parameter model optimized for code understanding and generation
     - Used for code generation, analysis, and security tasks
     - Quantized for efficient resource usage
   - **Assistant Model**: `mistral:7b-instruct-v0.2-q4_0`
     - 7B parameter model based on Mistral architecture
     - Used for general queries and security guidance
     - Provides context-aware responses and tool recommendations

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

### Running Tests
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_ai_features.py

# Run with coverage
pytest --cov=.
```

### Code Quality
```bash
# Format code
black .

# Lint code
pylint vulnforge_main.py
```

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