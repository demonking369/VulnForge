#!/usr/bin/env python3
"""
VulnForge Reconnaissance Script for Bumba Global
"""

import asyncio
import json
import logging
from pathlib import Path
from typing import Dict, List
import aiohttp
import subprocess
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ReconScanner:
    def __init__(self, config_path: Path):
        self.config = self._load_config(config_path)
        self.results = {
            "scan_time": datetime.now().isoformat(),
            "target": self.config["target"],
            "findings": []
        }
        
    def _load_config(self, config_path: Path) -> Dict:
        """Load scan configuration"""
        with open(config_path) as f:
            return json.load(f)
            
    async def run_nmap_scan(self):
        """Run Nmap scan"""
        try:
            cmd = ["nmap"] + self.config["tools"]["nmap"]["flags"] + [self.config["target"]["domain"]]
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                self.results["findings"].append({
                    "tool": "nmap",
                    "output": stdout.decode(),
                    "timestamp": datetime.now().isoformat()
                })
            else:
                logger.error(f"Nmap scan failed: {stderr.decode()}")
                
        except Exception as e:
            logger.error(f"Error running Nmap scan: {e}")
            
    async def run_subfinder(self):
        """Run Subfinder for subdomain enumeration"""
        try:
            cmd = ["subfinder", "-d", self.config["target"]["domain"], "-silent"]
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                subdomains = stdout.decode().splitlines()
                self.results["findings"].append({
                    "tool": "subfinder",
                    "subdomains": subdomains,
                    "timestamp": datetime.now().isoformat()
                })
            else:
                logger.error(f"Subfinder failed: {stderr.decode()}")
                
        except Exception as e:
            logger.error(f"Error running Subfinder: {e}")
            
    async def run_httpx(self, urls: List[str]):
        """Run httpx for HTTP probing"""
        try:
            # Write URLs to temporary file
            temp_file = Path("temp_urls.txt")
            temp_file.write_text("\n".join(urls))
            
            cmd = ["httpx", "-l", str(temp_file), "-silent", "-status-code", "-title"]
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                self.results["findings"].append({
                    "tool": "httpx",
                    "output": stdout.decode(),
                    "timestamp": datetime.now().isoformat()
                })
            else:
                logger.error(f"httpx failed: {stderr.decode()}")
                
            # Clean up temp file
            temp_file.unlink()
            
        except Exception as e:
            logger.error(f"Error running httpx: {e}")
            
    async def run_nuclei(self, urls: List[str]):
        """Run Nuclei for vulnerability scanning"""
        try:
            # Write URLs to temporary file
            temp_file = Path("temp_urls.txt")
            temp_file.write_text("\n".join(urls))
            
            cmd = ["nuclei", "-l", str(temp_file), "-severity", "critical,high,medium"]
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                self.results["findings"].append({
                    "tool": "nuclei",
                    "output": stdout.decode(),
                    "timestamp": datetime.now().isoformat()
                })
            else:
                logger.error(f"Nuclei failed: {stderr.decode()}")
                
            # Clean up temp file
            temp_file.unlink()
            
        except Exception as e:
            logger.error(f"Error running Nuclei: {e}")
            
    def save_results(self, output_path: Path):
        """Save scan results to file"""
        with open(output_path, 'w') as f:
            json.dump(self.results, f, indent=2)
            
async def main():
    # Initialize scanner
    scanner = ReconScanner(Path("configs/scan_config.json"))
    
    # Run scans
    logger.info("Starting reconnaissance scan...")
    
    # Run Nmap scan
    logger.info("Running Nmap scan...")
    await scanner.run_nmap_scan()
    
    # Run Subfinder
    logger.info("Running Subfinder...")
    await scanner.run_subfinder()
    
    # Get all discovered URLs
    urls = [scanner.config["target"]["url"]]
    for finding in scanner.results["findings"]:
        if finding["tool"] == "subfinder":
            urls.extend([f"https://{subdomain}" for subdomain in finding["subdomains"]])
    
    # Run httpx
    logger.info("Running httpx...")
    await scanner.run_httpx(urls)
    
    # Run Nuclei
    logger.info("Running Nuclei...")
    await scanner.run_nuclei(urls)
    
    # Save results
    output_path = Path("data/scan_results") / f"recon_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    scanner.save_results(output_path)
    
    logger.info(f"Scan completed. Results saved to {output_path}")

if __name__ == "__main__":
    asyncio.run(main()) 