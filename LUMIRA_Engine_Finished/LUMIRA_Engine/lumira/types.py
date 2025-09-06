"""
LUMIRA Types

Type definitions for the LUMIRA framework.
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, date


class PipelineStatus(Enum):
    """Pipeline execution status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class LUMIRAResult:
    """Result of LUMIRA processing."""
    input_text: str
    context: Dict[str, Any]
    status: PipelineStatus
    result: Dict[str, Any]
    metadata: Dict[str, Any]
    error: Optional[str] = None


@dataclass
class TextSample:
    """Text sample for analysis."""
    id: str
    ts: datetime
    source: str
    text: str
    meta: Dict[str, Any]


@dataclass
class EmotionScore:
    """Emotion score result."""
    name: str
    score: float


@dataclass
class IntegritySignal:
    """Integrity signal for content validation."""
    level: str
    reason: str
    weight: float = 1.0
    details: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.details is None:
            self.details = {}


@dataclass
class RiskFlag:
    """Risk flag for safety assessment."""
    kind: str
    level: str
    confidence: float
    excerpt: str
    ts: datetime


@dataclass
class TrendPoint:
    """Trend point for analytics."""
    date: date
    metric: str
    value: float


@dataclass
class AnalysisReport:
    """Complete analysis report."""
    sample_id: str
    emotions: List[EmotionScore]
    integrity: List[IntegritySignal]
    risks: List[RiskFlag]
