"""
LUMIRA Reporting Analyzer

Analysis functions for signal data reporting.
"""

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from collections import defaultdict

from ..signals.light_store import LightweightSignalStore
from ..signals.analytics_light import downhill_alert


@dataclass
class Summary:
    """Summary of signal data analysis."""
    window_days: int
    from_ts: str
    to_ts: str
    counts: Dict[str, int]
    joy_avg: float
    top_emotions: List[tuple]  # [(name, avg_score), ...]
    risk_breakdown: Dict[str, int]  # by kind+level
    last_highlights: Dict[str, Any]
    alert: Optional[Dict[str, Any]]


def _slice(records: List[dict], days: int) -> List[dict]:
    """Slice records to the last N days."""
    now = datetime.utcnow()
    cutoff = now - timedelta(days=days)
    return [r for r in records if datetime.fromisoformat(r["timestamp"]) >= cutoff]


def _aggregate(records: List[dict]) -> Dict[str, Any]:
    """Aggregate records into summary statistics."""
    counts = {"emotions": 0, "risks": 0, "integrity": 0}
    em_scores = defaultdict(list)
    risk_breakdown = defaultdict(int)
    last_highlights = {"recent_risks": [], "incongruence": 0}
    
    for r in records:
        counts[r["type"]] = counts.get(r["type"], 0) + 1
        
        if r["type"] == "emotions":
            # Process emotion data
            for emotion in r.get("data", []):
                name = emotion.get("name", "?")
                score = float(emotion.get("score", 0.0))
                em_scores[name].append(score)
                
        elif r["type"] == "risks":
            # Process risk data
            for risk in r.get("data", []):
                kind = risk.get("kind", "?")
                level = risk.get("level", "low")
                rk = f'{kind}:{level}'
                risk_breakdown[rk] += 1
                
                if len(last_highlights["recent_risks"]) < 10:
                    last_highlights["recent_risks"].append({
                        "ts": r["timestamp"],
                        "kind": kind,
                        "level": level,
                        "conf": risk.get("confidence", 0.0)
                    })
                    
        elif r["type"] == "integrity":
            # Process integrity data
            for signal in r.get("data", []):
                if signal.get("reason") == "future_tense_negation":
                    last_highlights["incongruence"] += 1
    
    # Calculate averages
    top = sorted(
        [(k, sum(v) / len(v)) for k, v in em_scores.items() if v],
        key=lambda x: x[1],
        reverse=True
    )[:5]
    
    joy_avg = 0.0
    for k, v in top:
        if k == "joy":
            joy_avg = v
    
    return {
        "counts": counts,
        "top_emotions": top,
        "joy_avg": joy_avg,
        "risk_breakdown": dict(risk_breakdown),
        "last_highlights": last_highlights
    }


def make_summary(store_path: str, window_days: int = 7) -> Summary:
    """
    Create a summary of signal data for the specified window.
    
    Args:
        store_path: Path to the signal store
        window_days: Number of days to analyze
        
    Returns:
        Summary object with analysis results
    """
    st = LightweightSignalStore(store_path)
    allrec = st.load()
    rec = _slice(allrec, window_days)
    agg = _aggregate(rec)
    alert = downhill_alert(rec, window_days=window_days)
    
    now = datetime.utcnow().isoformat()
    from_ts = (datetime.utcnow() - timedelta(days=window_days)).isoformat()
    
    return Summary(
        window_days=window_days,
        from_ts=from_ts,
        to_ts=now,
        counts=agg["counts"],
        joy_avg=agg["joy_avg"],
        top_emotions=agg["top_emotions"],
        risk_breakdown=agg["risk_breakdown"],
        last_highlights=agg["last_highlights"],
        alert=alert
    )
