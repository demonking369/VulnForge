"""
Logger utility for VulnForge
"""

import logging
import sys
from pathlib import Path
from rich.logging import RichHandler

def setup_logger(name: str = "vulnforge") -> logging.Logger:
    """Set up and configure logger"""
    logger = logging.getLogger(name)
    
    # Set log level
    logger.setLevel(logging.INFO)
    
    # Create handlers
    console_handler = RichHandler(rich_tracebacks=True)
    
    # Ensure log directory exists
    log_dir = Path.home() / ".vulnforge" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    file_handler = logging.FileHandler(
        log_dir / "vulnforge.log"
    )
    
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