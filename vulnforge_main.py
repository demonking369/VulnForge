#!/usr/bin/env python3
"""
VulnForge - Educational Cybersecurity Research Framework
For authorized testing and educational purposes only.
"""

# ╔══════════════════════════════════════════════════════════╗
# ║ VulnForge - Built with Blood by DemonKing369.0 👑        ║
# ║ GitHub: https://github.com/Arunking9                     ║
# ║ AI-Powered Security Framework for Bug Bounty Warriors ⚔️ ║
# ╚══════════════════════════════════════════════════════════╝

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
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

# Load environment variables
load_dotenv()
from typing import Optional

# SECURITY: Import security utilities
from utils.security_utils import (
    SecurityValidator,
    RateLimiter,
    FilePermissionManager,
    validate_target,
    sanitize_filename,
)
from utils.auth import get_auth_manager, Permission

from modules.recon.recon_module import EnhancedReconModule
from modules.ai.ai_integration import AIAnalyzer, OllamaClient
from modules.ai.ai_orchestrator import AIOrchestrator  # New Import
import modules.darkweb as darkweb_module
from modules.ai.agent import VulnForgeAgent
from modules.web.web_module import WebModule
from modules.exploit.exploit_module import ExploitModule
from modules.scan.scan_module import ScanModule


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
        self.agentic_mode = False
        self.agent = VulnForgeAgent(self.ollama)
        self.web_module = WebModule(self.base_dir, self.ai_analyzer)
        self.exploit_module = ExploitModule(self.base_dir, self.ai_analyzer)
        self.scan_module = ScanModule(self.base_dir, self.ai_analyzer)

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
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
        )
        self.logger = logging.getLogger(__name__)

    def banner(self):
        """Display tool banner"""
        banner_text = f"""
╔══════════════════════════════════════════════════════════════╗
║                    VulnForge v{self.version:10}                ║
║           Educational Security Research Framework            ║
║                For Authorized Testing Only                   ║
╚══════════════════════════════════════════════════════════════╝
        """
        self.console.print(Panel(banner_text, style="bold blue"))

    def check_tools(self):
        """Check if required tools are installed"""
        required_tools = [
            "nmap",
            "subfinder",
            "httpx",
            "gobuster",
            "nuclei",
            "ffuf",
            "whatweb",
            "dig",
        ]

        missing_tools = []
        for tool in required_tools:
            if not self.is_tool_installed(tool):
                missing_tools.append(tool)

        if missing_tools:
            self.logger.warning("Missing tools: %s", ", ".join(missing_tools))
            return False
        return True

    def is_tool_installed(self, tool):
        """Check if a tool is installed"""
        try:
            subprocess.run(
                ["which", tool],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return True
        except subprocess.CalledProcessError:
            return False

    def install_missing_tools(self):
        """Install missing tools"""
        self.logger.info("Installing missing tools...")

        # Update package list
        try:
            subprocess.run(["sudo", "apt", "update"], check=True)
        except subprocess.CalledProcessError as e:
            self.logger.error("Failed to update package list: %s", e)
            return False

        # Install Go tools
        go_tools = {
            "subfinder": "github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest",
            "httpx": "github.com/projectdiscovery/httpx/cmd/httpx@latest",
            "nuclei": "github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest",
        }

        for tool, package in go_tools.items():
            if not self.is_tool_installed(tool):
                self.logger.info("Installing %s...", tool)
                try:
                    # SECURITY FIX: Use full executable path and handle subprocess failures
                    result = subprocess.run(
                        ["/usr/bin/go", "install", package],
                        capture_output=True,
                        text=True,
                        check=True,
                    )
                    self.logger.info("Successfully installed %s", tool)
                except subprocess.CalledProcessError as e:
                    self.logger.error("Failed to install %s: %s", tool, e)
                    self.logger.error("stderr: %s", e.stderr)
                    return False
                except FileNotFoundError:
                    self.logger.error("Go not found. Please install Go first.")
                    return False

        return True

    async def run_recon(self, target: str, output_dir: Optional[Path] = None):
        """Run reconnaissance on target"""
        recon = EnhancedReconModule(
            self.base_dir, self.ai_analyzer, config_path="configs/tools.json"
        )
        return await recon.run_recon(target, output_dir)

    def ask_ai(self, question: str):
        """Handle AI questions"""
        system_prompt = """You are a cybersecurity expert assistant. Provide detailed, 
        accurate, and educational responses about security concepts, tools, and best practices.
        Always emphasize ethical use and proper authorization."""

        response = self.ollama.generate(question, system_prompt=system_prompt)
        if response:
            self.console.print("\n[bold green]AI Response:[/bold green]")
            self.console.print(Panel(response, style="blue"))
        else:
            self.console.print(
                "[bold red]Error: Could not get response from AI[/bold red]"
            )

    @RateLimiter(max_calls=5, time_window=60)
    def generate_tool(self, description: str, identifier: str = "default"):
        """Generate a custom tool using AI and save it to custom_tools directory.

        Args:
            description: Tool description
            identifier: Rate limit identifier (username/session)
        """
        try:
            # SECURITY: Sanitize description input
            if not description or not isinstance(description, str):
                self.logger.error("Invalid tool description")
                return

            # SECURITY: Limit description length
            if len(description) > 500:
                self.logger.error("Tool description too long (max 500 chars)")
                return

            # Use os.path.expanduser to properly handle home directory
            tool_dir = Path.home() / ".vulnforge" / "custom_tools"
            self.console.print(
                f"[bold blue]Resolved custom_tools directory:[/bold blue] {tool_dir}"
            )

            # SECURITY: Create directory with secure permissions (0o700)
            if not FilePermissionManager.create_secure_directory(tool_dir, mode=0o700):
                self.logger.error("Failed to create secure directory")
                return

            metadata_path = os.path.join(tool_dir, "metadata.json")

            system_prompt = (
                "You are an expert Python developer and security researcher. "
                "Generate a complete, safe, and well-documented Python script for the following tool description. "
                "Add usage instructions as comments at the top. The script should be self-contained and ready to use. "
                "Emphasize ethical use and include a disclaimer in the comments."
            )

            response = self.ollama.generate(description, system_prompt=system_prompt)
            if not response:
                self.console.print(
                    "[bold red]Error: Could not get response from AI[/bold red]"
                )
                return

            # SECURITY: Extract and sanitize filename
            import re

            base_name = re.sub(r"[^a-zA-Z0-9]+", "_", description.strip().lower())[
                :32
            ].strip("_")
            filename = sanitize_filename(
                f"{base_name or 'custom_tool'}_{int(time.time())}.py"
            )

            # SECURITY: Validate path to prevent traversal
            tool_path = SecurityValidator.sanitize_path(
                str(tool_dir / filename), base_dir=tool_dir
            )
            if not tool_path:
                self.logger.error("Invalid tool path")
                return

            # Write the generated tool to file
            with open(tool_path, "w", encoding="utf-8") as f:
                f.write(response)

            # SECURITY: Set secure file permissions (0o600) for generated tool files
            FilePermissionManager.set_secure_permissions(tool_path, mode=0o600)
            self.console.print(
                f"[bold green]✓ Tool generated and saved to:[/bold green] {tool_path}"
            )

            # Update metadata
            try:
                metadata = []
                if os.path.exists(metadata_path):
                    try:
                        with open(metadata_path) as f:
                            metadata = json.load(f)
                    except Exception as e:
                        self.logger.warning("Error reading metadata file: %s", e)
                        metadata = []

                metadata.append(
                    {
                        "description": description,
                        "filename": filename,
                        "created_at": datetime.now().isoformat(),
                    }
                )

                with open(metadata_path, "w", encoding="utf-8") as f:
                    json.dump(metadata, f, indent=2)
                # SECURITY FIX: Set secure file permissions for metadata files
                os.chmod(metadata_path, 0o600)
                self.console.print(
                    f"[bold green]✓ Metadata updated:[/bold green] {metadata_path}"
                )
            except Exception as e:
                self.logger.error("Error updating metadata: %s", e)
                return False

        except Exception as e:
            self.logger.error("Unexpected error in generate_tool: %s", e)
            return False

    def list_custom_tools(self):
        """List all custom tools in the custom_tools directory."""
        try:
            # SECURITY: Use Path and validate directory
            tool_dir = Path.home() / ".vulnforge" / "custom_tools"

            # SECURITY: Validate path
            tool_dir = SecurityValidator.sanitize_path(str(tool_dir))
            if not tool_dir:
                self.logger.error("Invalid tool directory path")
                return

            metadata_path = tool_dir / "metadata.json"

            if not tool_dir.exists():
                self.console.print(
                    "[bold yellow]No custom tools directory found.[/bold yellow]"
                )
                return

            if not metadata_path.exists():
                self.console.print(
                    "[bold yellow]No custom tools metadata found.[/bold yellow]"
                )
                return

            try:
                with open(metadata_path) as f:
                    metadata = json.load(f)

                if not metadata:
                    self.console.print(
                        "[bold yellow]No custom tools found.[/bold yellow]"
                    )
                    return

                self.console.print("\n[bold blue]Custom Tools:[/bold blue]")
                for tool in metadata:
                    self.console.print(
                        f"\n[bold green]Tool:[/bold green] {tool['filename']}"
                    )
                    self.console.print(
                        f"[bold cyan]Description:[/bold cyan] {tool['description']}"
                    )
                    self.console.print(
                        f"[bold magenta]Created:[/bold magenta] {tool['created_at']}"
                    )

            except Exception as e:
                self.logger.error("Error reading metadata: %s", e)
                return []

        except Exception as e:
            self.logger.error("Unexpected error in list_custom_tools: %s", e)
            return []


async def dev_mode_shell(vf, session_dir):
    console = Console()
    history = []
    console.print(
        "\n[bold magenta]Entering Dev Mode Shell. Type 'help' for commands.[/bold magenta]"
    )
    while True:
        try:
            cmd = input("[dev-mode]> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting dev mode.")
            break
        if not cmd:
            continue
        history.append(cmd)
        parts = cmd.split()
        if parts[0] == "help":
            console.print(
                """
[bold cyan]Available commands:[/bold cyan]
- analyze <module>: Analyze a module for improvements
- modify <module> <changes>: Apply changes to a module
- list: Show modification history
- help: Show this help message
- exit: Exit dev mode
"""
            )
        elif parts[0] == "exit":
            print("Exiting dev mode.")
            break
        elif parts[0] == "list":
            if history:
                console.print("[bold green]Modification History:[/bold green]")
                for h in history:
                    console.print(f"- {h}")
            else:
                console.print("[yellow]No modifications yet.[/yellow]")
        elif parts[0] == "analyze" and len(parts) > 1:
            module = parts[1]
            console.print(f"[bold blue]Analyzing module:[/bold blue] {module}")
            # Placeholder for actual analysis logic
            console.print(
                f"[italic]AI analysis for {module} not yet implemented.[/italic]"
            )
        elif parts[0] == "modify" and len(parts) > 2:
            module = parts[1]
            changes = " ".join(parts[2:])
            console.print(f"[bold blue]Modifying module:[/bold blue] {module}")
            console.print(f"[bold yellow]Requested changes:[/bold yellow] {changes}")
            # Placeholder for actual modification logic
            console.print(
                f"[italic]AI modification for {module} not yet implemented.[/italic]"
            )
        else:
            console.print(
                "[red]Unknown command. Type 'help' for available commands.[/red]"
            )


def get_parser():
    parser = argparse.ArgumentParser(
        description="""
╔══════════════════════════════════════════════════════════╗
║ VulnForge - Built with Blood by DemonKing369.0 👑        ║
║ GitHub: https://github.com/Arunking9                     ║
║ AI-Powered Security Framework for Bug Bounty Warriors ⚔️ ║
╚══════════════════════════════════════════════════════════╝

A powerful AI-driven security testing framework for authorized penetration testing and bug bounty hunting.

Key Features:
• AI-Autonomous Operation (--ai-only)
• Advanced Reconnaissance
• Stealth Mode Capabilities
• Multi-format Reporting
• Custom Tool Generation
• Interactive AI Assistant
• Development Mode

For detailed documentation, visit: https://github.com/Arunking9/VulnForge
""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--target", "-t", help="Target domain or IP")
    parser.add_argument(
        "--mode",
        "-m",
        choices=["recon", "scan", "web", "exploit"],
        default="recon",
        help="Operation mode",
    )
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument(
        "--output-format",
        choices=["markdown", "json", "html", "all"],
        default="all",
        help="Report output format",
    )
    parser.add_argument("--install", action="store_true", help="Install missing tools")
    parser.add_argument("--check", action="store_true", help="Check tool availability")
    parser.add_argument("--ai-model", help="Specify AI model to use")
    parser.add_argument(
        "--ai-only", action="store_true", help="Enable fully autonomous AI mode"
    )
    parser.add_argument(
        "--ai-debug", action="store_true", help="Show detailed AI reasoning"
    )
    parser.add_argument(
        "--dev-mode", action="store_true", help="Enable development mode"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Show detailed logs"
    )
    parser.add_argument(
        "--stealth", "-s", action="store_true", help="Enable stealth mode"
    )
    parser.add_argument(
        "--ai-pipeline",
        action="store_true",
        help="Enable the advanced multi-prompt AI pipeline.",
    )
    parser.add_argument(
        "--prompt-dir",
        help="Directory for the AI pipeline prompts.",
        default="prompts/system_prompts",
    )
    parser.add_argument(
        "--uninstall",
        action="store_true",
        help="Uninstall VulnForge and its components",
    )
    parser.add_argument(
        "--webmod",
        action="store_true",
        help="Launch VulnForge web interface (Streamlit UI)",
    )
    parser.add_argument(
        "--web-host",
        default="localhost",
        help="Web interface host (default: localhost)",
    )
    parser.add_argument(
        "--web-port", type=int, default=8501, help="Web interface port (default: 8501)"
    )
    parser.add_argument(
        "--agentic",
        "--ai-agent",
        action="store_true",
        help="Enable simple agentic AI mode",
    )
    parser.add_argument(
        "--no-ai", action="store_true", help="Disable AI analysis for the current mode"
    )

    # Add subparsers for commands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Ask AI command
    ask_ai_parser = subparsers.add_parser(
        "ask-ai", help="Ask the AI assistant a question"
    )
    ask_ai_parser.add_argument("question", help="The question to ask the AI")
    ask_ai_parser.add_argument(
        "--verbose", action="store_true", help="Show detailed model logs"
    )
    ask_ai_parser.add_argument(
        "--dangerous", action="store_true", help="Enable dangerous mode"
    )
    ask_ai_parser.add_argument(
        "--confirm-danger", action="store_true", help="Confirm dangerous mode"
    )

    # Generate tool command
    generate_tool_parser = subparsers.add_parser(
        "generate-tool", help="Generate a custom tool"
    )
    generate_tool_parser.add_argument(
        "description", help="Description of the tool to generate"
    )
    generate_tool_parser.add_argument(
        "--verbose", action="store_true", help="Show detailed generation logs"
    )

    # List tools command
    list_tools_parser = subparsers.add_parser(
        "list-tools", help="List all custom tools"
    )
    list_tools_parser.add_argument(
        "--verbose", action="store_true", help="Show detailed tool information"
    )

    # Dark web OSINT command (Robin integration)
    darkweb_parser = subparsers.add_parser(
        "darkweb", help="Run the Robin dark web OSINT workflow"
    )
    darkweb_parser.add_argument(
        "--query", "-q", required=True, help="Dark web search query"
    )
    darkweb_parser.add_argument(
        "--model",
        "-m",
        choices=darkweb_module.get_robin_model_choices(),
        default=darkweb_module.ROBIN_DEFAULT_MODEL,
        help="LLM model to use for refinement/filtering",
    )
    darkweb_parser.add_argument(
        "--threads",
        "-t",
        type=int,
        default=5,
        help="Number of concurrent requests for search/scrape",
    )
    darkweb_parser.add_argument(
        "--output",
        "-o",
        help="Optional output file or directory for the markdown report",
    )

    args = parser.parse_args()
    return parser, args


async def _async_main(args):
    # Initialize VulnForge
    vf = VulnForge()
    vf.banner()

    # Handle uninstall
    if args.uninstall:
        script_dir = Path(__file__).parent
        uninstall_script = script_dir / "uninstall_script.sh"

        if not uninstall_script.exists():
            print(f"Error: Uninstall script not found at {uninstall_script}")
            return

        try:
            subprocess.run([str(uninstall_script)], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running uninstall script: {e}")
        except KeyboardInterrupt:
            print("\nUninstall cancelled by user")
        return

    # Handle AI Pipeline Mode
    if args.ai_pipeline:
        if not args.target:
            print(
                "Error: A target is required for AI pipeline mode, e.g., --target 'scan example.com'"
            )
            return

        prompt_path = Path(args.prompt_dir)
        if not prompt_path.exists():
            print(f"Error: Prompt directory not found at '{prompt_path}'")
            return

        orchestrator = AIOrchestrator(prompt_path)
        orchestrator.execute_task(f"Perform a security scan on {args.target}")
        return

    # Handle Agentic AI Mode
    if args.agentic:
        vf.agentic_mode = True
        os.environ["VULNFORGE_AGENTIC"] = "1"
        vf.logger.info("Agentic AI mode enabled.")
        if args.target:
            # If target provided, run an initial agentic task
            task = f"Analyze and plan a security assessment for target: {args.target}"
            result = await vf.agent.run_task(task)
            vf.console.print("\n[bold cyan]--- Agentic Action Plan ---[/bold cyan]")
            vf.console.print(json.dumps(result, indent=2))
        else:
            vf.console.print(
                "\n[bold yellow]Agentic mode enabled. Ready for instructions...[/bold yellow]"
            )

        # If we are not in web mode, we might want an interactive CLI loop here
        # For now, we'll just continue to respect other flags.

    # Set logging level based on verbose flag
    if args.verbose:
        vf.logger.setLevel(logging.DEBUG)

    # Handle commands
    if args.command == "ask-ai":
        if args.dangerous and not args.confirm_danger:
            print("Error: --dangerous mode requires --confirm-danger flag")
            return
        vf.ask_ai(args.question)
        return
    elif args.command == "generate-tool":
        vf.generate_tool(args.description)
        return
    elif args.command == "list-tools":
        vf.list_custom_tools()
        return
    elif args.command == "darkweb":
        # Check if Robin is available
        if not darkweb_module.ROBIN_AVAILABLE:
            print("❌ Error: Robin module dependencies not installed.")
            print(
                "Install with: pip install langchain-core langchain-openai langchain-ollama"
            )
            return

        darkweb_module.run_darkweb_osint(
            args.query,
            model=args.model,
            threads=args.threads,
            output=args.output,
        )
        return

    # Check tools
    if args.check:
        if vf.check_tools():
            print("✓ All required tools are installed")
        else:
            print("✗ Some tools are missing")
            if input("Install missing tools? (y/N): ").lower() == "y":
                vf.install_missing_tools()
        return

    # Install tools
    if args.install:
        vf.install_missing_tools()
        return

    # Require target for operations
    if not args.target:
        print("Error: Target is required for security assessment operations")
        print(
            "Use --target to specify a domain or IP address you own or have authorization to test"
        )
        return

    # SECURITY: Validate target input
    if not validate_target(args.target):
        print(f"Error: Invalid target format: {args.target}")
        print("Target must be a valid domain name or IP address")
        return

    # Remove authorization prompt and disclaimer
    # Verify authorization
    # print(f"\n⚠️  AUTHORIZATION REQUIRED ⚠️")
    # print(f"Target: {args.target}")
    # print("This tool should only be used on systems you own or have explicit permission to test.")
    # if input("Do you have authorization to test this target? (yes/no): ").lower() != "yes":
    #     print("Exiting. Only use this tool on authorized targets.")
    #     return
    vf.logger.info("Authorization assumed. Continuing...")
    # Optionally, log a warning to file only
    logging.getLogger("vulnforge").warning(
        "No explicit authorization prompt. User is responsible for legal/ethical use."
    )

    # SECURITY: Create session directory with secure permissions
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # SECURITY: Sanitize target for use in path
    safe_target = sanitize_filename(args.target)
    session_dir = vf.base_dir / "sessions" / safe_target / timestamp

    # SECURITY: Create with restricted permissions
    if not FilePermissionManager.create_secure_directory(session_dir, mode=0o700):
        print("Error: Failed to create secure session directory")
        return

    # Initialize AI controller if needed
    if args.ai_only or args.ai_debug:
        from ai_controller import AIController

        ai_controller = AIController(
            str(session_dir), str(vf.base_dir / "configs" / "scan_config.json")
        )
        if not ai_controller.setup_ai():
            print("Error: Failed to setup AI system")
            return

        # Set output format
        ai_controller.output_format = args.output_format

    # Execute based on mode
    if args.mode == "recon":
        print(f"\n🔍 Starting reconnaissance on {args.target}")
        if args.ai_only:
            print("Running in AI-only mode - AI will make all decisions")
        if args.ai_debug:
            print("Debug mode enabled - showing detailed AI reasoning")
        if args.stealth:
            print("Stealth mode enabled - using random delays and rotating user agents")

        results = await vf.run_recon(args.target, args.output)

        # Display summary
        console = Console()
        console.print("\n[bold green]Reconnaissance Complete![bold green]")
        console.print(f"Found {len(results['subdomains'])} subdomains")
        console.print(f"Discovered {len(results['web_services'])} web services")

        # Count unique technologies
        technologies = set()
        for service in results["web_services"]:
            technologies.update(service.get("technologies", []))
        console.print(f"Identified {len(technologies)} unique technologies")

        if results["ai_analysis"].get("critical_findings"):
            console.print("\n[bold red]Critical Findings:[/bold red]")
            for finding in results["ai_analysis"]["critical_findings"]:
                console.print(f"- {finding.get('type')}: {finding.get('description')}")

        # Start dev mode shell if requested
        if args.dev_mode:
            await dev_mode_shell(vf, session_dir)

    elif args.mode == "scan":
        print(f"\n📡 Starting port scan on {args.target}")

        results = await vf.scan_module.run_scan(args.target, session_dir, use_ai=False)

        console = Console()
        console.print("\n[bold green]Scan Complete![/bold green]")
        console.print(f"Found {len(results['ports'])} open ports")

        if results["ports"]:
            from rich.table import Table

            table = Table(title=f"Open Ports on {args.target}")
            table.add_column("Port", style="cyan")
            table.add_column("State", style="green")
            table.add_column("Service", style="magenta")
            table.add_column("Version", style="yellow")

            for p in results["ports"]:
                version = f"{p['product']} {p['version']}".strip() or "N/A"
                table.add_row(
                    f"{p['number']}/{p['protocol']}", p["state"], p["service"], version
                )

            console.print(table)

        # AI Analysis Interaction
        if not args.no_ai:
            if (
                input(
                    "\n🤖 Do you want an AI analysis of these results? (y/N): "
                ).lower()
                == "y"
            ):
                console.print("\n[bold cyan]Generating AI Analysis...[/bold cyan]")
                # We reuse AIAnalyzer.analyze_nmap_output via ScanModule
                nmap_str = vf.scan_module._format_nmap_results(results["ports"])
                analysis = await vf.ai_analyzer.analyze_nmap_output(nmap_str)
                results["ai_analysis"] = analysis

                # Update saved results
                vf.scan_module._save_results(results, session_dir)

                if analysis:
                    console.print("\n[bold cyan]AI Security Insights:[/bold cyan]")
                    if isinstance(analysis, dict):
                        if "summary" in analysis:
                            console.print(
                                f"\n[bold]Summary:[/bold]\n{analysis['summary']}"
                            )
                        if "potential_vulnerabilities" in analysis:
                            console.print(
                                "\n[bold yellow]Potential Vulnerabilities:[/bold yellow]"
                            )
                            for v in analysis["potential_vulnerabilities"]:
                                console.print(
                                    f"- [bold]{v.get('type')}[/bold]: {v.get('description')} (Severity: {v.get('severity')})"
                                )
                    else:
                        console.print(analysis)
            else:
                console.print("\n[yellow]Skipping AI analysis.[/yellow]")
        else:
            console.print("\n[yellow]AI analysis disabled by flag.[/yellow]")

    elif args.mode == "web":
        print(f"\n🌐 Starting web discovery on {args.target}")
        if args.ai_only:
            print("Running in AI-only mode - AI will make all decisions")

        # Run discovery without AI initially to allow for interactive prompt at the end
        results = await vf.web_module.run_web_discovery(
            args.target, session_dir, use_ai=False
        )

        # Display summary
        console = Console()
        console.print("\n[bold green]Web Discovery Complete![/bold green]")
        console.print(f"Discovered {len(results['technologies'])} technologies")
        console.print(f"Found {len(results['directories'])} directories/files")

        # Interactive AI Analysis Prompt
        if not args.no_ai:
            if (
                input(
                    "\n🤖 Do you want an AI analysis of these results? (y/N): "
                ).lower()
                == "y"
            ):
                console.print("\n[bold cyan]Generating AI Analysis...[/bold cyan]")
                analysis = await vf.web_module.analyze_with_ai(args.target, results)
                results["ai_analysis"] = analysis

                # Update saved results with AI analysis
                vf.web_module.save_results(results, session_dir)

                if "error" not in analysis:
                    console.print("\n[bold cyan]AI Analysis Summary:[/bold cyan]")
                    st = analysis.get("tech_stack_assessment", "N/A")
                    console.print(f"[bold]Tech Stack:[/bold] {st}")

                    interesting = analysis.get("interesting_findings", [])
                    if interesting:
                        console.print(
                            "\n[bold yellow]Interesting Findings:[/bold yellow]"
                        )
                        for finding in interesting:
                            console.print(f"- {finding}")
            else:
                console.print("\n[yellow]Skipping AI analysis.[/yellow]")
        else:
            console.print("\n[yellow]AI analysis disabled by flag.[/yellow]")

        # Start dev mode shell if requested
        if args.dev_mode:
            await dev_mode_shell(vf, session_dir)

    elif args.mode == "exploit":
        print(f"\n💀 Starting exploit mode on {args.target}")

        # To run exploit mode, we need recon data
        # Let's check if there's a recent recon scan for this target
        recon_data = {}
        recon_results_path = session_dir / "recon_results.json"
        web_results_path = session_dir / "web_discovery_results.json"

        if recon_results_path.exists():
            with open(recon_results_path, "r") as f:
                recon_data = json.load(f)
        elif web_results_path.exists():
            with open(web_results_path, "r") as f:
                web_data = json.load(f)
                # Map web data to a format exploit module understands
                recon_data = {
                    "target": args.target,
                    "services": [
                        {"name": tech.get("raw"), "version": ""}
                        for tech in web_data.get("technologies", [])
                    ],
                }
        else:
            print(
                "[yellow]No reconnaissance data found for this target in the current session.[/yellow]"
            )
            print("Exploit mode works best when preceded by 'recon' or 'web' mode.")
            # We can still try with basic info if provided
            recon_data = {"target": args.target, "services": []}

        results = await vf.exploit_module.run_exploit_pipeline(
            args.target, recon_data, session_dir, use_ai=not args.no_ai
        )

        console = Console()
        console.print("\n[bold green]Exploit Pipeline Complete![/bold green]")
        console.print(
            f"Mapped {len(results['vulnerabilities'])} potential vulnerabilities"
        )
        console.print(f"Generated {len(results['exploits'])} exploits")

        if results["exploits"]:
            console.print("\n[bold cyan]Generated Exploits:[/bold cyan]")
            for exploit in results["exploits"]:
                if "error" not in exploit:
                    console.print(f"- [green]{exploit.get('file_path')}[/green]")
                    if exploit.get("validation", {}).get("issues"):
                        console.print(
                            f"  [yellow]Validation Issues:[/yellow] {', '.join(exploit['validation']['issues'])}"
                        )

        # Start dev mode shell if requested
        if args.dev_mode:
            await dev_mode_shell(vf, session_dir)


def main():
    """Synchronous entrypoint for console_scripts."""
    parser, args = get_parser()

    # Handle web mode BEFORE starting asyncio loop
    if args.webmod:
        # Check if Robin module is available
        if not darkweb_module.ROBIN_AVAILABLE:
            print("❌ Error: Robin module dependencies not installed.")
            print("\nInstall required packages:")
            print("  pip install langchain-core langchain-openai langchain-ollama")
            print(
                "  pip install langchain-anthropic langchain-google-genai langchain-community"
            )
            print("\nOr install all requirements:")
            print("  pip install -r requirements.txt")
            return

        print("🌐 Launching VulnForge Web Interface...")
        print(f"📍 Access the UI at: http://{args.web_host}:{args.web_port}")
        print("⚠️  Press Ctrl+C to stop the server\n")

        try:
            # Import streamlit CLI
            from streamlit.web import cli as stcli
            import sys

            # Get the UI file path
            ui_file = Path(__file__).parent / "modules" / "web" / "dashboard.py"

            if not ui_file.exists():
                print(f"❌ Error: Web UI file not found at {ui_file}")
                return

            # Prepare streamlit arguments
            sys.argv = [
                "streamlit",
                "run",
                str(ui_file),
                "--server.port",
                str(args.web_port),
                "--server.address",
                args.web_host,
                "--server.headless",
                "true",
                "--browser.gatherUsageStats",
                "false",
            ]

            # Launch streamlit
            sys.exit(stcli.main())

        except ImportError:
            print("❌ Error: Streamlit is not installed.")
            return
        except Exception as e:
            print(f"❌ Error launching web interface: {e}")
            return

    # Run the main async pipeline
    asyncio.run(_async_main(args))


if __name__ == "__main__":
    main()
