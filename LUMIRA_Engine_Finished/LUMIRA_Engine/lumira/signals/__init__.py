"""
LUMIRA Signals

Signal processing and analytics modules.
"""

from .light_store import LightweightSignalStore
from .analytics_light import (
    _moving_average, downhill_alert, analyze_emotion_trends, get_risk_summary
)

__all__ = [
    "LightweightSignalStore",
    "_moving_average",
    "downhill_alert", 
    "analyze_emotion_trends",
    "get_risk_summary",
]