"""
Reconnaissance module for VulnForge
Handles subdomain discovery, port scanning, and service enumeration
"""

import json
import asyncio
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import aiofiles
import aiohttp
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from utils.cli_utils import create_progress, print_results_table
from utils.logger import setup_logger
from utils.stealth_utils import stealth_manager

class ReconModule:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.console = Console()
        self.logger = setup_logger("vulnforge.recon")
        self.config = self._load_config()
        self.session = None
        
    def _load_config(self) -> Dict:
        """Load configuration from config file"""
        config_path = self.base_dir / "configs" / "tools.json"
        try:
            with open(config_path) as f:
                return json.load(f)
        except:
            return {
                "subfinder": {
                    "sources": ["bevigil", "binaryedge", "bufferover", "c99", "censys"],
                    "timeout": 300
                },
                "nmap": {
                    "default_flags": ["-sS", "-T4", "--max-retries=1"],
                    "stealth_flags": ["-sS", "-T2", "-f"],
                    "aggressive_flags": ["-sS", "-T5", "-A"]
                },
                "httpx": {
                    "threads": 50,
                    "timeout": 10,
                    "follow_redirects": True
                }
            }
            
    async def run_command(self, cmd: List[str], timeout: int = 300) -> str:
        """Run shell command asynchronously"""
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=timeout)
            return stdout.decode().strip()
        except asyncio.TimeoutError:
            self.logger.error(f"Command timed out: {' '.join(cmd)}")
            return ""
        except Exception as e:
            self.logger.error(f"Error running command: {e}")
            return ""
            
    async def discover_subdomains(self, domain: str) -> List[str]:
        """Discover subdomains using multiple tools"""
        self.console.print("[bold blue]Discovering subdomains...[/bold blue]")
        
        subdomains = set()
        
        # Use subfinder
        sources = self.config["subfinder"]["sources"]
        cmd = ["subfinder", "-d", domain, "-sources", ",".join(sources), "-silent"]
        output = await self.run_command(cmd)
        subdomains.update(line.strip() for line in output.splitlines() if line.strip())
        
        # Use amass (if available)
        try:
            cmd = ["amass", "enum", "-passive", "-d", domain, "-silent"]
            output = await self.run_command(cmd)
            subdomains.update(line.strip() for line in output.splitlines() if line.strip())
        except:
            pass
            
        # Use assetfinder (if available)
        try:
            cmd = ["assetfinder", "--subs-only", domain]
            output = await self.run_command(cmd)
            subdomains.update(line.strip() for line in output.splitlines() if line.strip())
        except:
            pass
            
        self.console.print(f"[green]Found {len(subdomains)} subdomains[/green]")
        return list(subdomains)
        
    async def scan_ports(self, target: str, mode: str = "default") -> List[Dict]:
        """Scan ports using nmap with stealth options"""
        self.console.print("[bold blue]Scanning ports...[/bold blue]")
        
        flags = self.config["nmap"][f"{mode}_flags"]
        cmd = ["nmap"] + flags + [target, "-oX", "-"]
        
        output = await self.run_command(cmd)
        if not output:
            return []
            
        # Parse nmap XML output
        try:
            import xml.etree.ElementTree as ET
            root = ET.fromstring(output)
            ports = []
            
            for port in root.findall(".//port"):
                port_id = port.get("portid")
                service = port.find("service")
                if service is not None:
                    ports.append({
                        "port": port_id,
                        "protocol": port.get("protocol"),
                        "service": service.get("name"),
                        "version": service.get("version", ""),
                        "state": port.find("state").get("state"),
                        "product": service.get("product", ""),
                        "cpe": service.get("cpe", "")
                    })
                    
            self.console.print(f"[green]Found {len(ports)} open ports[/green]")
            return ports
            
        except Exception as e:
            self.logger.error(f"Error parsing nmap output: {e}")
            return []
            
    async def probe_web_services(self, subdomains: List[str]) -> List[Dict]:
        """Probe discovered subdomains for web services"""
        self.console.print("[bold blue]Probing web services...[/bold blue]")
        
        # Save subdomains to temporary file
        temp_file = self.base_dir / "temp_subdomains.txt"
        async with aiofiles.open(temp_file, 'w') as f:
            await f.write('\n'.join(subdomains))
            
        # Run httpx with enhanced options
        cmd = [
            "httpx",
            "-l", str(temp_file),
            "-silent",
            "-json",
            "-status-code",
            "-title",
            "-tech-detect",
            "-server",
            "-websocket",
            "-tls-probe",
            "-csp-probe",
            "-t", str(self.config["httpx"]["threads"]),
            "-timeout", str(self.config["httpx"]["timeout"])
        ]
        
        output = await self.run_command(cmd)
        results = []
        
        for line in output.splitlines():
            try:
                result = json.loads(line)
                results.append({
                    "url": result.get("url", ""),
                    "status_code": result.get("status-code", 0),
                    "title": result.get("title", ""),
                    "technologies": result.get("technologies", []),
                    "server": result.get("server", ""),
                    "websocket": result.get("websocket", False),
                    "tls": result.get("tls", {}),
                    "csp": result.get("csp", {})
                })
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
        async with aiofiles.open(temp_file, 'w') as f:
            await f.write('\n'.join(service["url"] for service in web_services))
            
        # Run nuclei with enhanced options
        cmd = [
            "nuclei",
            "-l", str(temp_file),
            "-json",
            "-severity", "critical,high,medium",
            "-silent",
            "-stats",
            "-bulk-size", "25",
            "-concurrency", "25"
        ]
        
        output = await self.run_command(cmd)
        vulnerabilities = []
        
        for line in output.splitlines():
            try:
                vuln = json.loads(line)
                vulnerabilities.append({
                    "url": vuln.get("url", ""),
                    "type": vuln.get("type", ""),
                    "severity": vuln.get("severity", ""),
                    "description": vuln.get("description", ""),
                    "template": vuln.get("template", ""),
                    "matcher": vuln.get("matcher", ""),
                    "extracted_results": vuln.get("extracted-results", []),
                    "metadata": vuln.get("metadata", {})
                })
            except:
                continue
                
        # Cleanup
        temp_file.unlink(missing_ok=True)
        
        self.console.print(f"[green]Found {len(vulnerabilities)} potential vulnerabilities[/green]")
        return vulnerabilities
        
    async def run(self, target: str, output_dir: Optional[str] = None) -> Dict[str, Any]:
        """Run complete reconnaissance on target"""
        if not output_dir:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_dir = self.base_dir / "results" / f"{target}_{timestamp}"
        else:
            output_dir = Path(output_dir)
            
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize aiohttp session
        async with aiohttp.ClientSession() as session:
            self.session = session
            
            # Run reconnaissance steps
            subdomains = await self.discover_subdomains(target)
            ports = await self.scan_ports(target, mode="stealth")
            web_services = await self.probe_web_services(subdomains)
            vulnerabilities = await self.scan_vulnerabilities(web_services)
            
            # Prepare results
            results = {
                "target": target,
                "timestamp": datetime.now().isoformat(),
                "subdomains": subdomains,
                "ports": ports,
                "web_services": web_services,
                "vulnerabilities": vulnerabilities,
                "stealth_stats": stealth_manager.get_request_stats()
            }
            
            # Save results
            await self._save_results(results, output_dir)
            
            # Display results
            print_results_table({
                "Subdomains": subdomains,
                "Open Ports": ports,
                "Web Services": web_services,
                "Vulnerabilities": vulnerabilities
            })
            
            return results
            
    async def _save_results(self, results: Dict, output_dir: Path):
        """Save results in multiple formats"""
        # Save JSON
        json_path = output_dir / "results.json"
        async with aiofiles.open(json_path, 'w') as f:
            await f.write(json.dumps(results, indent=2))
            
        # Generate Markdown report
        md_path = output_dir / "report.md"
        async with aiofiles.open(md_path, 'w') as f:
            await f.write(f"""# VulnForge Reconnaissance Report

## Target: {results['target']}
## Scan Time: {results['timestamp']}

### Summary
- Subdomains Found: {len(results['subdomains'])}
- Open Ports: {len(results['ports'])}
- Web Services: {len(results['web_services'])}
- Vulnerabilities: {len(results['vulnerabilities'])}

### Subdomains
{chr(10).join(f'- {subdomain}' for subdomain in results['subdomains'])}

### Open Ports
{chr(10).join(f'- {port["port"]}/{port["protocol"]} ({port["service"]}) - {port.get("version", "Unknown")}' for port in results['ports'])}

### Web Services
{chr(10).join(f'- {service["url"]} ({service["status_code"]}) - {service.get("title", "No Title")}' for service in results['web_services'])}

### Vulnerabilities
{chr(10).join(f'- {vuln["type"]} ({vuln["severity"]}): {vuln["description"]}' for vuln in results['vulnerabilities'])}

### Stealth Statistics
- Total Proxies: {results['stealth_stats']['total_proxies']}
- Request Delay: {results['stealth_stats']['min_delay']}-{results['stealth_stats']['max_delay']}s
- Last Request: {results['stealth_stats']['last_request']}
""")
            
        self.console.print(f"[green]Results saved to: {output_dir}[/green]") 