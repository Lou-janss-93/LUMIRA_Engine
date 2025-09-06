"""
LUMIRA Reporting JSON

JSON rendering for signal data reports.
"""

from dataclasses import asdict
import json
from .analyzer import Summary


def render_json(s: Summary) -> str:
    """
    Render a summary as JSON report.
    
    Args:
        s: Summary object to render
        
    Returns:
        JSON formatted report string
    """
    return json.dumps(asdict(s), indent=2)
