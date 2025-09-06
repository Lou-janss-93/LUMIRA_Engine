"""
Type definitions for LUMIRA engine.
"""

from typing import Dict, List, Any, Union, Optional, Literal
from dataclasses import dataclass
from enum import Enum


class PipelineStatus(Enum):
    """Pipeline execution status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class EmotionType(Enum):
    """Types of emotions."""
    JOY = "joy"
    SADNESS = "sadness"
    ANGER = "anger"
    FEAR = "fear"
    SURPRISE = "surprise"
    DISGUST = "disgust"
    TRUST = "trust"
    ANTICIPATION = "anticipation"


class ContextType(Enum):
    """Types of context analysis."""
    DOMAIN = "domain"
    TEMPORAL = "temporal"
    SPATIAL = "spatial"
    SOCIAL = "social"
    CULTURAL = "cultural"


class SafetyLevel(Enum):
    """Safety levels for content."""
    SAFE = "safe"
    WARNING = "warning"
    UNSAFE = "unsafe"
    BLOCKED = "blocked"


@dataclass
class LUMIRAResult:
    """Result of LUMIRA processing."""
    input_text: str
    context: Dict[str, Any]
    options: Dict[str, Any]
    status: str
    modules: Dict[str, Any]
    final_score: float
    recommendations: List[str]
    metadata: Dict[str, Any]
    error: Optional[str] = None
