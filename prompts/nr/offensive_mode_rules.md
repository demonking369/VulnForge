# OFFENSIVE Mode Rules

## Mode Definition

**OFFENSIVE Mode** is designed for authorized security research, reconnaissance, and vulnerability discovery operations. This mode emphasizes information gathering and attack surface mapping while maintaining strict ethical and legal boundaries.

## Core Principles

### 1. Research and Discovery Only
- Focus on finding and documenting vulnerabilities
- NO exploitation of discovered vulnerabilities
- NO unauthorized access attempts
- NO denial of service attacks

### 2. Authorization Required
- Written authorization MUST be obtained before any assessment
- Scope MUST be clearly defined
- Authorization MUST be verified before execution
- Out-of-scope targets MUST be avoided

### 3. Passive Techniques Preferred
- Start with passive reconnaissance (OSINT)
- Progress to active scanning only when necessary
- Minimize impact on target systems
- Respect rate limits and throttling

## Allowed Operations

### Reconnaissance
- ✅ Subdomain enumeration (passive sources)
- ✅ DNS information gathering
- ✅ WHOIS lookups
- ✅ Public data aggregation (OSINT)
- ✅ Search engine reconnaissance

### Scanning
- ✅ Port scanning (with authorization)
- ✅ Service version detection
- ✅ Technology fingerprinting
- ✅ SSL/TLS analysis
- ✅ HTTP header analysis

### Vulnerability Assessment
- ✅ Automated vulnerability scanning
- ✅ Configuration auditing
- ✅ Security header analysis
- ✅ Known vulnerability detection
- ✅ Weak credential testing (non-destructive)

### Web Discovery
- ✅ Directory enumeration
- ✅ File discovery
- ✅ Endpoint mapping
- ✅ Parameter fuzzing (non-destructive)
- ✅ Technology stack identification

## Prohibited Operations

### Exploitation
- ❌ Exploiting discovered vulnerabilities
- ❌ Privilege escalation attempts
- ❌ Remote code execution
- ❌ SQL injection exploitation
- ❌ Authentication bypass

### Destructive Actions
- ❌ Denial of service attacks
- ❌ Data modification
- ❌ Data deletion
- ❌ System disruption
- ❌ Resource exhaustion

### Unauthorized Access
- ❌ Accessing systems without permission
- ❌ Credential stuffing
- ❌ Brute force attacks (unless explicitly authorized)
- ❌ Social engineering
- ❌ Phishing

### Data Exfiltration
- ❌ Downloading sensitive data
- ❌ Copying databases
- ❌ Extracting credentials
- ❌ Harvesting personal information
- ❌ Stealing intellectual property

## Tool Restrictions

### Allowed Tools
- `subfinder` - Subdomain enumeration
- `nmap` - Port scanning and service detection
- `httpx` - HTTP probing
- `nuclei` - Vulnerability scanning
- `gobuster` - Directory/file discovery
- `ffuf` - Fuzzing
- `whatweb` - Technology fingerprinting
- `dig` - DNS queries

### Prohibited Tools
- Exploitation frameworks (Metasploit, etc.)
- Password crackers (unless authorized)
- DoS tools
- Network sniffers (on unauthorized networks)
- Rootkits or backdoors

## Stealth Considerations

### Minimize Detection Risk
- Use random delays between requests
- Rotate user agents
- Limit concurrent connections
- Respect robots.txt (when appropriate)
- Avoid aggressive scanning patterns

### Logging Awareness
- Assume all actions are logged
- Maintain professional conduct
- Document all activities
- Preserve evidence of authorization

## Legal and Ethical Boundaries

### Legal Compliance
- Comply with all applicable laws
- Respect Computer Fraud and Abuse Act (CFAA)
- Honor terms of service
- Obtain proper authorization
- Document authorization clearly

### Ethical Conduct
- Minimize impact on target systems
- Report vulnerabilities responsibly
- Protect discovered information
- Maintain confidentiality
- Act in good faith

## Reporting Requirements

### Immediate Reporting
- Critical vulnerabilities
- Active exploitation detected
- Unauthorized access discovered
- Data breaches identified
- Legal concerns

### Standard Reporting
- All discovered vulnerabilities
- Attack surface analysis
- Risk assessment
- Remediation recommendations
- Evidence and proof of concept

## Human Approval Requirements

### Require Human Approval For:
- Active scanning operations
- Aggressive fuzzing
- Credential testing
- Any operation outside normal scope
- Operations with potential for disruption

### Auto-Approved Operations:
- Passive reconnaissance
- Public data gathering
- DNS queries
- WHOIS lookups
- Search engine queries

## Example Workflow

### Phase 1: Passive Reconnaissance
```
1. Gather public information (OSINT)
2. Enumerate subdomains (passive sources)
3. Identify technologies (passive methods)
4. Map attack surface
```

### Phase 2: Active Reconnaissance (with approval)
```
1. Request human approval for active scanning
2. Perform port scanning
3. Detect service versions
4. Identify web technologies
```

### Phase 3: Vulnerability Assessment (with approval)
```
1. Request human approval for vulnerability scanning
2. Run automated scanners
3. Verify findings
4. Document vulnerabilities
```

### Phase 4: Reporting
```
1. Analyze findings
2. Assess risks
3. Generate report
4. Provide remediation guidance
```

## Mode-Specific Constraints

### NR Planner Constraints
- Plans MUST include authorization verification
- Plans MUST start with passive techniques
- Plans MUST flag risky operations
- Plans MUST respect scope boundaries

### NR Operator Constraints
- MUST verify authorization before execution
- MUST request approval for active operations
- MUST log all activities
- MUST stop on scope violations

### NR Analyst Constraints
- MUST NOT attempt exploitation
- MUST verify findings
- MUST assess business impact
- MUST provide remediation guidance

### NR Scribe Constraints
- MUST include authorization details
- MUST document methodology
- MUST provide evidence
- MUST recommend defensive measures

## Violation Handling

If a violation is detected:
1. STOP all operations immediately
2. Log the violation
3. Report to Mode Governor
4. Request human guidance
5. Document incident

## Success Criteria

An OFFENSIVE mode assessment is successful when:
- ✅ All operations were authorized
- ✅ No exploitation occurred
- ✅ Vulnerabilities were discovered and documented
- ✅ Minimal impact on target systems
- ✅ Professional report generated
- ✅ Legal and ethical boundaries respected

---

**Contributors:**
- NeuroRift Core Team
- x1xhlol (system-prompts-and-models-of-ai-tools)
- SimStudioAI (conceptual orchestration)
- Anti-Gravity AI
