#!/usr/bin/env python3
"""
VulnForge AI Integration Module
Handles Ollama integration, prompt engineering, and AI-powered analysis
"""

import json
import requests
import subprocess
import logging
from typing import Dict, List, Optional, Any
import time
import re
from pathlib import Path
import asyncio
import ctypes


class OllamaClient:
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.logger = logging.getLogger(__name__)
        self.main_model = "deepseek-coder-v2:16b-lite-base-q4_0"  # Main model
        self.assistant_model = "mistral:7b-instruct-v0.2-q4_0"  # Assistant model
        self.backup_models = ["deepseek-coder:6.7b", "codellama:7b", "mistral:7b"]

    def is_available(self) -> bool:
        """Check if Ollama service is running"""
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False

    def list_models(self) -> List[Dict]:
        """List available models"""
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                return response.json().get("models", [])
        except Exception as e:
            self.logger.error(f"Error listing models: {e}")
        return []

    def pull_model(self, model: str) -> bool:
        """Pull a model if not available"""
        try:
            self.logger.info(f"Pulling model: {model}")
            data = {"name": model}
            response = requests.post(
                f"{self.base_url}/api/pull", json=data, stream=True
            )

            for line in response.iter_lines():
                if line:
                    try:
                        status = json.loads(line.decode("utf-8"))
                        if status.get("status") == "success":
                            return True
                    except:
                        continue
        except Exception as e:
            self.logger.error(f"Error pulling model {model}: {e}")
        return False

    def generate(
        self, prompt: str, model: str = None, system_prompt: str = None
    ) -> Optional[str]:
        """Generate text using Ollama"""
        if not model:
            model = self.get_best_model()

        if not model:
            self.logger.error("No suitable model available")
            return None

        try:
            data = {
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.5,  # Lowered for more deterministic planning
                    "top_p": 0.9,
                    "max_tokens": 4096,
                    "num_ctx": 16384,  # Increased context window for large prompts
                    "num_thread": 8,
                    "repeat_penalty": 1.1,
                },
            }

            if system_prompt:
                data["system"] = system_prompt

            response = requests.post(
                f"{self.base_url}/api/generate", json=data, timeout=300
            )  # Increased timeout

            if response.status_code == 200:
                result = response.json()
                return result.get("response", "").strip()
            else:
                self.logger.error(f"Ollama API error: {response.status_code}")

        except Exception as e:
            self.logger.error(f"Error generating with Ollama: {e}")

        return None

    def get_best_model(self) -> Optional[str]:
        """Get the best available model"""
        available_models = [m["name"] for m in self.list_models()]

        # Check main model first (deepseek-coder-v2:16b-lite-base-q4_0)
        if self.main_model in available_models:
            return self.main_model

        # Check assistant model next (mistral:7b-instruct-v0.2-q4_0)
        if self.assistant_model in available_models:
            return self.assistant_model

        # Check backup models
        for model in self.backup_models:
            if model in available_models:
                return model

        # If no preferred models, return first available
        if available_models:
            return available_models[0]

        return None


# Load the shared library
parser_lib_path = Path(__file__).parent / "utils" / "c_parser" / "libparser.so"
c_parser = ctypes.CDLL(str(parser_lib_path))

# Define the function signature for type safety
c_parser.parse_nuclei_output.argtypes = [ctypes.c_char_p]
c_parser.parse_nuclei_output.restype = ctypes.c_char_p


class AIAnalyzer:
    def __init__(self, ollama_client: OllamaClient):
        self.ollama = ollama_client
        self.logger = logging.getLogger(__name__)

    def analyze_nmap_output(self, nmap_output: str) -> Dict[str, Any]:
        """Analyze nmap scan results using AI"""
        system_prompt = """You are a cybersecurity expert analyzing nmap scan results. 
        Identify potential vulnerabilities, interesting services, and security issues.
        Provide structured analysis in JSON format with severity levels."""

        prompt = f"""
        Analyze this nmap scan output and identify potential security issues:
        
        {nmap_output}
        
        Provide analysis in this JSON format:
        {{
            "summary": "Brief overview",
            "high_risk_ports": ["port:service pairs that are high risk"],
            "interesting_services": ["notable services found"],
            "potential_vulnerabilities": [
                {{
                    "port": "port number",
                    "service": "service name",
                    "vulnerability": "description",
                    "severity": "low/medium/high/critical",
                    "recommendation": "what to investigate"
                }}
            ],
            "next_steps": ["recommended follow-up actions"]
        }}
        """

        response = self.ollama.generate(prompt, system_prompt=system_prompt)
        if response:
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                # Extract JSON if wrapped in markdown
                json_match = re.search(r"```json\n(.*?)\n```", response, re.DOTALL)
                if json_match:
                    try:
                        return json.loads(json_match.group(1))
                    except:
                        pass

        return {"error": "Failed to analyze nmap output", "raw_response": response}

    def generate_exploit_code(self, vulnerability_info: Dict) -> str:
        """Generate exploit code based on vulnerability information"""
        system_prompt = """You are a security researcher creating proof-of-concept exploit code.
        Generate safe, educational exploit code with proper error handling and comments.
        Include safety warnings and ethical use disclaimers."""

        prompt = f"""
        Generate a Python proof-of-concept exploit for this vulnerability:
        
        Service: {vulnerability_info.get('service', 'Unknown')}
        Port: {vulnerability_info.get('port', 'Unknown')}
        Vulnerability: {vulnerability_info.get('vulnerability', 'Unknown')}
        Target: {vulnerability_info.get('target', 'localhost')}
        
        Requirements:
        1. Include proper error handling
        2. Add educational comments
        3. Include safety warnings
        4. Make it modular and readable
        5. Add timeout and connection limits
        6. Include ethical use disclaimer
        
        Generate complete, working Python code:
        """

        response = self.ollama.generate(prompt, system_prompt=system_prompt)
        return response or "# Failed to generate exploit code"

    def analyze_web_response(self, url: str, response_data: Dict) -> Dict[str, Any]:
        """Analyze web service response for vulnerabilities"""
        system_prompt = """You are a web application security expert.
        Analyze HTTP responses for potential vulnerabilities and security issues."""

        headers = response_data.get("headers", {})
        content = response_data.get("content", "")[:2000]  # Limit content length

        prompt = f"""
        Analyze this web service for security issues:
        
        URL: {url}
        Status Code: {response_data.get('status_code')}
        Headers: {json.dumps(headers, indent=2)}
        Content (first 2000 chars): {content}
        
        Look for:
        - Missing security headers
        - Information disclosure
        - Potential injection points
        - Authentication issues
        - Technology stack vulnerabilities
        
        Provide JSON analysis:
        {{
            "security_headers": {{
                "missing": ["list of missing security headers"],
                "present": ["list of present security headers"]
            }},
            "information_disclosure": ["any leaked information"],
            "potential_vulnerabilities": [
                {{
                    "type": "vulnerability type",
                    "description": "detailed description",
                    "severity": "low/medium/high/critical",
                    "location": "where found"
                }}
            ],
            "technology_stack": ["detected technologies"],
            "recommendations": ["security recommendations"]
        }}
        """

        response = self.ollama.generate(prompt, system_prompt=system_prompt)
        if response:
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                json_match = re.search(r"```json\n(.*?)\n```", response, re.DOTALL)
                if json_match:
                    try:
                        return json.loads(json_match.group(1))
                    except:
                        pass

        return {"error": "Failed to analyze web response", "raw_response": response}

    def fix_broken_tool(
        self, tool_name: str, error_output: str, source_code: str = None
    ) -> str:
        """Generate fixes for broken security tools"""
        system_prompt = """You are a DevOps engineer specializing in fixing broken security tools.
        Analyze errors and provide working solutions."""

        prompt = f"""
        This security tool is broken and needs fixing:
        
        Tool: {tool_name}
        Error Output: {error_output}
        Source Code (if available): {source_code[:1000] if source_code else 'Not provided'}
        
        Analyze the error and provide:
        1. Root cause analysis
        2. Step-by-step fix instructions
        3. Modified code if needed
        4. Alternative solutions
        5. Prevention measures
        
        Focus on common issues like:
        - Dependency problems
        - API changes
        - Python version compatibility
        - Missing environment variables
        - Network/permission issues
        """

        response = self.ollama.generate(prompt, system_prompt=system_prompt)
        return response or "# Failed to generate fix"

    def prioritize_vulnerabilities(self, vulnerabilities: List[Dict]) -> List[Dict]:
        """Use AI to prioritize vulnerabilities by exploitability and impact"""
        system_prompt = """You are a penetration tester prioritizing vulnerabilities.
        Rank vulnerabilities by exploitability and business impact."""

        prompt = f"""
        Prioritize these vulnerabilities for testing:
        
        {json.dumps(vulnerabilities, indent=2)}
        
        Consider:
        - Ease of exploitation
        - Potential impact
        - Likelihood of success
        - Chaining possibilities
        
        Return prioritized list with scores (1-10) and reasoning:
        {{
            "prioritized_vulnerabilities": [
                {{
                    "original_index": 0,
                    "exploitability_score": 8,
                    "impact_score": 9,
                    "overall_priority": 8.5,
                    "reasoning": "why this is high priority",
                    "exploitation_difficulty": "easy/medium/hard",
                    "recommended_tools": ["tools to use"]
                }}
            ]
        }}
        """

        response = self.ollama.generate(prompt, system_prompt=system_prompt)
        if response:
            try:
                result = json.loads(response)
                return result.get("prioritized_vulnerabilities", vulnerabilities)
            except:
                pass

        return vulnerabilities

    def analyze_nuclei_output(self, nuclei_json_output: str) -> Dict[str, Any]:
        """Analyze nuclei output using the high-speed C parser."""

        # Call the C function
        raw_summary = c_parser.parse_nuclei_output(nuclei_json_output.encode("utf-8"))
        summary_str = raw_summary.decode("utf-8")

        # The C function must free the memory it allocated, or we'd have a memory leak.
        # For this example, we assume a simple case. A real implementation needs memory management.

        try:
            return json.loads(summary_str)
        except json.JSONDecodeError:
            return {"error": "Failed to parse summary from C module"}


class AIOrchestrator:
    """
    Manages a multi-step AI reasoning pipeline for complex security tasks.
    It chains specialized prompts for planning, tool selection, and execution.
    """

    def __init__(self, prompt_dir: Path):
        self.prompt_dir = prompt_dir
        self.ollama = OllamaClient()
        self.prompts = self._load_prompts()
        self.state = {}

    def _load_prompts(self):
        """Loads the specialized AI prompts from the prompt directory."""
        prompts = {}
        try:
            # Devin-style planning prompt
            with open(self.prompt_dir / "Devin AI/system.md", "r") as f:
                prompts["planner"] = f.read()
            # Manus-style tool selection prompt
            with open(
                self.prompt_dir / "Manus Agent Tools & Prompt/system.md", "r"
            ) as f:
                prompts["tool_selector"] = f.read()
            # Cursor-style code/analysis prompt
            with open(self.prompt_dir / "Cursor Prompts/prompts.md", "r") as f:
                prompts["analyst"] = f.read()
        except FileNotFoundError as e:
            print(f"Error: Could not load a required prompt. {e}")
            raise
        return prompts

    def execute_task(self, task_description: str):
        """
        Executes a full task pipeline: Plan -> Select Tool -> Execute -> Analyze.
        """
        print("--- AI Task Pipeline Initiated ---")

        # 1. Planning Phase (using Devin's prompt)
        plan = self._planning_phase(task_description)
        self.state["plan"] = plan
        print(f"Phase 1: Plan Created -> {plan}")

        # 2. Tool Selection Phase (using Manus' prompt)
        tool_command = self._tool_selection_phase(task_description, plan)
        self.state["tool_command"] = tool_command
        print(f"Phase 2: Tool Selected -> {tool_command}")

        # 3. Execution Phase (simulated)
        execution_result = self._execution_phase(tool_command)
        self.state["execution_result"] = execution_result
        print(f"Phase 3: Execution Result -> {execution_result[:100]}...")

        # 4. Analysis Phase (using Cursor's prompt)
        analysis = self._analysis_phase(execution_result)
        self.state["analysis"] = analysis
        print(f"Phase 4: Analysis Complete -> {analysis}")

        print("--- AI Task Pipeline Complete ---")
        return self.state

    def _planning_phase(self, task: str) -> str:
        """Uses the 'planner' prompt to create a high-level strategy."""
        system_prompt = self.prompts["planner"]
        user_prompt = f"Create a step-by-step plan for the following task: {task}"
        response = self.ollama.generate(user_prompt, system_prompt=system_prompt)
        return response

    def _tool_selection_phase(self, task: str, plan: str) -> str:
        """Uses the 'tool_selector' prompt to choose the right command."""
        system_prompt = self.prompts["tool_selector"]
        user_prompt = f"Given the task '{task}' and the plan '{plan}', what is the exact shell command to execute next? Only output the command."
        response = self.ollama.generate(user_prompt, system_prompt=system_prompt)
        return response

    def _execution_phase(self, command: str) -> str:
        """Simulates running the command and returns mock output."""
        print(f"Simulating execution of: `{command}`")
        if "nmap" in command:
            return "Starting Nmap 7.92 ... Nmap scan report for example.com (93.184.216.34)\nHost is up (0.011s latency).\nNot shown: 998 filtered tcp ports\nPORT    STATE SERVICE\n80/tcp  open  http\n443/tcp open  https"
        return "Command executed successfully. No output."

    def _analysis_phase(self, result: str) -> str:
        """Uses the 'analyst' prompt to interpret the results."""
        system_prompt = self.prompts["analyst"]
        user_prompt = f"Analyze the following tool output and provide a summary of key findings and recommendations:\n\n{result}"
        response = self.ollama.generate(user_prompt, system_prompt=system_prompt)
        return response


# CLI interface for AI module
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="VulnForge AI Module")
    parser.add_argument(
        "--test-connection", action="store_true", help="Test Ollama connection"
    )
    parser.add_argument("--pull-model", help="Pull a specific model")
    parser.add_argument(
        "--list-models", action="store_true", help="List available models"
    )
    parser.add_argument("--analyze-nmap", help="Analyze nmap output file")
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

    args = parser.parse_args()

    orchestrator = AIOrchestrator(Path(args.prompt_dir))

    if args.test_connection:
        if orchestrator.ollama.is_available():
            print("✓ AI system ready")
        else:
            print("✗ AI system not available")

    elif args.pull_model:
        if orchestrator.ollama.pull_model(args.pull_model):
            print(f"✓ Model {args.pull_model} pulled successfully")
        else:
            print(f"✗ Failed to pull model {args.pull_model}")

    elif args.list_models:
        models = orchestrator.ollama.list_models()
        print("Available models:")
        for model in models:
            print(f"  - {model['name']}")

    elif args.analyze_nmap:
        with open(args.analyze_nmap, "r") as f:
            content = f.read()
        result = orchestrator.analyzer.analyze_nmap_output(content)
        print(json.dumps(result, indent=2))

    # Handle AI Pipeline Mode
    if args.ai_pipeline:
        if not args.target:
            print(
                "Error: A target is required for AI pipeline mode, e.g., --target 'scan example.com'"
            )

        prompt_path = Path(args.prompt_dir)
        if not prompt_path.exists():
            print(f"Error: Prompt directory not found at '{prompt_path}'")

        orchestrator = AIOrchestrator(prompt_path)
        orchestrator.execute_task(f"Perform a security scan on {args.target}")
