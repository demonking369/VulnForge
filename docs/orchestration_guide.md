# NeuroRift Orchestration Guide

## Overview
NeuroRift now features a powerful Orchestration Layer that integrates various security tools under a unified AI-driven control system.

## Key Components

### 1. Execution Manager
Central engine that handles tool execution, logging, and safety checks.
- **Mode Governor**: Enforces OFFENSIVE vs DEFENSIVE operational modes.
- **Session Awareness**: Tracks all tool outputs within a session.

### 2. AI Agents
- **NRPlanner**: Analyzes the high-level goal and selects appropriate tools.
- **NROperator**: Executes the plan step-by-step, handling errors and approvals.
- **NRAnalyst**: Parses tool outputs to identify vulnerabilities and findings.
- **NRScribe**: Generates professional markdown reports from findings.

### 3. Supported Tools
- **Recon**: amass, masscan, nmap, unicornscan, ike-scan
- **Exploitation**: sqlmap, metasploit (msfconsole), netcat, mitmproxy
- **Monitoring**: wireshark (tshark)

## Usage

### CLI Orchestration Mode
Run NeuroRift in orchestrated mode:

```bash
python3 neurorift_main.py --orchestrated --target example.com --mode offensive
```

### Workflow
1. **Planning**: AI generates a multi-step plan (e.g., Amass -> Masscan -> Nmap -> Sqlmap).
2. **Approval**: You review and approve the plan.
3. **Execution**: Tools run automatically (or semi-automatically).
4. **Analysis**: AI correlates results.
5. **Reporting**: A comprehensive report is generated in `~/.neurorift/results/`.

## Adding New Tools
To add a new tool:
1. Create a wrapper in `modules/tools/wrappers/` inheriting from `BaseTool`.
2. Implement `build_command`, `parse_output`, `validate_input`.
3. Register the tool in `modules/orchestration/execution_manager.py`.

## Safety
- **Defensive Mode**: Blocks tools categorized as OFFENSIVE.
- **Human-in-the-Loop**: Critical steps require user confirmation.
