#!/usr/bin/env python3
"""
VulnForge Enhanced Reconnaissance Module
Handles automated reconnaissance with AI-powered analysis
"""

import asyncio
import json
import logging
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Any
import aiofiles
import aiohttp
from datetime import datetime
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn


class EnhancedReconModule:
    def __init__(
        self, base_dir: Path = None, ai_analyzer: Any = None, config_path: str = None
    ):
        """Initialize the reconnaissance module."""
        self.config = {
            "subfinder": {
                "sources": ["bevigil", "binaryedge", "bufferover", "c99", "censys"],
                "timeout": 30,
            },
            "nmap": {
                "default_flags": ["-sS", "-T4", "--max-retries=1"],
                "stealth_flags": ["-sS", "-T2", "-f"],
                "aggressive_flags": ["-sS", "-T5", "-A"],
            },
            "httpx": {"threads": 50, "timeout": 10, "follow_redirects": True},
        }

        self.base_dir = base_dir or Path.cwd()
        self.ai_analyzer = ai_analyzer
        self.logger = logging.getLogger(__name__)
        self.console = Console()

        if config_path:
            try:
                with open(config_path, "r") as f:
                    user_config = json.load(f)
                    # Deep merge user config with defaults
                    self.config = self._deep_merge(self.config, user_config)
            except Exception as e:
                self.logger.warning(f"Failed to load config from {config_path}: {e}")

    def _deep_merge(self, default, user):
        """Deep merge two dictionaries."""
        result = default.copy()
        for key, value in user.items():
            if (
                key in result
                and isinstance(result[key], dict)
                and isinstance(value, dict)
            ):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        return result

    async def run_command(self, cmd: List[str], timeout: int = 300) -> str:
        """Run shell command asynchronously"""
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await asyncio.wait_for(
                process.communicate(), timeout=timeout
            )
            return stdout.decode().strip()
        except asyncio.TimeoutError:
            self.logger.error(f"Command timed out: {' '.join(cmd)}")
            return ""
        except Exception as e:
            self.logger.error(f"Error running command: {e}")
            return ""

    async def discover_subdomains(self, domain: str) -> List[str]:
        """Discover subdomains using subfinder"""
        self.console.print("[bold blue]Discovering subdomains...[/bold blue]")
        sources = self.config["subfinder"]["sources"]
        cmd = ["subfinder", "-d", domain, "-sources", ",".join(sources), "-silent"]
        output = await self.run_command(cmd)
        if not output:
            self.logger.warning(
                f"No output from subfinder for {domain}. Check if subfinder is installed and configured correctly."
            )
            self.console.print(
                f"[yellow]Warning: No output from subfinder for {domain}. Check if subfinder is installed and configured correctly.[/yellow]"
            )
        subdomains = [line.strip() for line in output.splitlines() if line.strip()]
        self.console.print(f"[green]Found {len(subdomains)} subdomains[/green]")
        if len(subdomains) == 0:
            self.logger.warning(
                f"No subdomains found for {domain}. Check subfinder installation, network, and API keys."
            )
            self.console.print(
                f"[yellow]Warning: No subdomains found for {domain}. Check subfinder installation, network, and API keys.[/yellow]"
            )
        return subdomains

    async def probe_web_services(self, subdomains: List[str]) -> List[Dict]:
        """Probe discovered subdomains for web services"""
        self.console.print("[bold blue]Probing web services...[/bold blue]")

        # Save subdomains to temporary file
        temp_file = self.base_dir / "temp_subdomains.txt"
        async with aiofiles.open(temp_file, "w") as f:
            await f.write("\n".join(subdomains))

        # Run httpx
        cmd = [
            "httpx",
            "-l",
            str(temp_file),
            "-silent",
            "-json",
            "-status-code",
            "-title",
            "-tech-detect",
            "-t",
            str(self.config["httpx"]["threads"]),
            "-timeout",
            str(self.config["httpx"]["timeout"]),
        ]

        output = await self.run_command(cmd)
        results = []

        for line in output.splitlines():
            try:
                result = json.loads(line)
                results.append(
                    {
                        "url": result.get("url", ""),
                        "status_code": result.get("status-code", 0),
                        "title": result.get("title", ""),
                        "technologies": result.get("technologies", []),
                    }
                )
            except:
                continue

        # Cleanup
        temp_file.unlink(missing_ok=True)

        self.console.print(f"[green]Found {len(results)} web services[/green]")
        return results

    async def scan_vulnerabilities(self, web_services: List[Dict]) -> List[Dict]:
        """Scan web services for vulnerabilities using nuclei"""
        self.console.print("[bold blue]Scanning for vulnerabilities...[/bold blue]")

        # Save URLs to temporary file
        temp_file = self.base_dir / "temp_urls.txt"
        async with aiofiles.open(temp_file, "w") as f:
            await f.write("\n".join(service["url"] for service in web_services))

        # Run nuclei
        cmd = [
            "nuclei",
            "-l",
            str(temp_file),
            "-json",
            "-severity",
            ",".join(self.config["nuclei"]["severity"]),
            "-silent",
        ]

        output = await self.run_command(cmd)
        vulnerabilities = []

        for line in output.splitlines():
            try:
                vuln = json.loads(line)
                vulnerabilities.append(
                    {
                        "url": vuln.get("url", ""),
                        "type": vuln.get("type", ""),
                        "severity": vuln.get("severity", ""),
                        "description": vuln.get("description", ""),
                        "template": vuln.get("template", ""),
                    }
                )
            except:
                continue

        # Cleanup
        temp_file.unlink(missing_ok=True)

        self.console.print(
            f"[green]Found {len(vulnerabilities)} potential vulnerabilities[/green]"
        )
        return vulnerabilities

    async def run_recon(
        self, target: str, output_dir: Optional[Path] = None
    ) -> Dict[str, Any]:
        """Run complete reconnaissance on target concurrently"""
        if not output_dir:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_dir = self.base_dir / "results" / f"{target}_{timestamp}"
        output_dir.mkdir(parents=True, exist_ok=True)

        # Define all reconnaissance tasks
        recon_tasks = [
            self.discover_subdomains(target),
            self.run_port_scan(target),  # Assuming a new async port scan method
            # Add other concurrent tasks here
        ]

        # Run tasks concurrently
        results = await asyncio.gather(*recon_tasks, return_exceptions=True)

        # Process results...
        subdomains = results[0] if not isinstance(results[0], Exception) else []
        port_scan_results = results[1] if not isinstance(results[1], Exception) else {}

        web_services = await self.probe_web_services(subdomains)
        vulnerabilities = await self.scan_vulnerabilities(web_services)

        # Generate AI analysis
        ai_analysis = await self._analyze_results(
            target, subdomains, web_services, vulnerabilities
        )

        # Prepare results
        results = {
            "target": target,
            "timestamp": datetime.now().isoformat(),
            "subdomains": subdomains,
            "web_services": web_services,
            "vulnerabilities": vulnerabilities,
            "ai_analysis": ai_analysis,
        }

        # Save results
        await self._save_results(results, output_dir)

        return results

    async def _analyze_results(
        self,
        target: str,
        subdomains: List[str],
        web_services: List[Dict],
        vulnerabilities: List[Dict],
    ) -> Dict:
        """Analyze results using AI"""
        self.console.print("[bold blue]Analyzing results with AI...[/bold blue]")

        # Prepare data for AI analysis
        analysis_data = {
            "target": target,
            "subdomain_count": len(subdomains),
            "web_service_count": len(web_services),
            "vulnerability_count": len(vulnerabilities),
            "critical_findings": [],
            "recommendations": [],
        }

        # Analyze vulnerabilities
        if vulnerabilities:
            vuln_summary = "\n".join(
                [
                    f"- {v['type']} ({v['severity']}): {v['description']}"
                    for v in vulnerabilities
                ]
            )

            prompt = f"""
            Analyze these security findings for {target}:
            
            {vuln_summary}
            
            Provide:
            1. Critical findings that need immediate attention
            2. Recommended next steps for exploitation
            3. Potential attack chains
            """

            ai_response = self.ai_analyzer.ollama.generate(prompt)
            if ai_response:
                try:
                    analysis = json.loads(ai_response)
                    analysis_data.update(analysis)
                except:
                    # If JSON parsing fails, use raw response
                    analysis_data["raw_analysis"] = ai_response

        return analysis_data

    async def _save_results(self, results: Dict, output_dir: Path):
        """Save results in multiple formats"""
        # Save JSON
        json_path = output_dir / "results.json"
        async with aiofiles.open(json_path, "w") as f:
            await f.write(json.dumps(results, indent=2))

        # Generate Markdown report
        md_path = output_dir / "report.md"
        async with aiofiles.open(md_path, "w") as f:
            await f.write(
                f"""# VulnForge Reconnaissance Report

## Target: {results['target']}
## Scan Time: {results['timestamp']}

### Summary
- Subdomains Found: {len(results['subdomains'])}
- Web Services: {len(results['web_services'])}
- Vulnerabilities: {len(results['vulnerabilities'])}

### Subdomains
{chr(10).join(f'- {subdomain}' for subdomain in results['subdomains'])}

### Web Services
{chr(10).join(f'- {service["url"]} ({service["status_code"]})' for service in results['web_services'])}

### Vulnerabilities
{chr(10).join(f'- {vuln["type"]} ({vuln["severity"]}): {vuln["description"]}' for vuln in results['vulnerabilities'])}

### AI Analysis
{json.dumps(results['ai_analysis'], indent=2)}
"""
            )

        self.console.print(f"[green]Results saved to: {output_dir}[/green]")
