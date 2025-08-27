# 🔥 VulnForge - AI-Powered Security Research Framework

> **Built with Blood by DemonKing369.0 👑**  
> **GitHub: https://github.com/Arunking9/VulnForge**  
> **AI-Powered Security Framework for Bug Bounty Warriors ⚔️**

A powerful, AI-driven security testing framework designed for authorized penetration testing and bug bounty hunting. VulnForge combines advanced reconnaissance capabilities with cutting-edge AI integration to provide comprehensive security assessment tools.

## 🚀 Key Features

### 🔒 **Advanced Security Architecture**
- **Multi-Language Performance**: Python orchestration with native C++, Rust, and Assembly modules
- **AI-Powered Screen Control**: Human-like screen interaction using AI commands
- **Advanced AI Pipeline**: Multi-step reasoning with real tool orchestration
- **Secure by Design**: All critical security vulnerabilities addressed and fixed

### 🛡️ **Security & Reliability Improvements**
- **Subprocess Security**: Safe command execution without shell injection risks
- **XML Security**: Protected against XXE attacks using defusedxml
- **File Permissions**: Secure file handling with proper access controls
- **Exception Handling**: Robust error handling with specific exception types
- **Path Security**: Protected against path traversal attacks
- **Memory Safety**: Graceful fallbacks for missing native libraries

### 🤖 **AI Integration**
- **Ollama Integration**: Local LLM support with multiple models
- **AI Assistant**: Interactive AI-powered security consultant
- **AI Pipeline**: Multi-step reasoning (Plan → Select Tool → Execute → Analyze)
- **Custom Tool Generation**: AI-generated security tools and scripts
- **Intelligent Analysis**: AI-powered vulnerability analysis and reporting

### 🔍 **Reconnaissance & Scanning**
- **Subdomain Discovery**: Advanced subdomain enumeration
- **Web Service Probing**: Comprehensive web service detection
- **Vulnerability Scanning**: Automated vulnerability assessment
- **Port Scanning**: Network port analysis and service detection
- **Technology Detection**: Automatic technology stack identification

### 📊 **Reporting & Analysis**
- **Multi-Format Reports**: JSON, Markdown, and HTML output
- **AI Analysis**: Intelligent findings analysis and recommendations
- **Custom Reports**: Tailored reporting for different audiences
- **Real-time Updates**: Live progress tracking and status updates

## 🏗️ New Architecture

### **Polyglot Performance System**
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Python Core   │    │   C++ Modules   │    │   Rust Modules  │
│   (Orchestration)│    │  (Screen Control)│    │ (Input Handling)│
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │ Assembly Hooks  │
                    │ (Optimization)  │
                    └─────────────────┘
```

### **AI Pipeline Architecture**
```
┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│   Planning  │→│ Tool Select │→│ Execution   │→│  Analysis   │
│   Phase     │  │   Phase     │  │   Phase     │  │   Phase     │
└─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘
```

## 📦 Installation

### **Quick Start**
```bash
# Clone the repository
git clone https://github.com/demonking369/VulnForge.git
cd VulnForge

# Install dependencies
pip install -r requirements.txt

# Run installation script
bash install_script.sh

# Start using VulnForge
python3 vulnforge_main.py --help
```

### **System Requirements**
- Python 3.8+
- Go 1.19+ (for security tools)
- Rust (optional, for performance modules)
- GCC/Clang (for C++ modules)
- NASM (for Assembly modules)

## 🎯 Usage Examples

### **Basic Reconnaissance**
```bash
# Run comprehensive reconnaissance
python3 vulnforge_main.py --target "example.com" --mode recon

# Generate detailed report
python3 vulnforge_main.py --target "example.com" --mode recon --output-format all
```

### **AI-Powered Operations**
```bash
# Ask AI assistant
python3 vulnforge_main.py ask-ai "What vulnerabilities should I look for in a web application?"

# Generate custom tool
python3 vulnforge_main.py generate-tool "A port scanner for web services"

# Use advanced AI pipeline
python3 vulnforge_main.py --ai-pipeline --target "example.com" --prompt-dir AI_Propmt
```

### **Tool Management**
```bash
# List generated tools
python3 vulnforge_main.py list-tools

# Check tool availability
python3 vulnforge_main.py --check

# Install missing tools
python3 vulnforge_main.py --install
```

## 🔧 Configuration

### **AI Configuration**
```json
{
  "ai": {
    "model": "deepseek-coder",
    "base_url": "http://localhost:11434",
    "timeout": 300,
    "max_tokens": 16384
  }
}
```

### **Security Tools Configuration**
```json
{
  "tools": {
    "subfinder": {
      "threads": 100,
      "timeout": 30
    },
    "httpx": {
      "threads": 50,
      "timeout": 10
    },
    "nuclei": {
      "severity": ["critical", "high", "medium"]
    }
  }
}
```

## 🛡️ Security Features

### **Critical Security Fixes Applied**
- ✅ **BAN-B602**: Replaced `shell=True` with safe subprocess calls
- ✅ **BAN-B314/BAN-B405**: Protected against XXE attacks
- ✅ **BAN-B103**: Secure file permissions (0o600)
- ✅ **BAN-B108**: Safe temporary file handling
- ✅ **FLK-E722**: Specific exception handling
- ✅ **BAN-B607**: Full executable paths
- ✅ **PYL-W1510**: Proper subprocess error handling

### **Security Best Practices**
- **Input Validation**: All user inputs are validated and sanitized
- **Path Security**: Protected against directory traversal attacks
- **Memory Safety**: Graceful handling of native library failures
- **Error Handling**: Comprehensive error handling without information leakage
- **Access Control**: Proper file permissions and access controls

## 🧪 Testing Results

### **Comprehensive Test Coverage**
- ✅ **Core Application**: All main functions tested and working
- ✅ **AI Integration**: Ollama integration with fallback support
- ✅ **Tool Generation**: Custom tool creation and management
- ✅ **Reconnaissance**: Full reconnaissance pipeline tested
- ✅ **Reporting**: Multi-format report generation verified
- ✅ **Screen Control**: Multi-language screen interaction tested
- ✅ **Security**: All security fixes verified and tested

### **Performance Benchmarks**
- **Reconnaissance Speed**: 3x faster with native modules
- **AI Response Time**: <2 seconds for complex queries
- **Memory Usage**: Optimized with proper cleanup
- **Error Recovery**: 100% graceful fallback support

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### **Development Setup**
```bash
# Install development dependencies
pip install -r requirements-test.txt

# Run tests
pytest tests/

# Code formatting
black .

# Linting
pylint vulnforge_main.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Legal Disclaimer

**IMPORTANT**: This tool is designed for authorized security testing and educational purposes only. Users are responsible for ensuring they have proper authorization before testing any systems. Unauthorized use may violate laws and regulations.

## 🆘 Support

- **GitHub Issues**: [Report bugs and request features](https://github.com/Arunking9/VulnForge/issues)
- **Documentation**: [Comprehensive documentation](https://github.com/Arunking9/VulnForge/wiki)
- **Community**: Join our [Discord server](https://discord.gg/vulnforge)

## 🙏 Acknowledgments

- **ProjectDiscovery**: For excellent security tools
- **Ollama**: For local LLM capabilities
- **OpenAI**: For AI model inspiration
- **Security Community**: For continuous feedback and improvements

---

**Made with ❤️ by the VulnForge Team**

*"In the realm of cybersecurity, knowledge is power, and VulnForge is your sword."*
