# VulnForge Robin Report

## Target
- Type: domain
- Value: example.com

## Findings
- Leak Type: credentials
- Source: darkweb forum
- First Seen: 2024-08-01
- Last Seen: 2024-08-15
- Raw Snippet:
```
user: demo@example.com
pass: SuperSecret!
```
- Structured Fields:
  - email: demo@example.com
  - password_present: true
  - services: MegaCorp VPN

## Notes
Suspected credential dump referencing MegaCorp VPN.
