"""
Logger utility for VulnForge
"""

# ╔══════════════════════════════════════════════════════════╗
# ║ VulnForge - Built with Blood by DemonKing369.0 👑        ║
# ║ GitHub: https://github.com/Arunking9                     ║
# ║ AI-Powered Security Framework for Bug Bounty Warriors ⚔️║
# ╚══════════════════════════════════════════════════════════╝

import logging
import sys
from pathlib import Path
from rich.logging import RichHandler
import os
from datetime import datetime

def setup_logger(name: str, log_dir: str, log_file: str = None) -> logging.Logger:
    """Setup logger with file and console handlers.
    
    Args:
        name: Logger name
        log_dir: Directory to store log files
        log_file: Optional specific log file name
        
    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Create log directory if it doesn't exist
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)
    
    # Create file handler
    if log_file is None:
        log_file = f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    file_handler = logging.FileHandler(log_path / log_file)
    file_handler.setLevel(logging.INFO)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    # Add watermark to log file
    watermark = """# VulnForge Session Log - Authored by DemonKing369.0
# Session started at: {timestamp}
# GitHub: https://github.com/Arunking9
# ===================================================
""".format(timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    with open(log_path / log_file, 'r+') as f:
        content = f.read()
        f.seek(0, 0)
        f.write(watermark + content)
    
    return logger 