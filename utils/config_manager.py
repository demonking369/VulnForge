#!/usr/bin/env python3
"""
Configuration Manager for VulnForge
Handles loading and managing configuration settings
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional
import os


class ConfigManager:
    def __init__(self, config_path: str):
        self.logger = logging.getLogger(__name__)
        self.config_path = Path(config_path)
        self.config_dir = self.config_path.parent / "configs"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        try:
            if self.config_path.exists():
                with open(self.config_path, "r") as f:
                    return json.load(f)
            else:
                self.logger.warning(f"Config file not found: {self.config_path}")
                return {}
        except Exception as e:
            self.logger.error(f"Error loading config: {e}")
            return {}

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self.config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set configuration value"""
        self.config[key] = value
        self._save_config()

    def _save_config(self) -> None:
        """Save configuration to file"""
        try:
            with open(self.config_path, "w") as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving config: {e}")

    def get_ai_config(self) -> Dict[str, Any]:
        """Get AI configuration"""
        return self.config.get("ai", {})

    def get_notification_config(self) -> Dict[str, Any]:
        """Get notification configuration"""
        return self.config.get("notifications", {})

    def get_tool_config(self, tool_name: str) -> Dict[str, Any]:
        """Get tool-specific configuration"""
        return self.config.get("tools", {}).get(tool_name, {})

    def save_config(self):
        """Save current configuration to file"""
        try:
            with open(self.config_path, "w") as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving config: {e}")

    def update(self, updates: Dict[str, Any]):
        """Update multiple configuration values"""
        self.config = {**self.config, **updates}
        self._save_config()

    def reset(self):
        """Reset configuration to defaults"""
        self.config = self._load_config()
        self._save_config()

    def export(self, filepath: Path):
        """Export configuration to file"""
        try:
            with open(filepath, "w") as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error exporting config: {e}")

    def import_config(self, filepath: Path):
        """Import configuration from file"""
        try:
            with open(filepath) as f:
                imported_config = json.load(f)
                self.config = {**self.config, **imported_config}
                self._save_config()
        except Exception as e:
            self.logger.error(f"Error importing config: {e}")

    def get_all(self) -> Dict[str, Any]:
        """Get complete configuration"""
        return self.config.copy()

    def validate(self) -> bool:
        """Validate configuration"""
        required_keys = [
            "ai.preferred_model",
            "scanning.max_threads",
            "stealth.enabled",
            "reporting.default_format",
        ]

        for key in required_keys:
            if self.get(key) is None:
                self.logger.error(f"Missing required config key: {key}")
                return False

        return True
