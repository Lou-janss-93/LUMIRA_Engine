"""
LUMIRA Configuration

Configuration management for the LUMIRA framework.
"""

import os
from typing import Dict, Any, Optional
from dataclasses import dataclass


def env_bool(name: str, default: bool = False) -> bool:
    """
    Get boolean value from environment variable.
    
    Args:
        name: Environment variable name
        default: Default value if not set
        
    Returns:
        Boolean value from environment
    """
    value = os.getenv(name, str(default)).lower()
    return value in ('true', '1', 'yes', 'on', 'enabled')


@dataclass
class LUMIRAConfig:
    """
    LUMIRA configuration class.
    
    Manages configuration settings for the LUMIRA framework.
    """
    
    # Feature flags
    LUMIRA_ENABLED: bool = False
    LUMIRA_SEMANTICS_ENABLED: bool = False
    LUMIRA_SAFETY_ENABLED: bool = False
    LUMIRA_SIGNALS_ENABLED: bool = False
    
    # Data paths
    LUMIRA_DATA_DIR: str = ".lumira"
    LUMIRA_DB_PATH: str = ".lumira/signals.jsonl"
    
    # AI Provider settings
    ai_provider: str = "ollama"
    model: str = "llama2"
    max_retries: int = 3
    timeout: float = 30.0
    
    # Logging settings
    log_level: str = "INFO"
    log_file: Optional[str] = None
    
    def __post_init__(self):
        """Load configuration from environment variables."""
        # Feature flags
        self.LUMIRA_ENABLED = env_bool("LUMIRA_ENABLED", self.LUMIRA_ENABLED)
        self.LUMIRA_SEMANTICS_ENABLED = env_bool("LUMIRA_SEMANTICS_ENABLED", self.LUMIRA_SEMANTICS_ENABLED)
        self.LUMIRA_SAFETY_ENABLED = env_bool("LUMIRA_SAFETY_ENABLED", self.LUMIRA_SAFETY_ENABLED)
        self.LUMIRA_SIGNALS_ENABLED = env_bool("LUMIRA_SIGNALS_ENABLED", self.LUMIRA_SIGNALS_ENABLED)
        
        # Data paths
        self.LUMIRA_DATA_DIR = os.getenv("LUMIRA_DATA_DIR", self.LUMIRA_DATA_DIR)
        self.LUMIRA_DB_PATH = os.getenv("LUMIRA_DB_PATH", self.LUMIRA_DB_PATH)
        
        # AI Provider settings
        self.ai_provider = os.getenv("LUMIRA_AI_PROVIDER", self.ai_provider)
        self.model = os.getenv("LUMIRA_MODEL", self.model)
        self.max_retries = int(os.getenv("LUMIRA_MAX_RETRIES", str(self.max_retries)))
        self.timeout = float(os.getenv("LUMIRA_TIMEOUT", str(self.timeout)))
        
        # Logging settings
        self.log_level = os.getenv("LUMIRA_LOG_LEVEL", self.log_level)
        self.log_file = os.getenv("LUMIRA_LOG_FILE", self.log_file)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            "LUMIRA_ENABLED": self.LUMIRA_ENABLED,
            "LUMIRA_SEMANTICS_ENABLED": self.LUMIRA_SEMANTICS_ENABLED,
            "LUMIRA_SAFETY_ENABLED": self.LUMIRA_SAFETY_ENABLED,
            "LUMIRA_SIGNALS_ENABLED": self.LUMIRA_SIGNALS_ENABLED,
            "LUMIRA_DATA_DIR": self.LUMIRA_DATA_DIR,
            "LUMIRA_DB_PATH": self.LUMIRA_DB_PATH,
            "ai_provider": self.ai_provider,
            "model": self.model,
            "max_retries": self.max_retries,
            "timeout": self.timeout,
            "log_level": self.log_level,
            "log_file": self.log_file,
        }
