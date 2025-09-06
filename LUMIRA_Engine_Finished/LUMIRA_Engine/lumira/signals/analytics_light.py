"""
LUMIRA Signals Analytics Light

Lightweight analytics for signal data.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import statistics


def _moving_average(values: List[float], window: int) -> List[float]:
    """
    Calculate moving average for a list of values.
    
    Args:
        values: List of numeric values
        window: Window size for moving average
        
    Returns:
        List of moving average values
    """
    if not values or window <= 0:
        return []
    
    if window >= len(values):
        return [statistics.mean(values)] * len(values)
    
    result = []
    for i in range(len(values)):
        start_idx = max(0, i - window + 1)
        end_idx = i + 1
        window_values = values[start_idx:end_idx]
        result.append(statistics.mean(window_values))
    
    return result


def downhill_alert(records: List[Dict[str, Any]], window_days: int = 7) -> Optional[Dict[str, Any]]:
    """
    Detect downhill trend alert based on risk and joy patterns.
    
    Heuristic: risk MA rising AND joy MA dropping across window → warning
    
    Args:
        records: List of signal records
        window_days: Number of days to analyze
        
    Returns:
        Alert dictionary if pattern detected, None otherwise
    """
    if not records:
        return None
    
    # Filter records to the specified window
    cutoff_date = datetime.now() - timedelta(days=window_days)
    recent_records = []
    
    for record in records:
        try:
            record_ts = datetime.fromisoformat(record["timestamp"])
            if record_ts >= cutoff_date:
                recent_records.append(record)
        except (ValueError, KeyError):
            continue
    
    if len(recent_records) < 3:  # Need at least 3 records for trend analysis
        return None
    
    # Sort by timestamp
    recent_records.sort(key=lambda x: datetime.fromisoformat(x["timestamp"]))
    
    # Extract emotion and risk data
    emotion_records = [r for r in recent_records if r.get("type") == "emotions"]
    risk_records = [r for r in recent_records if r.get("type") == "risks"]
    
    if not emotion_records or not risk_records:
        return None
    
    # Calculate daily averages for joy and risk
    daily_joy = _calculate_daily_emotion_average(emotion_records, "joy")
    daily_risk = _calculate_daily_risk_average(risk_records)
    
    if len(daily_joy) < 3 or len(daily_risk) < 3:
        return None
    
    # Calculate moving averages (window of 3 days)
    joy_ma = _moving_average(daily_joy, 3)
    risk_ma = _moving_average(daily_risk, 3)
    
    if len(joy_ma) < 2 or len(risk_ma) < 2:
        return None
    
    # Check for downhill trend
    joy_trend = _calculate_trend(joy_ma)
    risk_trend = _calculate_trend(risk_ma)
    
    # Alert if joy is decreasing AND risk is increasing
    if joy_trend < -0.1 and risk_trend > 0.1:  # Thresholds for trend detection
        return {
            "alert_type": "downhill_trend",
            "severity": "medium",
            "reason": "Joy decreasing and risk increasing over time",
            "window_days": window_days,
            "joy_trend": joy_trend,
            "risk_trend": risk_trend,
            "joy_ma": joy_ma,
            "risk_ma": risk_ma,
            "detected_at": datetime.now().isoformat()
        }
    
    return None


def _calculate_daily_emotion_average(emotion_records: List[Dict[str, Any]], emotion_name: str) -> List[float]:
    """Calculate daily average for a specific emotion."""
    daily_scores = {}
    
    for record in emotion_records:
        try:
            record_ts = datetime.fromisoformat(record["timestamp"])
            date_key = record_ts.date()
            
            if date_key not in daily_scores:
                daily_scores[date_key] = []
            
            # Extract emotion scores from data
            emotions = record.get("data", [])
            for emotion in emotions:
                if emotion.get("name") == emotion_name:
                    daily_scores[date_key].append(emotion.get("score", 0))
        except (ValueError, KeyError):
            continue
    
    # Convert to sorted list of daily averages
    daily_averages = []
    for date in sorted(daily_scores.keys()):
        if daily_scores[date]:
            daily_averages.append(statistics.mean(daily_scores[date]))
        else:
            daily_averages.append(0.0)
    
    return daily_averages


def _calculate_daily_risk_average(risk_records: List[Dict[str, Any]]) -> List[float]:
    """Calculate daily average risk score."""
    daily_scores = {}
    
    for record in risk_records:
        try:
            record_ts = datetime.fromisoformat(record["timestamp"])
            date_key = record_ts.date()
            
            if date_key not in daily_scores:
                daily_scores[date_key] = []
            
            # Extract risk scores from data
            risks = record.get("data", [])
            for risk in risks:
                confidence = risk.get("confidence", 0)
                level = risk.get("level", "low")
                
                # Convert level to numeric score
                level_score = {"low": 0.3, "medium": 0.6, "high": 0.9}.get(level, 0.3)
                daily_scores[date_key].append(confidence * level_score)
        except (ValueError, KeyError):
            continue
    
    # Convert to sorted list of daily averages
    daily_averages = []
    for date in sorted(daily_scores.keys()):
        if daily_scores[date]:
            daily_averages.append(statistics.mean(daily_scores[date]))
        else:
            daily_averages.append(0.0)
    
    return daily_averages


def _calculate_trend(values: List[float]) -> float:
    """Calculate trend slope using simple linear regression."""
    if len(values) < 2:
        return 0.0
    
    n = len(values)
    x = list(range(n))
    
    # Simple linear regression slope
    x_mean = statistics.mean(x)
    y_mean = statistics.mean(values)
    
    numerator = sum((x[i] - x_mean) * (values[i] - y_mean) for i in range(n))
    denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
    
    if denominator == 0:
        return 0.0
    
    return numerator / denominator


def analyze_emotion_trends(records: List[Dict[str, Any]], emotion_name: str, window_days: int = 7) -> Dict[str, Any]:
    """
    Analyze trends for a specific emotion.
    
    Args:
        records: List of signal records
        emotion_name: Name of emotion to analyze
        window_days: Number of days to analyze
        
    Returns:
        Emotion trend analysis
    """
    if not records:
        return {"trend": "no_data", "slope": 0.0, "values": []}
    
    # Filter emotion records
    emotion_records = [r for r in records if r.get("type") == "emotions"]
    
    if not emotion_records:
        return {"trend": "no_data", "slope": 0.0, "values": []}
    
    # Calculate daily averages
    daily_values = _calculate_daily_emotion_average(emotion_records, emotion_name)
    
    if len(daily_values) < 2:
        return {"trend": "insufficient_data", "slope": 0.0, "values": daily_values}
    
    # Calculate trend
    slope = _calculate_trend(daily_values)
    
    # Determine trend direction
    if slope > 0.1:
        trend = "increasing"
    elif slope < -0.1:
        trend = "decreasing"
    else:
        trend = "stable"
    
    return {
        "trend": trend,
        "slope": slope,
        "values": daily_values,
        "window_days": window_days,
        "emotion": emotion_name
    }


def get_risk_summary(records: List[Dict[str, Any]], window_days: int = 7) -> Dict[str, Any]:
    """
    Get risk summary for the specified window.
    
    Args:
        records: List of signal records
        window_days: Number of days to analyze
        
    Returns:
        Risk summary
    """
    if not records:
        return {"total_risks": 0, "by_level": {}, "by_kind": {}}
    
    # Filter risk records
    risk_records = [r for r in records if r.get("type") == "risks"]
    
    if not risk_records:
        return {"total_risks": 0, "by_level": {}, "by_kind": {}}
    
    # Count risks by level and kind
    by_level = {}
    by_kind = {}
    total_risks = 0
    
    for record in risk_records:
        risks = record.get("data", [])
        for risk in risks:
            total_risks += 1
            level = risk.get("level", "unknown")
            kind = risk.get("kind", "unknown")
            
            by_level[level] = by_level.get(level, 0) + 1
            by_kind[kind] = by_kind.get(kind, 0) + 1
    
    return {
        "total_risks": total_risks,
        "by_level": by_level,
        "by_kind": by_kind,
        "window_days": window_days
    }