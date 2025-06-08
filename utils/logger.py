"""
Logger module for VulnForge
Handles logging configuration and formatting
"""

import logging
import sys
from pathlib import Path
from rich.logging import RichHandler
from typing import Optional

def setup_logger(name: str = "vulnforge", level: int = logging.INFO) -> logging.Logger:
    """Setup logger with rich formatting"""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Create handlers
    console_handler = RichHandler(rich_tracebacks=True)
    file_handler = logging.FileHandler(Path.home() / ".vulnforge" / "logs" / "vulnforge.log")
    
    # Create formatters
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Set formatters
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    
    # Add handlers
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Get logger instance"""
    return logging.getLogger(name or "vulnforge") 