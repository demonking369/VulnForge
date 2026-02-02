from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from enum import Enum
from pydantic import BaseModel
from pathlib import Path

class ToolMode(Enum):
    OFFENSIVE = "offensive"
    DEFENSIVE = "defensive"

class ToolCategory(Enum):
    RECON = "recon"
    EXPLOITATION = "exploitation"
    MONITORING = "monitoring"
    ANALYSIS = "analysis"

class ToolInput(BaseModel):
    target: str
    args: Dict[str, Any] = {}

class ToolResult(BaseModel):
    tool_name: str
    timestamp: str
    command: str
    raw_output: str
    structured_data: Dict[str, Any]
    error: Optional[str] = None

class BaseTool(ABC):
    def __init__(self, name: str, description: str, category: ToolCategory, mode: ToolMode):
        self.name = name
        self.description = description
        self.category = category
        self.mode = mode

    @abstractmethod
    def validate_input(self, input_data: ToolInput) -> bool:
        """Validate if the input is appropriate for this tool."""
        pass

    @abstractmethod
    def build_command(self, input_data: ToolInput) -> List[str]:
        """Construct the command line arguments."""
        pass

    @abstractmethod
    def parse_output(self, raw_output: str) -> Dict[str, Any]:
        """Parse raw terminal output into structured JSON."""
        pass
    
    @abstractmethod
    def check_installed(self) -> bool:
        """Check if the tool is installed on the system."""
        pass
