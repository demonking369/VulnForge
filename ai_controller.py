# ╔══════════════════════════════════════════════════════════╗
# ║ VulnForge - Built with Blood by DemonKing369.0 👑        ║
# ║ GitHub: https://github.com/Arunking9                     ║
# ║ AI-Powered Security Framework for Bug Bounty Warriors ⚔️ ║
# ╚══════════════════════════════════════════════════════════╝

import os
import json
import logging
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

# SECURITY: Import security utilities
from utils.security_utils import SecurityValidator, RateLimiter
from utils.auth import get_auth_manager, Permission

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

    @RateLimiter(max_calls=5, time_window=60)
    async def process_query(
        self,
        query: str,
        context: Optional[Dict[str, Any]] = None,
        session_id: Optional[str] = None,
        identifier: str = "default",
    ) -> Dict[str, Any]:
        """Process an AI query with authentication and rate limiting.

        Args:
            query: The query to process
            context: Optional context data
            session_id: Optional session ID for authentication
            identifier: Rate limit identifier

        Returns:
            Dictionary containing the response and metadata

        Raises:
            PermissionError: If authentication fails
        """
        # SECURITY: Validate input
        if not isinstance(query, str) or not query.strip():
            raise ValueError("Query must be a non-empty string")

        # SECURITY: Limit query length to prevent abuse
        if len(query) > 5000:
            raise ValueError("Query too long (max 5000 characters)")

        # SECURITY: Sanitize query for logging
        safe_query = SecurityValidator.sanitize_log_input(query[:100])
        self.logger.info("Processing AI query: %s...", safe_query)

        # SECURITY: Check authentication if session_id provided
        if session_id:
            auth_manager = get_auth_manager()
            auth_manager.require_permission(session_id, Permission.AI_QUERY)

        try:
            # Prepare context
            context_str = ""
            if context:
                # SECURITY: Validate context is a dict
                if not isinstance(context, dict):
                    raise ValueError("Context must be a dictionary")
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
                # Return an empty log list as the logger doesn't expose in-memory logs
                "logs": [],
                "prompt": prompt,
            }

        except ValueError as e:
            # SECURITY: Don't expose internal errors
            self.logger.error("Validation error: %s", str(e))
            raise
        except Exception as e:
            # SECURITY: Log but don't expose detailed error
            self.logger.error("Error processing query: %s", str(e))
            raise RuntimeError("Failed to process query")

    async def _get_ai_response(self, prompt: str) -> str:
        """Get response from AI model with timeout.

        Args:
            prompt: The prompt to send to the AI

        Returns:
            The AI's response

        Raises:
            TimeoutError: If request times out
        """
        try:
            # SECURITY: Implement timeout for AI requests
            async with asyncio.timeout(300):  # 5 minute timeout
                # TODO: Implement actual AI model call
                # For now, return a placeholder response
                return "This is a placeholder response. AI integration pending."

        except asyncio.TimeoutError:
            self.logger.error("AI request timed out")
            raise TimeoutError("AI request timed out after 300 seconds")
        except Exception as e:
            self.logger.error("Error getting AI response: %s", str(e))
            raise

    def _generate_report(self) -> Dict[str, str]:
        """Generate reports for the current session.

        Returns:
            Dictionary mapping report types to their file paths
        """
        self.logger.info("Generating reports in %s format...", self.output_format)

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
            self.logger.error("Error generating reports: %s", str(e))
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
                "AI setup complete. Available models: %s", [m["name"] for m in models]
            )
            return True
        except Exception as e:
            self.logger.error("Error in setup_ai: %s", e)
            return False
