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

class OllamaClient:
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.logger = logging.getLogger(__name__)
        self.default_model = "deepseek-coder-v2:16b-lite-base-q5_K_S"
        self.backup_models = [
            "deepseek-coder:6.7b",
            "codellama:7b",
            "mistral:7b"
        ]
        
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
                return response.json().get('models', [])
        except Exception as e:
            self.logger.error(f"Error listing models: {e}")
        return []
        
    def pull_model(self, model: str) -> bool:
        """Pull a model if not available"""
        try:
            self.logger.info(f"Pulling model: {model}")
            data = {"name": model}
            response = requests.post(f"{self.base_url}/api/pull", json=data, stream=True)
            
            for line in response.iter_lines():
                if line:
                    try:
                        status = json.loads(line.decode('utf-8'))
                        if status.get('status') == 'success':
                            return True
                    except:
                        continue
        except Exception as e:
            self.logger.error(f"Error pulling model {model}: {e}")
        return False
        
    def generate(self, prompt: str, model: str = None, system_prompt: str = None) -> Optional[str]:
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
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "max_tokens": 4096,  # Increased for better code generation
                    "num_ctx": 8192,     # Increased context window
                    "num_thread": 8,      # Optimize for multi-core systems
                    "repeat_penalty": 1.1  # Slightly reduce repetition
                }
            }
            
            if system_prompt:
                data["system"] = system_prompt
                
            response = requests.post(f"{self.base_url}/api/generate", json=data, timeout=180)  # Increased timeout
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', '').strip()
            else:
                self.logger.error(f"Ollama API error: {response.status_code}")
                
        except Exception as e:
            self.logger.error(f"Error generating with Ollama: {e}")
            
        return None
        
    def get_best_model(self) -> Optional[str]:
        """Get the best available model"""
        available_models = [m['name'] for m in self.list_models()]
        
        # Check default model first (deepseek-coder-v2)
        if self.default_model in available_models:
            return self.default_model
            
        # Check backup models
        for model in self.backup_models:
            if model in available_models:
                return model
                
        # If no preferred models, return first available
        if available_models:
            return available_models[0]
            
        return None


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
                json_match = re.search(r'```json\n(.*?)\n```', response, re.DOTALL)
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
        
        headers = response_data.get('headers', {})
        content = response_data.get('content', '')[:2000]  # Limit content length
        
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
                json_match = re.search(r'```json\n(.*?)\n```', response, re.DOTALL)
                if json_match:
                    try:
                        return json.loads(json_match.group(1))
                    except:
                        pass
                        
        return {"error": "Failed to analyze web response", "raw_response": response}
        
    def fix_broken_tool(self, tool_name: str, error_output: str, source_code: str = None) -> str:
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
                return result.get('prioritized_vulnerabilities', vulnerabilities)
            except:
                pass
                
        return vulnerabilities


class AIOrchestrator:
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.ollama = OllamaClient()
        self.analyzer = AIAnalyzer(self.ollama)
        self.logger = logging.getLogger(__name__)
        
    def setup_ai(self) -> bool:
        """Setup AI environment"""
        if not self.ollama.is_available():
            self.logger.error("Ollama service not available. Start with: ollama serve")
            return False
            
        # Ensure we have at least one model
        models = self.ollama.list_models()
        if not models:
            self.logger.info("No models found. Pulling default model...")
            if not self.ollama.pull_model(self.ollama.default_model):
                self.logger.error("Failed to pull default model")
                return False
                
        self.logger.info(f"AI setup complete. Available models: {[m['name'] for m in models]}")
        return True
        
    def generate_attack_strategy(self, target_info: Dict) -> Dict[str, Any]:
        """Generate comprehensive attack strategy"""
        system_prompt = """You are a senior penetration tester creating attack strategies.
        Generate comprehensive, methodical attack plans based on reconnaissance data."""
        
        prompt = f"""
        Based on this reconnaissance data, create a comprehensive attack strategy:
        
        Target Information: {json.dumps(target_info, indent=2)}
        
        Generate attack strategy with:
        1. Attack phases (reconnaissance, scanning, exploitation, post-exploitation)
        2. Specific tools and techniques for each phase
        3. Priority targets and attack vectors
        4. Potential exploit chains
        5. Risk assessment
        6. Timeline and resource requirements
        
        Format as JSON:
        {{
            "attack_phases": [
                {{
                    "phase": "phase name",
                    "objectives": ["what to achieve"],
                    "tools": ["specific tools to use"],
                    "techniques": ["attack techniques"],
                    "expected_duration": "time estimate",
                    "success_indicators": ["how to know if successful"]
                }}
            ],
            "priority_targets": ["highest value targets"],
            "attack_vectors": ["main attack paths"],
            "exploit_chains": ["potential exploit combinations"],
            "risk_level": "low/medium/high",
            "recommendations": ["strategic recommendations"]
        }}
        """
        
        response = self.ollama.generate(prompt, system_prompt=system_prompt)
        if response:
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                json_match = re.search(r'```json\n(.*?)\n```', response, re.DOTALL)
                if json_match:
                    try:
                        return json.loads(json_match.group(1))
                    except:
                        pass
                        
        return {"error": "Failed to generate attack strategy"}


# CLI interface for AI module
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="VulnForge AI Module")
    parser.add_argument("--test-connection", action="store_true", help="Test Ollama connection")
    parser.add_argument("--pull-model", help="Pull a specific model")
    parser.add_argument("--list-models", action="store_true", help="List available models")
    parser.add_argument("--analyze-nmap", help="Analyze nmap output file")
    
    args = parser.parse_args()
    
    orchestrator = AIOrchestrator(Path.home() / ".vulnforge")
    
    if args.test_connection:
        if orchestrator.setup_ai():
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
        with open(args.analyze_nmap, 'r') as f:
            content = f.read()
        result = orchestrator.analyzer.analyze_nmap_output(content)
        print(json.dumps(result, indent=2))