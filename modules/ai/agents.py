from typing import List, Dict, Any, Optional
import json
from modules.ai.ai_integration import OllamaClient
from modules.orchestration.execution_manager import ExecutionManager, ScanRequest
from modules.orchestration.data_models import SessionContext, ToolExecutionResult, Finding

class NRPlanner:
    def __init__(self, ollama: OllamaClient):
        self.ollama = ollama
        
    async def create_plan(self, task: str, available_tools: List[Dict]) -> List[ScanRequest]:
        """
        Generates a list of tool executions to achieve the task.
        """
        tools_desc = "\n".join([f"- {t['name']}: {t['description']} (Mode: {t['mode']})" for t in available_tools])
        
        prompt = f"""
        You are the Planner for NeuroRift Security System.
        Goal: {task}
        
        Available Tools:
        {tools_desc}
        
        Create a logical execution plan.
        Return a JSON array of steps. Each step must have:
        - tool_name: exact name from list
        - target: target from goal
        - args: dictionary of arguments
        - reasoning: why this step is needed
        
        Example:
        [
            {{"tool_name": "nmap", "target": "example.com", "args": {{"flags": ["-F"]}}, "reasoning": "Quick scan to find open ports"}}
        ]
        """
        
        response = await self.ollama.generate(prompt)
        try:
            # Basic parsing of JSON from response (handling potential markdown code blocks)
            cleaned = response.replace("```json", "").replace("```", "").strip()
            plan_data = json.loads(cleaned)
            
            requests = []
            for step in plan_data:
                # Ensure target is present, if not use task mentions or safe default (should be handled by AI)
                req = ScanRequest(
                    tool_name=step['tool_name'],
                    target=step.get('target', 'unknown'),
                    args=step.get('args', {})
                )
                requests.append(req)
            return requests
        except Exception as e:
            print(f"Error parsing plan: {e}")
            return []

class NROperator:
    def __init__(self, execution_manager: ExecutionManager):
        self.manager = execution_manager
        
    async def execute_plan(self, requests: List[ScanRequest], context: SessionContext) -> List[ToolExecutionResult]:
        results = []
        for req in requests:
            # Here we could implement the human-in-the-loop check
            # For now, we assume pre-approval or we print to console
            print(f"\n[OPERATOR] Preparing to run: {req.tool_name} on {req.target}")
            
            # TODO: Add real approval mechanism via Web/CLI
            result = await self.manager.execute_tool(req, context)
            results.append(result)
            if result.status != "success":
                print(f"[OPERATOR] Step failed: {result.error}")
                break
        return results

class NRAnalyst:
    def __init__(self, ollama: OllamaClient):
        self.ollama = ollama
        
    async def analyze_results(self, results: List[ToolExecutionResult]) -> List[Finding]:
        if not results:
            return []
            
        context_str = ""
        for res in results:
            context_str += f"Tool: {res.tool_name}\nCommand: {res.command}\nOutput:\n{res.raw_output[:2000]}\n---\n"
            
        prompt = f"""
        You are the Analyst for NeuroRift.
        Analyze the following tool outputs and identify security findings.
        
        {context_str}
        
        Return a JSON array of findings. Each finding:
        - title
        - severity (CRITICAL, HIGH, MEDIUM, LOW, INFO)
        - description
        - tool_source
        """
        
        response = await self.ollama.generate(prompt)
        findings = []
        try:
            cleaned = response.replace("```json", "").replace("```", "").strip()
            data = json.loads(cleaned)
            for item in data:
                finding = Finding(
                    title=item['title'],
                    severity=item['severity'],
                    description=item['description'],
                    tool_source=item['tool_source'],
                    details=item
                )
                findings.append(finding)
        except Exception as e:
            print(f"Error parsing analysis: {e}")
            
        return findings

class NRScribe:
    def __init__(self, ollama: OllamaClient):
        self.ollama = ollama

    async def generate_report(self, task: str, findings: List[Finding]) -> str:
        findings_text = "\n".join([f"- [{f.severity}] {f.title}: {f.description}" for f in findings])
        
        prompt = f"""
        Generate a professional security report for the task: {task}
        
        Findings:
        {findings_text}
        
        Format as Markdown. Include Executive Summary, Technical Details, and Recommendations.
        """
        return await self.ollama.generate(prompt)
