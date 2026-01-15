# �️ VulnForge: AI-Augmented Security Research Framework

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/platform-linux-lightgrey)]()
[![Status](https://img.shields.io/badge/status-active-success)]()

> **"In the realm of cybersecurity, knowledge is power, and VulnForge is your sword."**


> [!IMPORTANT]
> **🚧 THIS PROJECT IS CURRENTLY IN ACTIVE DEVELOPMENT (BETA Phase) 🚧**
>
> While the core features are functional, you may encounter bugs or incomplete features. We are actively shaping the future of this tool and **NEED YOUR HELP!**
>
> **We are looking for contributors!** Whether you're a developer, security researcher, or documentation wizard, check out the [Contributing](#-community--support) section to join the mission.

---

## 📖 Table of Contents
- [Overview](#-overview)
- [Architecture](#-architecture)
- [Key Features](#-key-features)
- [Visual Tour](#-visual-tour)
- [Installation Guide](#-installation-guide)
- [Usage Manual](#-usage-manual)
- [Configuration](#-configuration)
- [Disclaimer](#-legal-disclaimer)

---

## 🔭 Overview

**VulnForge** is an enterprise-grade security testing framework designed for authorized penetration testers, bug bounty hunters, and security researchers. Unlike traditional tools, VulnForge leverages **Local Large Language Models (LLMs)** to act as an autonomous reasoning engine, capable of planning complex security tasks, analyzing scan results for context-aware risks, and interacting with the user through a natural language interface.

The framework unifies industry-standard tools (`nmap`, `nuclei`, `subfinder`) into a cohesive, modular platform accessible via a modern Web Dashboard or a powerful Command Line Interface (CLI).

---

## 🏗️ Architecture

VulnForge is built on a modular Python architecture that separates core logic, tool execution, and AI reasoning.

```mermaid
graph TD
    User[User / Security Researcher] -->|Interacts| Dashboard[Web Dashboard (Streamlit)]
    User -->|Commands| CLI[CLI Interface]
    
    Dashboard & CLI --> Controller[Core Controller]
    
    Controller --> AI[AI Orchestrator (Ollama)]
    Controller --> Recon[Recon Module]
    Controller --> DarkWeb[Dark Web Module (Robin)]
    Controller --> Scanning[Scanning Module]
    
    Recon --> Tools((External Tools))
    Scanning --> Tools
    
    Tools -->|Subfinder| Subdomains[Subdomains]
    Tools -->|Nmap| Ports[Port Data]
    Tools -->|Nuclei| Vulns[Vulnerabilities]
    
    DarkWeb -->|Tor| Onion[Onion Sites]
    
    AI -->|Analyzes| Reports[Intelligence Reports]
```

---

## 🚀 Key Features

### 1. **Autonomous AI Agent**
*   **Web-Connected Reasoning**: The AI can browse the internet (via DuckDuckGo) to validate findings against the latest CVEs and exploit databases in real-time.
*   **Agentic Planning**: In `Agentic Mode`, the AI autonomously formulates multi-step execution plans based on high-level user intents (e.g., "Find all login pages and check for default creds").
*   **Contextual Analysis**: Goes beyond static rule matching by analyzing vulnerability context to reduce false positives.

### 2. **Dark Web Intelligence (Robin Integration)**
*   **Tor-Native**: Built-in routing via Tor SOCKS proxy for safe interaction with `.onion` services.
*   **Semantic Search**: Uses AI to refine search queries and filter results, isolating high-value intelligence from noise.
*   **Automated Scraping**: Safely extracts and summarizes content from hidden services for offline analysis.

### 3. **Advanced Reconnaissance Engine**
*   **Full-Spectrum Discovery**: Automated workflow chaining subdomain enumeration (`subfinder`), port scanning (`nmap`), and technology profiling (`whatweb`).
*   **Vulnerability Assessment**: Integrated `nuclei` scanning for rapid identification of known security flaws.
*   **Stealth Mode**: Configurable rate limiting and passive scan options to minimize detection risk.

---

## 📸 Visual Tour

### **The Command Center (Web Dashboard)**
The centralized hub for all your security operations. Monitor active scans, view system health, and access all modules.
> *[PLACEHOLDER: Insert screenshot of the main Dashboard Overview here]*
> *Recommended size: 1200x800px*

### **AI Security Assistant**
Interact naturally with the framework. Ask questions, request scans, and toggle "Web Search" for real-time internet data.
> *[PLACEHOLDER: Insert screenshot of the AI Chat Interface showing Web Search toggle]*
> *Recommended size: 800x600px*

### **Dark Web Investigation**
Search, filter, and analyze dark web findings in a secure, isolated environment.
> *[PLACEHOLDER: Insert screenshot of the Dark Web / Robin module interface]*
> *Recommended size: 1200x800px*

---

## 📦 Installation Guide

### **Prerequisites**
*   **Operating System**: Linux (Kali Linux or Ubuntu 22.04+ recommended)
*   **Python**: Version 3.10 or higher
*   **Tor**: Required for Dark Web functionality
    ```bash
    sudo apt update && sudo apt install tor -y
    sudo systemctl enable --now tor
    ```
*   **Ollama**: Required for AI features. [Download Ollama](https://ollama.com).

### **Step-by-Step Setup**

1.  **Clone the Repository**
    Get the latest stable version of VulnForge.
    ```bash
    git clone https://github.com/demonking369/VulnForge.git
    cd VulnForge
    ```

2.  **Run the Installer**
    Our automated script handles dependency management and tool installation.
    ```bash
    bash install_script.sh
    ```

3.  **Prepare AI Models**
    Pull the recommended models for optimal performance.
    ```bash
    ollama pull llama3.2    # Recommended balanced model
    ollama pull deepseek-r1 # Excellent for reasoning tasks
    ```

---

## � Usage Manual

### **Mode A: Web Dashboard (Recommended)**
The ideal experience for visual analysis and reporting.
```bash
vulnforge --webmod
```
*   **Access**: Open your browser to `http://localhost:8501`
*   **Features**: Full graphical control over all modules, real-time logs, and interactive reports.

### **Mode B: Command Line Interface (CLI)**
For rapid, headless execution and scripting.

**Standard Recon Scan:**
```bash
vulnforge -t example.com --mode recon
```

**Agentic Mode (Autonomous):**
Delegate the planning to the AI.
```bash
vulnforge --agentic -t example.com --intent "Check for exposed admin panels"
```

**Dark Web Search:**
```bash
vulnforge --darkweb --query "leaked credentials example.com"
```

---

## 🔧 Configuration

VulnForge utilizes a centralized `.env` file for configuration.

| Variable | Description | Default |
| :--- | :--- | :--- |
| `AI_ENABLED` | Master switch for AI features | `true` |
| `OLLAMA_MAIN_MODEL` | Primary LLM for complex reasoning | `llama3.2` |
| `OLLAMA_ASSISTANT_MODEL` | Faster LLM for chat interactions | `llama3.2` |
| `ROBIN_TOR_PROXY` | SOCKS proxy for Dark Web traffic | `socks5h://127.0.0.1:9050` |
| `LOG_LEVEL` | Application logging verbosity | `INFO` |

---

## ⚠️ Legal Disclaimer

**VulnForge is purpose-built for AUTHORIZED security testing, red teaming, and educational research.**

*   **Authorization Required**: You must have explicit, written permission from the owner of any system you scan or test.
*   **Compliance**: Users are responsible for complying with all applicable local, state, and federal laws.
*   **Liability**: The developers and contributors of VulnForge are not liable for any misuse, damage, or illegal activities resulting from the use of this software.

---

## 🤝 Community & Support

> **🙌 Call for Contributors:**
> We need passionate developers to help take VulnForge to the next level!
> *   **Refining AI Prompts**: Help make the agent smarter.
> *   **frontend**: Improve the Streamlit dashboard.
> *   **Testing**: Report bugs and verify fixes.
>
> **Pull Requests are highly encouraged!**

*   **GitHub Issues**: [Report Bugs & Request Features](https://github.com/demonking369/VulnForge/issues)
*   **Community**: Join the discussion on [Reddit](https://reddit.com/r/Linux_369)
*   **Contributing**: PRs are welcome! Please read `CONTRIBUTING.md` before submitting.

---

**Built with ❤️ and ☕ by the VulnForge Team**
