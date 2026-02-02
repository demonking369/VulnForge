# NeuroRift: Orchestrated Intelligence Mode

## Overview

**NeuroRift** is the next evolution of NeuroRift, featuring an advanced **Orchestrated Intelligence Mode** that coordinates multiple specialized AI agents to perform sophisticated security assessments with unprecedented precision and control.

## Architecture

NeuroRift employs a multi-agent architecture where specialized agents work in concert to plan, execute, analyze, and report on security operations:

```
┌─────────────────────────────────────────────────────────────┐
│                    NeuroRift Orchestrator                  │
│                     (Central Coordinator)                    │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│  NR        │      │  NR        │      │  NR        │
│  Planner     │─────▶│  Operator    │─────▶│  Analyst     │
│              │      │              │      │              │
│ • Planning   │      │ • Execution  │      │ • Analysis   │
│ • Strategy   │      │ • Terminal   │      │ • Risk       │
│ • Tooling    │      │ • Automation │      │ • CVSS       │
└──────────────┘      └──────────────┘      └──────────────┘
                                                    │
                                                    ▼
                                            ┌──────────────┐
                                            │  NR        │
                                            │  Scribe      │
                                            │              │
                                            │ • Reporting  │
                                            │ • Docs       │
                                            │ • Audit      │
                                            └──────────────┘
```

## Agent Roles

### NR Planner
**Strategic Planning & Task Decomposition**

The Planner analyzes security assessment requests and creates detailed execution plans:
- Decomposes complex tasks into atomic steps
- Selects appropriate tools and techniques
- Assesses risks and legal implications
- Outputs deterministic JSON plans

**Capabilities:**
- Task analysis and decomposition
- Tool selection and sequencing
- Resource estimation
- Risk assessment

### NR Operator
**Execution & Terminal Automation**

The Operator executes plans through terminal commands with strict operational discipline:
- Executes security tools via terminal only
- No browser automation without human approval
- Implements retry logic and error handling
- Reports progress in real-time

**Capabilities:**
- Terminal command execution
- Tool invocation (nmap, subfinder, nuclei, etc.)
- Error handling and retries
- Progress reporting

**Constraints:**
- Terminal-only execution
- Human approval required for external actions
- No file modifications outside workspace

### NR Analyst
**Security Analysis & Vulnerability Assessment**

The Analyst transforms raw tool outputs into actionable security intelligence:
- Identifies vulnerabilities and misconfigurations
- Assigns CVSS scores and severity ratings
- Reduces false positives through context analysis
- Correlates findings across multiple tools

**Capabilities:**
- Vulnerability assessment
- CVSS scoring
- False positive reduction
- Attack chain identification

**Frameworks:**
- CVSS 3.1
- OWASP Top 10
- CWE/SANS Top 25
- MITRE ATT&CK

### NR Scribe
**Report Generation & Documentation**

The Scribe transforms analysis into professional, multi-format reports:
- Generates executive summaries
- Creates technical documentation
- Produces audit trails
- Supports multiple output formats

**Capabilities:**
- Multi-format reporting (Markdown, JSON, HTML, PDF)
- Executive summaries
- Technical documentation
- Compliance mapping

## Operational Modes

NeuroRift operates in two strictly separated modes, enforced by the **Mode Governor**:

### OFFENSIVE Mode
**Research & Discovery**

Focus: Finding and documenting vulnerabilities

**Allowed Operations:**
- ✅ Passive reconnaissance (OSINT)
- ✅ Subdomain enumeration
- ✅ Port scanning (with authorization)
- ✅ Vulnerability scanning
- ✅ Web discovery

**Prohibited Operations:**
- ❌ Exploitation
- ❌ Unauthorized access
- ❌ Denial of service
- ❌ Data exfiltration

**Tools:** subfinder, nmap, httpx, nuclei, gobuster, ffuf, whatweb, dig

### DEFENSIVE Mode
**Analysis & Mitigation**

Focus: Analyzing findings and recommending fixes

**Allowed Operations:**
- ✅ Vulnerability analysis
- ✅ Risk assessment
- ✅ Patch recommendations
- ✅ Hardening guidance
- ✅ Compliance mapping

**Prohibited Operations:**
- ❌ Active scanning
- ❌ Reconnaissance
- ❌ Vulnerability discovery
- ❌ Offensive techniques

**Tools:** Analysis tools, configuration auditors, patch validators

## Mode Governor

The Mode Governor enforces strict operational discipline:

- **No Cross-Mode Contamination**: OFFENSIVE and DEFENSIVE modes cannot mix
- **Tool Validation**: Only mode-approved tools can be used
- **Violation Logging**: All violations are logged and reported
- **Mode Switching**: Disabled by default for safety

## Human-in-the-Loop

NeuroRift requires human approval for:
- Browser navigation
- External API calls
- File system modifications outside workspace
- Network requests outside target scope
- Any high-risk operations

**Approval Workflow:**
1. Agent requests approval with detailed justification
2. Terminal displays approval prompt
3. User approves or denies
4. Action logged in audit trail
5. Timeout after 5 minutes (default: deny)

## Task State & Memory

NeuroRift maintains persistent task state:

- **Checkpointing**: Automatic checkpoints every 5 minutes
- **Resume Capability**: Resume interrupted tasks
- **History Tracking**: Complete execution history
- **Context Preservation**: Agent context maintained across sessions

## Usage

### Basic Reconnaissance (OFFENSIVE Mode)

```bash
neurorift --orchestrated --mode offensive -t example.com
```

**What happens:**
1. NR Planner creates reconnaissance plan
2. NR Operator executes tools (subfinder, nmap, nuclei)
3. NR Analyst analyzes findings
4. NR Scribe generates report

### Vulnerability Analysis (DEFENSIVE Mode)

```bash
neurorift --orchestrated --mode defensive --analyze results/scan.json
```

**What happens:**
1. NR Planner creates analysis plan
2. NR Analyst analyzes existing scan results
3. NR Analyst prioritizes vulnerabilities
4. NR Scribe generates remediation guide

### Resume Interrupted Task

```bash
neurorift --resume task_20260124_092347
```

## Configuration

NeuroRift is configured via `configs/neurorift_x_config.json`:

```json
{
  "agents": {
    "planner": { "max_planning_iterations": 3 },
    "operator": { "max_retries": 3 },
    "analyst": { "confidence_threshold": 0.7 }
  },
  "mode_governor": {
    "allow_mode_switching": false,
    "log_violations": true
  },
  "human_in_the_loop": {
    "timeout_seconds": 300,
    "default_on_timeout": "deny"
  }
}
```

## System Prompts

NeuroRift agents are governed by system prompts adapted from the **system-prompts-and-models-of-ai-tools** repository:

- `prompts/vfx/vfx_planner_prompt.md` - Planning methodology (Cursor/Devin AI patterns)
- `prompts/vfx/vfx_operator_prompt.md` - Execution discipline (Devin AI patterns)
- `prompts/vfx/vfx_analyst_prompt.md` - Security analysis framework
- `prompts/vfx/vfx_scribe_prompt.md` - Report generation standards
- `prompts/vfx/offensive_mode_rules.md` - OFFENSIVE mode constraints
- `prompts/vfx/defensive_mode_rules.md` - DEFENSIVE mode constraints

## Example Workflow

### Full OFFENSIVE Assessment

```bash
# Initialize task
neurorift --orchestrated --mode offensive -t example.com

# NR Planner creates plan:
# 1. Passive subdomain enumeration
# 2. HTTP service probing
# 3. Port scanning
# 4. Vulnerability scanning

# NR Operator executes:
# $ subfinder -d example.com -silent
# $ httpx -l subdomains.txt -silent
# $ nmap -sV -T4 -iL live_hosts.txt
# $ nuclei -l live_hosts.txt -silent

# NR Analyst analyzes:
# - 15 vulnerabilities found
# - 3 critical, 5 high, 7 medium
# - CVSS scores assigned
# - False positives filtered

# NR Scribe reports:
# - Executive summary
# - Technical findings
# - Remediation guidance
# - Audit trail
```

## Security & Ethics

NeuroRift enforces strict security and ethical boundaries:

- **Authorization Required**: All operations require verified authorization
- **No Exploitation**: Vulnerability discovery only, no exploitation
- **Legal Compliance**: Respects all applicable laws and regulations
- **Responsible Disclosure**: Encourages responsible vulnerability reporting
- **Audit Trail**: Complete logging of all operations

## Comparison: NeuroRift vs NeuroRift

| Feature | NeuroRift | NeuroRift |
|---------|-----------|-------------|
| AI Mode | Simple Agentic | Multi-Agent Orchestration |
| Agents | 1 (Generic) | 4 (Specialized) |
| Planning | Basic | Strategic (NR Planner) |
| Execution | Mixed | Terminal-Only (NR Operator) |
| Analysis | Basic | Advanced (NR Analyst + CVSS) |
| Reporting | Simple | Professional (NR Scribe) |
| Mode Separation | None | Strict (Mode Governor) |
| Human Approval | Optional | Required for risky ops |
| Task Memory | None | Persistent with checkpoints |
| System Prompts | Generic | Specialized per agent |

## Credits

**Contributors:**
- NeuroRift Core Team
- x1xhlol (system-prompts-and-models-of-ai-tools)
- SimStudioAI (conceptual orchestration)
- Anti-Gravity AI

## License

NeuroRift inherits the MIT license from NeuroRift.

## Disclaimer

NeuroRift is designed for **authorized security testing only**. Users must obtain explicit written permission before testing any systems. The developers are not liable for misuse.

---

**Built with ❤️ and ☕ by the NeuroRift Team**
