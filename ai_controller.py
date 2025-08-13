# ╔══════════════════════════════════════════════════════════╗
# ║ VulnForge - Built with Blood by DemonKing369.0 👑        ║
# ║ GitHub: https://github.com/Arunking9                     ║
# ║ AI-Powered Security Framework for Bug Bounty Warriors ⚔️║
# ╚══════════════════════════════════════════════════════════╝

import os
import json
import logging
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

from utils.report_generator import ReportGenerator
from utils.logger import setup_logger
from utils.config_manager import ConfigManager
from utils.context_builder import ContextBuilder
from utils.notifier import Notifier


class AIController:
    """Controls AI operations and decision making."""

    def __init__(self, session_dir: str, config_path: str):
        """Initialize the AI controller.

        Args:
            session_dir: Directory to store session data
            config_path: Path to configuration file
        """
        self.session_dir = Path(session_dir)
        self.config = ConfigManager(config_path)
        self.logger = setup_logger("ai_controller")
        self.context_builder = ContextBuilder(self.session_dir)
        self.notifier = Notifier(session_dir, config_path)
        self.report_generator = ReportGenerator(self.session_dir)
        self.output_format = "all"  # Default output format

        # Initialize session data
        self.session_data = {
            "start_time": datetime.now().isoformat(),
            "modules": [],
            "tools": {},
            "findings": [],
            "execution_history": [],
            "ai_decisions": [],
            "errors": [],
        }

    async def process_query(
        self, query: str, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Process an AI query.

        Args:
            query: The query to process
            context: Optional context data

        Returns:
            Dictionary containing the response and metadata
        """
        self.logger.info(f"Processing AI query: {query}")

        try:
            # Prepare context
            context_str = ""
            if context:
                context_str = json.dumps(context, indent=2)

            # Create prompt
            prompt = f"""You are a security expert. Please provide guidance on the following query:
            
Query: {query}

Context:
{context_str}

Consider:
1. Security best practices
2. Common vulnerabilities
3. Tool recommendations
4. Step-by-step guidance
5. Safety considerations

Provide a detailed response:"""

            # Get AI response
            response = await self._get_ai_response(prompt)

            # Log response
            self.logger.info("AI response received")

            return {
                "answer": response,
                "logs": self.logger.get_logs(),
                "prompt": prompt,
            }

        except Exception as e:
            self.logger.error(f"Error processing query: {str(e)}")
            raise

    async def _get_ai_response(self, prompt: str) -> str:
        """Get response from AI model.

        Args:
            prompt: The prompt to send to the AI

        Returns:
            The AI's response
        """
        try:
            # TODO: Implement actual AI model call
            # For now, return a placeholder response
            return "This is a placeholder response. AI integration pending."

        except Exception as e:
            self.logger.error(f"Error getting AI response: {str(e)}")
            raise

    def _generate_report(self) -> Dict[str, str]:
        """Generate reports for the current session.

        Returns:
            Dictionary mapping report types to their file paths
        """
        self.logger.info(f"Generating reports in {self.output_format} format...")

        try:
            # Prepare context data
            context = {
                "target": {
                    "domain": self.session_data.get("target_domain"),
                    "ip": self.session_data.get("target_ip"),
                    "scan_time": self.session_data.get("start_time"),
                    "duration": self._calculate_duration(),
                },
                "modules": self.session_data["modules"],
                "tools": self.session_data["tools"],
                "vulnerabilities": self.session_data.get("findings", []),
                "exploits": self.session_data.get("execution_history", []),
                "defensive_measures": self.session_data.get("defensive_measures", []),
                "recommendations": self.session_data.get("recommendations", []),
                "errors": self.session_data["errors"],
            }

            # Generate reports
            report_paths = self.report_generator.generate_reports(
                context, self.output_format
            )

            self.logger.info("Reports generated successfully")
            return report_paths

        except Exception as e:
            self.logger.error(f"Error generating reports: {str(e)}")
            raise

    def _calculate_duration(self) -> str:
        """Calculate session duration.

        Returns:
            Formatted duration string
        """
        start_time = datetime.fromisoformat(self.session_data["start_time"])
        end_time = datetime.now()
        duration = end_time - start_time

        hours = duration.seconds // 3600
        minutes = (duration.seconds % 3600) // 60
        seconds = duration.seconds % 60

        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    def setup_ai(self) -> bool:
        """Setup AI environment: check Ollama service and model availability."""
        try:
            if hasattr(self, "ollama"):
                client = self.ollama
            else:
                from ai_integration import OllamaClient

                client = OllamaClient()
            if not client.is_available():
                self.logger.error(
                    "Ollama service not available. Start with: ollama serve"
                )
                return False
            models = client.list_models()
            if not models:
                self.logger.info("No models found. Pulling default model...")
                if not client.pull_model(client.main_model):
                    self.logger.error("Failed to pull default model")
                    return False
            self.logger.info(
                f"AI setup complete. Available models: {[m['name'] for m in models]}"
            )
            return True
        except Exception as e:
            self.logger.error(f"Error in setup_ai: {e}")
            return False
