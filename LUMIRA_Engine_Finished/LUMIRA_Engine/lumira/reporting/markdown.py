"""
LUMIRA Reporting Markdown

Markdown rendering for signal data reports.
"""

from .analyzer import Summary


def render_markdown(s: Summary) -> str:
    """
    Render a summary as markdown report.
    
    Args:
        s: Summary object to render
        
    Returns:
        Markdown formatted report string
    """
    lines = []
    lines.append(f"# LUMIRA Report — window {s.window_days} days")
    lines.append(f"_From: {s.from_ts}_  →  _To: {s.to_ts}_")
    lines.append("")
    
    lines.append("## Overview")
    lines.append(f"- Records: emotions={s.counts.get('emotions', 0)}, risks={s.counts.get('risks', 0)}, integrity={s.counts.get('integrity', 0)}")
    lines.append(f"- Avg joy: {s.joy_avg:.3f}")
    lines.append("")
    
    lines.append("## Top Emotions")
    for name, avg in s.top_emotions:
        lines.append(f"- {name}: {avg:.3f}")
    lines.append("")
    
    lines.append("## Risk Breakdown")
    if s.risk_breakdown:
        for k, v in sorted(s.risk_breakdown.items(), key=lambda x: (-x[1], x[0])):
            lines.append(f"- {k}: {v}")
    else:
        lines.append("- none")
    lines.append("")
    
    lines.append("## Recent Risk Highlights")
    if s.last_highlights.get("recent_risks"):
        for r in s.last_highlights["recent_risks"]:
            lines.append(f"- {r['ts']} — {r['kind']} [{r['level']}] (conf={r['conf']:.3f})")
    else:
        lines.append("- none")
    lines.append("")
    
    lines.append(f"## Incongruence signals: {s.last_highlights.get('incongruence', 0)}")
    lines.append("")
    
    lines.append("## Alert")
    if s.alert:
        lines.append(f"**{s.alert.get('severity', 'warning').upper()}** — {s.alert.get('reason')}  (riskΔ={s.alert.get('risk_trend', 0):.3f}, joyΔ={s.alert.get('joy_trend', 0):.3f})")
    else:
        lines.append("No downhill trend detected.")
    lines.append("")
    
    lines.append("> Disclaimer: LUMIRA is not a medical device. Non-diagnostic heuristics only.")
    
    return "\n".join(lines)
