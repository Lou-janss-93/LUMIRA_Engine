"""
LUMIRA - Lightweight Unified Modular Intelligence & Reasoning Architecture

A modern, modular framework for emotional analysis, context-aware computing,
and intelligent reasoning.
"""

__version__ = "2.0.0"
__author__ = "Louis Janssens"

# Core exports
from .engine import LumiraEngine, integrate_with_existing_efc
from .config import LUMIRAConfig, env_bool
from .types import (
    LUMIRAResult, PipelineStatus, TextSample, EmotionScore,
    IntegritySignal, RiskFlag, TrendPoint, AnalysisReport
)

__all__ = [
    "LumiraEngine",
    "integrate_with_existing_efc",
    "LUMIRAConfig",
    "env_bool",
    "LUMIRAResult",
    "PipelineStatus",
    "TextSample",
    "EmotionScore",
    "IntegritySignal",
    "RiskFlag",
    "TrendPoint",
    "AnalysisReport",
]