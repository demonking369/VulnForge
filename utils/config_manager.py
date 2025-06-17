#!/usr/bin/env python3
"""
VulnForge Configuration Manager
Handles persistent configuration settings
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional
import os

class ConfigManager:
    def __init__(self, base_dir: Path):
        """Initialize configuration manager.
        
        Args:
            base_dir: Base directory for configuration files (Path or str)
        """
        self.base_dir = Path(base_dir) if isinstance(base_dir, str) else base_dir
        self.logger = logging.getLogger(__name__)
        self.config_dir = self.base_dir / "configs"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.config_file = self.config_dir / "settings.json"
        self.config = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        default_config = {
            "ai": {
                "preferred_model": "deepseek-coder-v2:16b-lite-base-q5_K_S",
                "fallback_models": [
                    "deepseek-coder:6.7b",
                    "codellama:7b",
                    "mistral:7b"
                ],
                "cache_size": 100,
                "timeout": 180
            },
            "scanning": {
                "max_threads": 10,
                "timeout": 300,
                "rate_limit": {
                    "enabled": True,
                    "delay": 1
                }
            },
            "stealth": {
                "enabled": True,
                "user_agent_rotation": True,
                "proxy_rotation": False,
                "delay_range": [1.0, 3.0]
            },
            "reporting": {
                "default_format": "markdown",
                "include_screenshots": True,
                "save_raw_data": True
            },
            "notifications": {
                "enabled": False,
                "webhook_url": "",
                "email": {
                    "enabled": False,
                    "smtp_server": "",
                    "smtp_port": 587,
                    "username": "",
                    "password": ""
                },
                "discord": {
                    "enabled": False,
                    "webhook_url": ""
                }
            },
            "tools": {
                "nmap": {
                    "default_flags": ["-sS", "-T4", "--max-retries=1"],
                    "stealth_flags": ["-sS", "-T2", "-f"],
                    "aggressive_flags": ["-sS", "-T5", "-A"]
                },
                "subfinder": {
                    "sources": ["bevigil", "binaryedge", "bufferover", "c99", "censys"],
                    "timeout": 30
                },
                "httpx": {
                    "threads": 50,
                    "timeout": 10,
                    "follow_redirects": True
                },
                "nuclei": {
                    "update_templates": True,
                    "severity": ["critical", "high", "medium"],
                    "rate_limit": 150
                }
            }
        }
        
        try:
            if self.config_file.exists():
                with open(self.config_file) as f:
                    user_config = json.load(f)
                    # Deep merge with defaults
                    return self._deep_merge(default_config, user_config)
            return default_config
        except Exception as e:
            self.logger.error(f"Error loading config: {e}")
            return default_config
            
    def _deep_merge(self, default: Dict, user: Dict) -> Dict:
        """Deep merge two dictionaries"""
        result = default.copy()
        
        for key, value in user.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
                
        return result
        
    def save_config(self):
        """Save current configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving config: {e}")
            
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
                
        return value if value is not None else default
        
    def set(self, key: str, value: Any):
        """Set configuration value"""
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
            
        config[keys[-1]] = value
        self.save_config()
        
    def update(self, updates: Dict[str, Any]):
        """Update multiple configuration values"""
        self.config = self._deep_merge(self.config, updates)
        self.save_config()
        
    def reset(self):
        """Reset configuration to defaults"""
        self.config = self._load_config()
        self.save_config()
        
    def export(self, filepath: Path):
        """Export configuration to file"""
        try:
            with open(filepath, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error exporting config: {e}")
            
    def import_config(self, filepath: Path):
        """Import configuration from file"""
        try:
            with open(filepath) as f:
                imported_config = json.load(f)
                self.config = self._deep_merge(self.config, imported_config)
                self.save_config()
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
            "reporting.default_format"
        ]
        
        for key in required_keys:
            if self.get(key) is None:
                self.logger.error(f"Missing required config key: {key}")
                return False
                
        return True 