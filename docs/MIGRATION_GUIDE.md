# Migration Guide: NeuroRift → NeuroRift

## Overview

This guide helps you migrate from NeuroRift's simple agentic mode to NeuroRift's advanced Orchestrated Intelligence Mode.

## Breaking Changes

### 1. Command Line Interface

**Old (NeuroRift):**
```bash
neurorift --agentic -t example.com
```

**New (NeuroRift):**
```bash
neurorift --orchestrated --mode offensive -t example.com
```

### 2. Mode Selection

NeuroRift requires explicit mode selection:
- `--mode offensive` - Research and discovery
- `--mode defensive` - Analysis and mitigation

### 3. Configuration Files

**Old:** No dedicated configuration for agentic mode

**New:** `configs/neurorift_x_config.json` - Comprehensive agent configuration

### 4. System Prompts

**Old:** Single prompt file (`prompts/agentic_system.md`)

**New:** Specialized prompts per agent:
- `prompts/vfx/vfx_planner_prompt.md`
- `prompts/vfx/vfx_operator_prompt.md`
- `prompts/vfx/vfx_analyst_prompt.md`
- `prompts/vfx/vfx_scribe_prompt.md`

## Command Mapping

| NeuroRift Command | NeuroRift Equivalent |
|-------------------|------------------------|
| `--agentic` | `--orchestrated` |
| `-t example.com` | `--mode offensive -t example.com` |
| `--ai-only` | Removed (use `--orchestrated`) |
| `--ai-debug` | `--orchestrated --verbose` |

## Feature Comparison

### Agent Architecture

**NeuroRift:**
- Single generic agent
- Mixed responsibilities
- Basic planning

**NeuroRift:**
- 4 specialized agents (Planner, Operator, Analyst, Scribe)
- Clear separation of concerns
- Strategic planning with NR Planner

### Execution Control

**NeuroRift:**
- Mixed terminal/browser execution
- No strict boundaries
- Optional human approval

**NeuroRift:**
- Terminal-only execution (NR Operator)
- Strict mode enforcement (Mode Governor)
- Required human approval for risky operations

### Analysis Capabilities

**NeuroRift:**
- Basic AI analysis
- Generic vulnerability detection
- Simple reporting

**NeuroRift:**
- Advanced analysis (NR Analyst)
- CVSS scoring
- False positive reduction
- Professional reporting (NR Scribe)

## Migration Steps

### Step 1: Update Commands

Replace all `--agentic` flags with `--orchestrated --mode offensive`:

```bash
# Before
neurorift --agentic -t example.com

# After
neurorift --orchestrated --mode offensive -t example.com
```

### Step 2: Configure Modes

Decide which mode to use for each operation:

**OFFENSIVE Mode** (Discovery):
```bash
neurorift --orchestrated --mode offensive -t example.com
```

**DEFENSIVE Mode** (Analysis):
```bash
neurorift --orchestrated --mode defensive --analyze results/scan.json
```

### Step 3: Review Configuration

Create or update `configs/neurorift_x_config.json`:

```json
{
  "mode_governor": {
    "default_mode": "offensive",
    "allow_mode_switching": false
  },
  "human_in_the_loop": {
    "enabled": true,
    "timeout_seconds": 300
  }
}
```

### Step 4: Update Scripts

If you have automation scripts, update them:

```bash
#!/bin/bash
# Old script
# neurorift --agentic -t $TARGET

# New script
neurorift --orchestrated --mode offensive -t $TARGET
```

## Backward Compatibility

### Legacy Mode Support

The old `--agentic` flag still works but is deprecated:

```bash
# Still works (deprecated)
neurorift --agentic -t example.com

# Equivalent to
neurorift --orchestrated --mode offensive -t example.com
```

**Warning:** Legacy mode will be removed in a future version.

### Configuration Migration

Old agentic mode configurations are automatically migrated:

```python
# Old: prompts/agentic_system.md
# New: prompts/vfx/vfx_planner_prompt.md (and others)
```

## New Features in NeuroRift

### 1. Mode Governor

Enforces strict separation between OFFENSIVE and DEFENSIVE modes:

```python
from modules.ai.mode_governor import ModeGovernor

governor = ModeGovernor()
governor.set_mode("offensive")
governor.validate_tool("nmap")  # ✓ Allowed in OFFENSIVE mode
governor.validate_tool("patch_validator")  # ✗ Not allowed
```

### 2. Task Memory

Persistent task state with checkpoint/resume:

```bash
# Start task
neurorift --orchestrated --mode offensive -t example.com

# Interrupt with Ctrl+C

# Resume later
neurorift --resume task_20260124_092347
```

### 3. Human-in-the-Loop

Required approval for risky operations:

```
NR Operator requests permission to browse: https://example.com
Allow this action? (y/n):
```

### 4. Multi-Format Reporting

Professional reports in multiple formats:

```bash
# Generate all formats
neurorift --orchestrated --mode offensive -t example.com --output-format all

# Outputs:
# - report.md (Markdown)
# - report.json (JSON)
# - report.html (HTML)
# - report.pdf (PDF)
```

## Troubleshooting

### Issue: "Mode not specified"

**Error:**
```
Error: Operational mode required for NeuroRift
```

**Solution:**
Add `--mode offensive` or `--mode defensive`:
```bash
neurorift --orchestrated --mode offensive -t example.com
```

### Issue: "Tool not allowed in mode"

**Error:**
```
ModeViolation: Tool 'nmap' is not allowed in DEFENSIVE mode
```

**Solution:**
Use OFFENSIVE mode for scanning:
```bash
neurorift --orchestrated --mode offensive -t example.com
```

### Issue: "Human approval timeout"

**Error:**
```
Approval request timed out (300s). Action denied.
```

**Solution:**
Increase timeout in configuration:
```json
{
  "human_in_the_loop": {
    "timeout_seconds": 600
  }
}
```

## Best Practices

### 1. Always Specify Mode

Be explicit about operational mode:
```bash
# Good
neurorift --orchestrated --mode offensive -t example.com

# Avoid
neurorift --orchestrated -t example.com  # Uses default mode
```

### 2. Use DEFENSIVE Mode for Analysis

Analyze existing results in DEFENSIVE mode:
```bash
neurorift --orchestrated --mode defensive --analyze results/scan.json
```

### 3. Enable Human Approval

Keep human-in-the-loop enabled for safety:
```json
{
  "human_in_the_loop": {
    "enabled": true
  }
}
```

### 4. Review Violation Logs

Regularly check mode violations:
```bash
cat ~/.neurorift/logs/mode_violations.json
```

## Getting Help

- **Documentation**: `docs/VULNFORGE_X_README.md`
- **Agent Roles**: `docs/AGENT_ROLES.md`
- **GitHub Issues**: https://github.com/demonking369/NeuroRift/issues
- **Community**: https://reddit.com/r/Linux_369

---

**Contributors:**
- NeuroRift Core Team
- x1xhlol (system-prompts-and-models-of-ai-tools)
- SimStudioAI (conceptual orchestration)
- Anti-Gravity AI
