import json
from pathlib import Path
from ai_integration import OllamaClient
import subprocess

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
            with open(self.prompt_dir / "Manus Agent Tools & Prompt/system.md", "r") as f:
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
        self.state['plan'] = plan
        print(f"Phase 1: Plan Created -> {plan}")

        # 2. Tool Selection Phase (using Manus' prompt)
        tool_command = self._tool_selection_phase(task_description, plan)
        self.state['tool_command'] = tool_command
        print(f"Phase 2: Tool Selected -> {tool_command}")

        # 3. Execution Phase (simulated)
        execution_result = self._execution_phase(tool_command)
        self.state['execution_result'] = execution_result
        print(f"Phase 3: Execution Result -> {execution_result[:100]}...")

        # 4. Analysis Phase (using Cursor's prompt)
        analysis = self._analysis_phase(execution_result)
        self.state['analysis'] = analysis
        print(f"Phase 4: Analysis Complete -> {analysis}")

        print("--- AI Task Pipeline Complete ---")
        return self.state

    def _planning_phase(self, task: str) -> str:
        """Uses the 'planner' prompt to create a high-level strategy."""
        system_prompt = self.prompts['planner']
        user_prompt = f"Create a step-by-step plan for the following task: {task}"
        response = self.ollama.generate(user_prompt, system_prompt=system_prompt)
        return response

    def _tool_selection_phase(self, task: str, plan: str) -> str:
        """Uses the 'tool_selector' prompt to choose the right command."""
        system_prompt = self.prompts['tool_selector']
        user_prompt = f"Given the task '{task}' and the plan '{plan}', what is the exact shell command to execute next? Only output the command."
        response = self.ollama.generate(user_prompt, system_prompt=system_prompt)
        return response
    
    def _execution_phase(self, command: str) -> str:
        """Executes the shell command and returns real output."""
        print(f"Executing: `{command}`")
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=600)
            if result.returncode == 0:
                return result.stdout
            else:
                return f"[ERROR] Command failed: {result.stderr}"
        except Exception as e:
            return f"[ERROR] Exception during execution: {e}"

    def _analysis_phase(self, result: str) -> str:
        """Uses the 'analyst' prompt to interpret the results."""
        system_prompt = self.prompts['analyst']
        user_prompt = f"Analyze the following tool output and provide a summary of key findings and recommendations:\n\n{result}"
        response = self.ollama.generate(user_prompt, system_prompt=system_prompt)
        return response 