# ╔══════════════════════════════════════════════════════════╗
# ║ VulnForge - Built with Blood by DemonKing369.0 👑        ║
# ║ GitHub: https://github.com/Arunking9                     ║
# ║ AI-Powered Security Framework for Bug Bounty Warriors ⚔️║
# ╚══════════════════════════════════════════════════════════╝

#!/usr/bin/env python3
"""
VulnForge LLM Engine
Handles model management, fallbacks, and caching for AI operations
"""

import json
import logging
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
import httpx
from functools import lru_cache


class LLMEngine:
    def __init__(self, config_path: Optional[Path] = None):
        self.logger = logging.getLogger(__name__)
        self.base_url = "http://localhost:11434"
        self.config = self._load_config(config_path)
        self.models = self._initialize_models()
        self.current_model = self.models[0]  # Start with preferred model
        self.response_cache = {}

    def _load_config(self, config_path: Optional[Path] = None) -> Dict:
        """Load LLM configuration"""
        if not config_path:
            config_path = Path.home() / ".vulnforge" / "configs" / "llm_config.json"

        default_config = {
            "preferred_model": "deepseek-coder-v2:16b-lite-base-q5_K_S",
            "fallback_models": ["deepseek-coder:6.7b", "codellama:7b", "mistral:7b"],
            "cache_size": 100,
            "timeout": 180,
            "max_retries": 3,
            "retry_delay": 2,
        }

        try:
            if config_path.exists():
                with open(config_path) as f:
                    return {**default_config, **json.load(f)}
            return default_config
        except Exception as e:
            self.logger.error("Error loading LLM config: %s", e)
            self.config = {}

    def _initialize_models(self) -> List[str]:
        """Initialize available models"""
        available_models = []

        # Check preferred model first
        if self._is_model_available(self.config["preferred_model"]):
            available_models.append(self.config["preferred_model"])

        # Check fallback models
        for model in self.config["fallback_models"]:
            if self._is_model_available(model):
                available_models.append(model)

        if not available_models:
            self.logger.error("No models available!")

        return available_models

    async def _is_model_available(self, model: str) -> bool:
        """Check if a model is available"""
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                response = await client.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                models = response.json().get("models", [])
                return any(m["name"] == model for m in models)
        except (httpx.RequestError, httpx.TimeoutException) as e:
            self.logger.error("Error checking model availability: %s", e)
            return False
        return False

    def _pull_model(self, model: str) -> bool:
        """Pull a model if not available"""
        try:
            self.logger.info("Pulling model: %s", model)
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
            self.logger.error("Error pulling model %s: %s", model, e)
        return False

    @lru_cache(maxsize=100)
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
    ) -> Optional[str]:
        """Generate text (wrapper for query)"""
        return await self.query(prompt, system_prompt=system_prompt, model=model)

    async def query(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: Optional[str] = None,
        use_cache: bool = True,
    ) -> Optional[str]:
        if not model:
            model = self.current_model

        # Check cache if enabled
        cache_key = f"{model}:{prompt}:{system_prompt}"
        if use_cache and cache_key in self.response_cache:
            return self.response_cache[cache_key]

        for attempt in range(self.config["max_retries"]):
            try:
                data = {
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "top_p": 0.9,
                        "max_tokens": 4096,
                        "num_ctx": 8192,
                        "num_thread": 8,
                        "repeat_penalty": 1.1,
                    },
                }

                if system_prompt:
                    data["system"] = system_prompt

                async with httpx.AsyncClient(timeout=self.config["timeout"]) as client:
                    response = await client.post(
                        f"{self.base_url}/api/generate", json=data
                    )

                if response.status_code == 200:
                    result = response.json().get("response", "").strip()
                    if use_cache:
                        self.response_cache[cache_key] = result
                    return result

            except (httpx.RequestError, httpx.TimeoutException) as e:
                self.logger.error("Error querying model %s: %s", model, e)

            # Try next model if available
            if model in self.models:
                current_index = self.models.index(model)
                if current_index + 1 < len(self.models):
                    model = self.models[current_index + 1]
                    self.logger.info("Switching to fallback model: %s", model)
                else:
                    break

            await asyncio.sleep(self.config["retry_delay"])

        return None

    def clear_cache(self):
        """Clear the response cache"""
        self.response_cache.clear()
        self.query.cache_clear()

    def get_available_models(self) -> List[str]:
        """Get list of available models"""
        return self.models.copy()

    def set_preferred_model(self, model: str) -> bool:
        """Set preferred model if available"""
        if self._is_model_available(model):
            self.current_model = model
            return True
        return False
