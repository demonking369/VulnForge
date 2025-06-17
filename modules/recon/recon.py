"""
Reconnaissance Module for VulnForge
Handles target reconnaissance and information gathering
"""

import asyncio
import logging
from pathlib import Path
from typing import Optional, Dict, Any
import subprocess

class ReconModule:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.logger = logging.getLogger(__name__)
        
    async def run(self, target: str, output_dir: Optional[str] = None) -> Dict[str, Any]:
        """
        Run reconnaissance on the target
        
        Args:
            target: Target domain or IP
            output_dir: Optional output directory for results
            
        Returns:
            Dictionary containing reconnaissance results
        """
        self.logger.info(f"Starting reconnaissance on {target}")
        
        # Initialize results dictionary
        results = {
            "target": target,
            "subdomains": [],
            "ports": [],
            "services": [],
            "vulnerabilities": []
        }
        
        try:
            # Run subdomain enumeration
            subdomains = await self._run_subfinder(target)
            results["subdomains"] = subdomains
            
            # Run port scanning
            ports = await self._run_nmap(target)
            results["ports"] = ports
            
            # Run service detection
            services = await self._run_httpx(target, subdomains)
            results["services"] = services
            
            # Run vulnerability scanning
            vulns = await self._run_nuclei(target, services)
            results["vulnerabilities"] = vulns
            
            # Save results if output directory specified
            if output_dir:
                self._save_results(results, output_dir)
                
            return results
            
        except Exception as e:
            self.logger.error(f"Error during reconnaissance: {e}")
            raise
            
    async def _run_subfinder(self, target: str) -> list:
        """Run subfinder for subdomain enumeration"""
        cmd = ["subfinder", "-d", target, "-silent"]
        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await proc.communicate()
            
            if proc.returncode != 0:
                self.logger.error(f"Subfinder error: {stderr.decode()}")
                return []
                
            return stdout.decode().splitlines()
            
        except Exception as e:
            self.logger.error(f"Error running subfinder: {e}")
            return []
            
    async def _run_nmap(self, target: str) -> list:
        """Run nmap for port scanning"""
        cmd = ["nmap", "-sS", "-T4", "--max-retries=1", target]
        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await proc.communicate()
            
            if proc.returncode != 0:
                self.logger.error(f"Nmap error: {stderr.decode()}")
                return []
                
            return stdout.decode().splitlines()
            
        except Exception as e:
            self.logger.error(f"Error running nmap: {e}")
            return []
            
    async def _run_httpx(self, target: str, subdomains: list) -> list:
        """Run httpx for service detection"""
        # Use correct httpx syntax for URL scanning (no flags, just the URL)
        cmd = ["httpx", target]
        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await proc.communicate()
            
            if proc.returncode != 0:
                self.logger.error(f"HTTPx error: {stderr.decode()}")
                return []
                
            return stdout.decode().splitlines()
            
        except Exception as e:
            self.logger.error(f"Error running httpx: {e}")
            return []
            
    async def _run_nuclei(self, target: str, services: list) -> list:
        """Run nuclei for vulnerability scanning"""
        # Get nuclei path
        nuclei_path = str(Path.home() / "go" / "bin" / "nuclei")
        
        # Check if nuclei is installed
        if not Path(nuclei_path).exists():
            self.logger.error("Nuclei is not installed. Please install it using: go install -v github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest")
            return []
            
        # Use correct nuclei syntax for URL scanning
        cmd = [nuclei_path, target, "-severity", "critical,high"]
        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await proc.communicate()
            
            if proc.returncode != 0:
                self.logger.error(f"Nuclei error: {stderr.decode()}")
                return []
                
            return stdout.decode().splitlines()
            
        except Exception as e:
            self.logger.error(f"Error running nuclei: {e}")
            return []
            
    def _save_results(self, results: Dict[str, Any], output_dir: str):
        """Save reconnaissance results to file"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Save as JSON
        import json
        with open(output_path / "recon_results.json", "w") as f:
            json.dump(results, f, indent=2) 