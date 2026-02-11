# NeuroRift Agent Roles

## Overview

NeuroRift employs four specialized agents, each with distinct responsibilities and capabilities. This document provides detailed information about each agent role.

---

## NR Planner

**Role:** Strategic Planning & Task Decomposition

### Responsibilities

The Planner is the strategic brain of NeuroRift, responsible for:

1. **Request Analysis**
   - Parse user security assessment requests
   - Identify objectives and success criteria
   - Determine scope and boundaries
   - Assess authorization requirements

2. **Task Decomposition**
   - Break complex tasks into atomic steps
   - Sequence operations logically
   - Identify dependencies between steps
   - Estimate resource requirements

3. **Tool Selection**
   - Select appropriate security tools
   - Validate tool availability
   - Consider stealth and detection risk
   - Optimize for efficiency

4. **Risk Assessment**
   - Evaluate legal and ethical implications
   - Identify potential detection risks
   - Assess impact on target systems
   - Flag high-risk operations

### Capabilities

- Task analysis and decomposition
- Tool selection and sequencing
- Resource estimation
- Risk assessment
- JSON plan generation

### Output Format

The Planner outputs deterministic JSON plans:

```json
{
  "plan_id": "plan_001",
  "objective": "Perform reconnaissance on example.com",
  "mode": "offensive",
  "target": "example.com",
  "steps": [
    {
      "step_id": 1,
      "description": "Enumerate subdomains",
      "tool": "subfinder",
      "requires_human_approval": false
    }
  ]
}
```

### System Prompt

Location: `prompts/vfx/vfx_planner_prompt.md`

Adapted from: Cursor/Devin AI planning patterns

---

## NR Operator

**Role:** Execution & Terminal Automation

### Responsibilities

The Operator is the execution engine, responsible for:

1. **Plan Execution**
   - Execute steps from Planner in sequence
   - Invoke security tools via terminal
   - Capture and structure tool output
   - Report progress and results

2. **Terminal Control**
   - Execute ONLY terminal commands
   - No browser automation without approval
   - No external API calls without permission
   - No file modifications outside workspace

3. **Error Handling**
   - Detect tool failures
   - Implement retry logic (max 3 attempts)
   - Report errors with context
   - Request human intervention when stuck

4. **Human-in-the-Loop**
   - Request approval for risky operations
   - Wait for human confirmation
   - Log all approval requests
   - Timeout handling (default: deny)

### Capabilities

- Terminal command execution
- Tool invocation (nmap, subfinder, nuclei, etc.)
- Error handling and retries
- Progress reporting
- Output structuring

### Constraints

**TERMINAL ONLY:**
- No browser navigation
- No direct HTTP requests (use tools)
- No file modifications outside `~/.neurorift/`
- No system package installation without approval

### Execution Patterns

**Subdomain Enumeration:**
```bash
subfinder -d example.com -silent -o /tmp/subdomains.txt
```

**Port Scanning:**
```bash
nmap -sV -T4 -iL /tmp/live_hosts.txt -oN /tmp/nmap_results.txt
```

**Vulnerability Scanning:**
```bash
nuclei -l /tmp/live_hosts.txt -silent -o /tmp/nuclei_results.json -json
```

### System Prompt

Location: `prompts/vfx/vfx_operator_prompt.md`

Adapted from: Devin AI execution patterns

---

## NR Analyst

**Role:** Security Analysis & Vulnerability Assessment

### Responsibilities

The Analyst is the intelligence engine, responsible for:

1. **Vulnerability Assessment**
   - Analyze tool outputs for security issues
   - Identify vulnerabilities and misconfigurations
   - Correlate findings across multiple tools
   - Reduce false positives

2. **Risk Scoring**
   - Assign CVSS scores to vulnerabilities
   - Consider environmental context
   - Assess exploitability and impact
   - Prioritize findings by severity

3. **Correlation Analysis**
   - Connect related findings
   - Identify attack chains
   - Map vulnerabilities to MITRE ATT&CK
   - Build comprehensive threat picture

4. **Intelligence Generation**
   - Extract actionable insights
   - Identify patterns and trends
   - Highlight critical risks
   - Provide remediation guidance

### Capabilities

- Vulnerability assessment
- CVSS 3.1 scoring
- False positive reduction
- Attack chain identification
- Context-aware analysis

### Frameworks

- **CVSS 3.1**: Common Vulnerability Scoring System
- **OWASP Top 10**: Web application security risks
- **CWE/SANS Top 25**: Common weakness enumeration
- **MITRE ATT&CK**: Adversarial tactics and techniques

### Severity Classification

- **Critical (9.0-10.0)**: Remote code execution, authentication bypass
- **High (7.0-8.9)**: Privilege escalation, significant data exposure
- **Medium (4.0-6.9)**: Information disclosure, configuration weaknesses
- **Low (0.1-3.9)**: Minimal impact, best practice violations

### Output Format

```json
{
  "findings": [
    {
      "finding_id": "VULN-001",
      "title": "Outdated Apache HTTP Server",
      "severity": "high",
      "cvss_score": 7.5,
      "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:N/I:N/A:H",
      "remediation": "Update Apache to version 2.4.54 or later"
    }
  ]
}
```

### System Prompt

Location: `prompts/vfx/vfx_analyst_prompt.md`

Custom security analysis framework

---

## NR Scribe

**Role:** Report Generation & Documentation

### Responsibilities

The Scribe is the documentation engine, responsible for:

1. **Report Generation**
   - Transform analysis into readable reports
   - Create executive summaries
   - Generate technical documentation
   - Produce audit trails

2. **Multi-Format Output**
   - Markdown for readability
   - JSON for automation
   - HTML for presentation
   - PDF for distribution

3. **Audience Adaptation**
   - Executive summaries for management
   - Technical details for security teams
   - Remediation guides for developers
   - Compliance reports for auditors

4. **Documentation**
   - Methodology documentation
   - Evidence preservation
   - Timeline tracking
   - Attribution and credits

### Capabilities

- Multi-format reporting
- Executive summaries
- Technical documentation
- Audit trail generation
- Compliance mapping

### Report Structure

1. **Executive Summary** (1-2 pages)
   - High-level overview
   - Key findings
   - Business impact
   - Recommended actions

2. **Methodology**
   - Assessment scope
   - Tools used
   - Techniques employed
   - Limitations

3. **Findings**
   - Detailed vulnerability descriptions
   - CVSS scores
   - Evidence
   - Remediation steps

4. **Recommendations**
   - Prioritized action items
   - Quick wins
   - Long-term improvements

5. **Appendix**
   - Raw tool outputs
   - Technical details
   - Glossary

### Output Formats

- **Markdown**: Human-readable, version-controllable
- **JSON**: Machine-readable, automation-friendly
- **HTML**: Interactive, filterable, shareable
- **PDF**: Professional, distributable

### System Prompt

Location: `prompts/vfx/vfx_scribe_prompt.md`

Security reporting standards

---

## Agent Communication

### Orchestration Flow

```
User Request
     ↓
NR Planner (Creates plan)
     ↓
NR Operator (Executes plan)
     ↓
NR Analyst (Analyzes results)
     ↓
NR Scribe (Generates report)
     ↓
Final Report
```

### Context Handoffs

Agents communicate through structured context handoffs:

1. **Planner → Operator**: Execution plan (JSON)
2. **Operator → Analyst**: Tool outputs (structured data)
3. **Analyst → Scribe**: Security analysis (findings + recommendations)

### Shared Knowledge

All agents access a shared knowledge base containing:
- Task metadata
- Target information
- Operational mode
- Authorization status
- Environmental context

---

## Mode-Specific Behavior

### OFFENSIVE Mode

**NR Planner:**
- Plans discovery operations
- Selects reconnaissance tools
- Flags risky operations

**NR Operator:**
- Executes scanning tools
- Requests approval for active scans
- Logs all activities

**NR Analyst:**
- Focuses on exploitability
- Identifies attack paths
- Maps attack surface

**NR Scribe:**
- Emphasizes discovered vulnerabilities
- Recommends defensive measures

### DEFENSIVE Mode

**NR Planner:**
- Plans analysis operations
- No active scanning
- Focuses on remediation

**NR Operator:**
- Works with existing data only
- No tool execution
- Validates data sources

**NR Analyst:**
- Prioritizes by business impact
- Recommends practical fixes
- Considers compensating controls

**NR Scribe:**
- Emphasizes remediation
- Provides implementation guides
- Documents defensive measures

---

## Credits

**Contributors:**
- NeuroRift Core Team
- x1xhlol (system-prompts-and-models-of-ai-tools)
- SimStudioAI (conceptual orchestration)
- Anti-Gravity AI
