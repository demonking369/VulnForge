#!/usr/bin/env python3
"""
VulnForge - Educational Cybersecurity Research Framework
For authorized testing and educational purposes only.
"""

# ╔══════════════════════════════════════════════════════════╗
# ║ VulnForge - Built with Blood by DemonKing369.0 👑        ║
# ║ GitHub: https://github.com/Arunking9                     ║
# ║ AI-Powered Security Framework for Bug Bounty Warriors ⚔️║
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
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from typing import Optional

from recon_module import EnhancedReconModule
from ai_integration import AIAnalyzer, OllamaClient
from ai_orchestrator import AIOrchestrator  # New Import
from modules.darkweb import (
    run_darkweb_osint,
    ROBIN_DEFAULT_MODEL,
    get_robin_model_choices,
)


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
            format="%(asctime)s - %(levelname)s - %(message)s",
            handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
        )
        self.logger = logging.getLogger(__name__)

    def banner(self):
        """Display tool banner"""
        banner_text = f"""
╔══════════════════════════════════════════════════════════════╗
║                         VulnForge v{self.version}            ║
║              Educational Security Research Framework         ║
║                   For Authorized Testing Only                ║
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

    def generate_tool(self, description: str):
        """Generate a custom tool using AI and save it to custom_tools directory."""
        try:
            # Use os.path.expanduser to properly handle home directory
            tool_dir = os.path.expanduser("~/.vulnforge/custom_tools")
            self.console.print(
                f"[bold blue]Resolved custom_tools directory:[/bold blue] {tool_dir}"
            )

            # Create directory with proper permissions
            try:
                os.makedirs(tool_dir, mode=0o755, exist_ok=True)
                self.console.print(
                    f"[bold green]✓ Directory created/verified:[/bold green] {tool_dir}"
                )
            except PermissionError as e:
                self.logger.error("Permission error creating directory: %s", e)
                return
            except Exception as e:
                self.logger.error("Error creating directory: %s", e)
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

            # Extract a reasonable filename from the description
            import re

            base_name = re.sub(r"[^a-zA-Z0-9]+", "_", description.strip().lower())[
                :32
            ].strip("_")
            filename = f"{base_name or 'custom_tool'}_{int(time.time())}.py"
            tool_path = os.path.join(tool_dir, filename)

            # Write the generated tool to file
            with open(tool_path, "w", encoding="utf-8") as f:
                f.write(response)
            # SECURITY FIX: Set secure file permissions (0o600) for generated tool files
            # This ensures only the owner can read/write the file
            os.chmod(tool_path, 0o600)
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
            tool_dir = os.path.expanduser("~/.vulnforge/custom_tools")
            metadata_path = os.path.join(tool_dir, "metadata.json")

            if not os.path.exists(tool_dir):
                self.console.print(
                    "[bold yellow]No custom tools directory found.[/bold yellow]"
                )
                return

            if not os.path.exists(metadata_path):
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


async def _async_main():
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
        default="AI_Propmt/system-prompts-and-models-of-ai-tools",
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
        choices=get_robin_model_choices(),
        default=ROBIN_DEFAULT_MODEL,
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

    # Initialize VulnForge
    vf = VulnForge()
    vf.banner()

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
        run_darkweb_osint(
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

    # Create session directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    session_dir = vf.base_dir / "sessions" / args.target / timestamp
    session_dir.mkdir(parents=True, exist_ok=True)

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
        print("Port scanning mode not implemented yet")

    elif args.mode == "web":
        print("Web discovery mode not implemented yet")

    elif args.mode == "exploit":
        print("Exploit mode not implemented yet")


def main():
    """Synchronous entrypoint for console_scripts."""
    asyncio.run(_async_main())


if __name__ == "__main__":
    main()
