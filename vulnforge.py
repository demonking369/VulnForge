#!/usr/bin/env python3
"""
VulnForge - AI-Powered Vulnerability Research Framework
For authorized security research and bug bounty hunting
"""

import os
import sys
import argparse
import logging
import asyncio
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from modules.recon.recon import ReconModule
from utils.logger import setup_logger
from utils.cli_utils import print_banner
from utils.stealth_utils import stealth_manager

class VulnForge:
    def __init__(self):
        self.version = "0.1.0"
        self.console = Console()
        self.logger = setup_logger()
        self.base_dir = Path.home() / ".vulnforge"
        self.setup_directories()
        
    def setup_directories(self):
        """Create necessary directories if they don't exist"""
        dirs = [
            self.base_dir,
            self.base_dir / "results",
            self.base_dir / "logs",
            self.base_dir / "configs",
            self.base_dir / "data",
            self.base_dir / "data" / "cve_feeds",
            self.base_dir / "data" / "exploit_db",
            self.base_dir / "data" / "reports",
            self.base_dir / "data" / ".temp"
        ]
        for dir_path in dirs:
            dir_path.mkdir(parents=True, exist_ok=True)
            
    def check_tools(self) -> bool:
        """Check if required tools are installed"""
        required_tools = [
            "nmap", "subfinder", "httpx", "nuclei", 
            "gobuster", "ffuf", "whatweb", "dig"
        ]
        
        missing_tools = []
        for tool in required_tools:
            if not self.is_tool_installed(tool):
                missing_tools.append(tool)
                
        if missing_tools:
            self.logger.warning(f"Missing tools: {', '.join(missing_tools)}")
            return False
        return True
        
    def is_tool_installed(self, tool: str) -> bool:
        """Check if a tool is installed"""
        try:
            subprocess.run(["which", tool], check=True, 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except subprocess.CalledProcessError:
            return False
            
    async def run_recon(self, target: str, output_dir: str = None, stealth: bool = True):
        """Run reconnaissance module"""
        if stealth:
            # Configure stealth settings
            stealth_manager.set_delay_range(1.0, 3.0)
            
            # Load proxies if available
            proxy_file = self.base_dir / "configs" / "proxies.txt"
            if proxy_file.exists():
                stealth_manager.load_proxies_from_file(str(proxy_file))
                
        recon = ReconModule(self.base_dir)
        return await recon.run(target, output_dir)
        
    async def run_exploit(self, target: str, vulnerability: str):
        """Run exploit module (placeholder)"""
        self.console.print("[yellow]Exploit module not implemented yet[/yellow]")
        
    async def run_report(self, target: str, output_format: str = "markdown"):
        """Run reporting module (placeholder)"""
        self.console.print("[yellow]Reporting module not implemented yet[/yellow]")

async def main():
    parser = argparse.ArgumentParser(description="VulnForge - AI-Powered Vulnerability Research Framework")
    parser.add_argument("--target", "-t", required=True, help="Target domain or IP")
    parser.add_argument("--mode", "-m", choices=["recon", "exploit", "report"], 
                       default="recon", help="Operation mode")
    parser.add_argument("--output", "-o", help="Output directory")
    parser.add_argument("--vulnerability", "-v", help="Specific vulnerability to exploit")
    parser.add_argument("--format", "-f", choices=["markdown", "json", "html"],
                       default="markdown", help="Report output format")
    parser.add_argument("--stealth", "-s", action="store_true", 
                       help="Enable stealth mode with random delays and proxy rotation")
    parser.add_argument("--check", action="store_true", 
                       help="Check if required tools are installed")
    
    args = parser.parse_args()
    
    # Initialize VulnForge
    vf = VulnForge()
    print_banner(vf.version)
    
    # Check tools if requested
    if args.check:
        if vf.check_tools():
            print("✓ All required tools are installed")
        else:
            print("✗ Some tools are missing")
            if input("Install missing tools? (y/N): ").lower() == 'y':
                # TODO: Implement tool installation
                pass
        return
    
    # Verify authorization
    vf.console.print("\n[bold red]⚠️  AUTHORIZATION REQUIRED ⚠️[/bold red]")
    vf.console.print(f"Target: {args.target}")
    vf.console.print("This tool should only be used on systems you own or have explicit permission to test.")
    
    if input("Do you have authorization to test this target? (yes/no): ").lower() != "yes":
        vf.console.print("[red]Exiting. Only use this tool on authorized targets.[/red]")
        return
        
    # Execute based on mode
    if args.mode == "recon":
        vf.console.print(f"\n[bold blue]🔍 Starting reconnaissance on {args.target}[/bold blue]")
        results = await vf.run_recon(args.target, args.output, args.stealth)
        
    elif args.mode == "exploit":
        if not args.vulnerability:
            vf.console.print("[red]Error: Vulnerability must be specified for exploit mode[/red]")
            return
        await vf.run_exploit(args.target, args.vulnerability)
        
    elif args.mode == "report":
        await vf.run_report(args.target, args.format)

if __name__ == "__main__":
    asyncio.run(main()) 