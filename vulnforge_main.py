#!/usr/bin/env python3
"""
VulnForge - Educational Cybersecurity Research Framework
For authorized testing and educational purposes only.
"""

import os
import sys
import json
import argparse
import subprocess
import time
from datetime import datetime
from pathlib import Path
import logging
import asyncio
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from typing import Optional

from recon_module import EnhancedReconModule
from ai_integration import AIAnalyzer, OllamaClient

class VulnForge:
    def __init__(self):
        self.version = "1.0.0"
        self.base_dir = Path.home() / ".vulnforge"
        self.results_dir = self.base_dir / "results"
        self.tools_dir = self.base_dir / "tools"
        self.setup_directories()
        self.setup_logging()
        self.console = Console()
        
        # Initialize AI components
        self.ollama = OllamaClient()
        self.ai_analyzer = AIAnalyzer(self.ollama)
        
    def setup_directories(self):
        """Create necessary directories"""
        self.base_dir.mkdir(exist_ok=True)
        self.results_dir.mkdir(exist_ok=True)
        self.tools_dir.mkdir(exist_ok=True)
        
    def setup_logging(self):
        """Setup logging configuration"""
        log_file = self.base_dir / "vulnforge.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def banner(self):
        """Display tool banner"""
        banner_text = f"""
╔══════════════════════════════════════════════════════════════╗
║                         VulnForge v{self.version}                         ║
║              Educational Security Research Framework          ║
║                   For Authorized Testing Only                ║
╚══════════════════════════════════════════════════════════════╝
        """
        self.console.print(Panel(banner_text, style="bold blue"))
        
    def check_tools(self):
        """Check if required tools are installed"""
        required_tools = [
            "nmap", "subfinder", "httpx", "gobuster", 
            "nuclei", "ffuf", "whatweb", "dig"
        ]
        
        missing_tools = []
        for tool in required_tools:
            if not self.is_tool_installed(tool):
                missing_tools.append(tool)
                
        if missing_tools:
            self.logger.warning(f"Missing tools: {', '.join(missing_tools)}")
            return False
        return True
        
    def is_tool_installed(self, tool):
        """Check if a tool is installed"""
        try:
            subprocess.run(["which", tool], check=True, 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except subprocess.CalledProcessError:
            return False
            
    def install_missing_tools(self):
        """Install missing tools"""
        self.logger.info("Installing missing tools...")
        
        # Update package list
        subprocess.run(["sudo", "apt", "update"], check=True)
        
        # Install Go tools
        go_tools = {
            "subfinder": "github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest",
            "httpx": "github.com/projectdiscovery/httpx/cmd/httpx@latest",
            "nuclei": "github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest",
        }
        
        for tool, package in go_tools.items():
            if not self.is_tool_installed(tool):
                self.logger.info(f"Installing {tool}...")
                subprocess.run(["go", "install", package], check=True)
                
    async def run_recon(self, target: str, output_dir: Optional[Path] = None):
        """Run reconnaissance on target"""
        recon = EnhancedReconModule(self.base_dir, self.ai_analyzer)
        return await recon.run_recon(target, output_dir)


async def main():
    parser = argparse.ArgumentParser(description="VulnForge - Educational Security Research Framework")
    parser.add_argument("--target", "-t", help="Target domain or IP")
    parser.add_argument("--mode", "-m", choices=["recon", "scan", "web", "exploit"], 
                       default="recon", help="Operation mode")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--install", action="store_true", help="Install missing tools")
    parser.add_argument("--check", action="store_true", help="Check tool availability")
    parser.add_argument("--ai-model", help="Specify AI model to use")
    
    args = parser.parse_args()
    
    # Initialize VulnForge
    vf = VulnForge()
    vf.banner()
    
    # Check tools
    if args.check:
        if vf.check_tools():
            print("✓ All required tools are installed")
        else:
            print("✗ Some tools are missing")
            if input("Install missing tools? (y/N): ").lower() == 'y':
                vf.install_missing_tools()
        return
        
    # Install tools
    if args.install:
        vf.install_missing_tools()
        return
        
    # Require target for operations
    if not args.target:
        print("Error: Target is required for security assessment operations")
        print("Use --target to specify a domain or IP address you own or have authorization to test")
        return
        
    # Verify authorization
    print(f"\n⚠️  AUTHORIZATION REQUIRED ⚠️")
    print(f"Target: {args.target}")
    print("This tool should only be used on systems you own or have explicit permission to test.")
    
    if input("Do you have authorization to test this target? (yes/no): ").lower() != "yes":
        print("Exiting. Only use this tool on authorized targets.")
        return
        
    # Execute based on mode
    if args.mode == "recon":
        print(f"\n🔍 Starting reconnaissance on {args.target}")
        results = await vf.run_recon(args.target, args.output)
        
        # Display summary
        console = Console()
        console.print("\n[bold green]Reconnaissance Complete![/bold green]")
        console.print(f"Found {len(results['subdomains'])} subdomains")
        console.print(f"Discovered {len(results['web_services'])} web services")
        console.print(f"Identified {len(results['technologies'])} technologies")
        
        if results['ai_analysis'].get('critical_findings'):
            console.print("\n[bold red]Critical Findings:[/bold red]")
            for finding in results['ai_analysis']['critical_findings']:
                console.print(f"- {finding.get('type')}: {finding.get('description')}")
                
    elif args.mode == "scan":
        print("Port scanning mode not implemented yet")
        
    elif args.mode == "web":
        print("Web discovery mode not implemented yet")
        
    elif args.mode == "exploit":
        print("Exploit mode not implemented yet")


if __name__ == "__main__":
    asyncio.run(main())