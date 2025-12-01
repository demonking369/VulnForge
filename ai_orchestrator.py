import json
import subprocess
import shlex
from pathlib import Path
from ai_integration import OllamaClient


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
        prompts = {}
        try:
            # SECURITY FIX: Use correct path structure and file names for the nested prompt directories
            base_prompt_dir = self.prompt_dir / "system-prompts-and-models-of-ai-tools"

            # Check what files actually exist and use appropriate fallbacks
            devin_file = base_prompt_dir / "Devin AI/Prompt.txt"
            manus_file = base_prompt_dir / "Manus Agent Tools & Prompt/system.md"
            cursor_file = base_prompt_dir / "Cursor Prompts/prompts.md"

            # Load Devin AI prompt
            if devin_file.exists():
                with open(devin_file, "r") as f:
                    prompts["planner"] = f.read()
            else:
                prompts["planner"] = (
                    "You are a planning AI. Create step-by-step plans for tasks."
                )

            # Load Manus prompt
            if manus_file.exists():
                with open(manus_file, "r") as f:
                    prompts["tool_selector"] = f.read()
            else:
                prompts["tool_selector"] = (
                    "You are a tool selection AI. Choose appropriate tools for tasks."
                )

            # Load Cursor prompt
            if cursor_file.exists():
                with open(cursor_file, "r") as f:
                    prompts["analyst"] = f.read()
            else:
                prompts["analyst"] = (
                    "You are an analysis AI. Analyze results and provide insights."
                )

        except Exception as e:
            print(f"Error: Could not load prompts. {e}")
            # Provide fallback prompts
            prompts = {
                "planner": "You are a planning AI. Create step-by-step plans for tasks.",
                "tool_selector": "You are a tool selection AI. Choose appropriate tools for tasks.",
                "analyst": "You are an analysis AI. Analyze results and provide insights.",
            }
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
        """Executes the shell command and returns real output."""
        print(f"Executing: `{command}`")
        try:
            # SECURITY FIX: Use shlex.split to safely parse command without shell=True
            # This prevents command injection while maintaining functionality
            cmd_parts = shlex.split(command)
            result = subprocess.run(
                cmd_parts, capture_output=True, text=True, timeout=600
            )
            if result.returncode == 0:
                return result.stdout
            else:
                return f"[ERROR] Command failed: {result.stderr}"
        except Exception as e:
            return f"[ERROR] Exception during execution: {e}"

    def _analysis_phase(self, result: str) -> str:
        """Uses the 'analyst' prompt to interpret the results."""
        system_prompt = self.prompts["analyst"]
        user_prompt = f"Analyze the following tool output and provide a summary of key findings and recommendations:\n\n{result}"
        response = self.ollama.generate(user_prompt, system_prompt=system_prompt)
        return response
