"""
LUMIRA Safety Detector

Safety detection and risk assessment modules.

IMPORTANT: This is a non-clinical, rule-based safety detector.
It is NOT a medical diagnostic tool and should NOT be used for
clinical assessment or treatment decisions. For professional
mental health support, please contact appropriate medical services.
"""

import re
from typing import Dict, Any, List, Optional
from datetime import datetime

from ..types import TextSample, RiskFlag, IntegritySignal


# Self-harm terms (safe, non-graphic)
SELF_HARM_TERMS = {
    "self_harm_general": [
        "hurt myself", "harm myself", "hurt myself", "self harm", "self-harm",
        "cut myself", "cutting", "burn myself", "burning", "hit myself",
        "hit myself", "punch myself", "scratch myself", "bite myself",
        "self injury", "self-injury", "self mutilation", "self-mutilation",
        "self destructive", "self-destructive", "self sabotage", "self-sabotage",
        "zelfbeschadiging", "zichzelf pijn doen", "zichzelf verwonden"
    ],
    "suicide_intent": [
        "kill myself", "end my life", "end it all", "not want to live",
        "better off dead", "world without me", "disappear forever",
        "suicide", "take my own life", "end myself", "not here anymore",
        "give up", "give up on life", "life not worth living",
        "nothing to live for", "no point living", "wish I was dead",
        "want to die", "ready to die", "time to die", "end this",
        "zelfmoord", "eigen leven beëindigen", "niet meer willen leven",
        "opgeven", "geen zin meer in leven"
    ],
    "self_hate": [
        "hate myself", "despise myself", "loathe myself", "disgusted with myself",
        "worthless", "useless", "pathetic", "stupid", "idiot", "failure",
        "loser", "waste of space", "burden", "disappointment", "let down",
        "not good enough", "never good enough", "always mess up", "ruin everything",
        "everyone hates me", "nobody likes me", "better without me",
        "haat mezelf", "veracht mezelf", "waardeloos", "mislukking", "loser",
        "niemand houdt van me", "beter zonder mij"
    ],
    "isolation": [
        "alone", "lonely", "isolated", "nobody understands", "nobody cares",
        "no one to talk to", "no friends", "everyone left me", "abandoned",
        "rejected", "unwanted", "unloved", "forgotten", "invisible",
        "nobody notices", "nobody would miss me", "easier if I wasn't here",
        "alleen", "eenzaam", "geïsoleerd", "niemand begrijpt me", "niemand geeft om me",
        "verlaten", "vergeten", "onzichtbaar"
    ],
    "hopelessness": [
        "hopeless", "no hope", "never get better", "always be like this",
        "nothing will change", "stuck forever", "no way out", "trapped",
        "no future", "no point", "pointless", "meaningless", "empty",
        "numb", "dead inside", "feel nothing", "can't feel anything",
        "hopeloos", "geen hoop", "wordt nooit beter", "geen uitweg",
        "geen toekomst", "zinloos", "leeg", "voel niets"
    ]
}

# Escalation patterns (high risk indicators)
ESCALATION_PATTERNS = [
    r'\b(plan|planning|planned|plans)\b.*\b(suicide|kill|end|die)\b',
    r'\b(method|way|how)\b.*\b(suicide|kill|end|die)\b',
    r'\b(when|where|time)\b.*\b(suicide|kill|end|die)\b',
    r'\b(tonight|today|tomorrow|soon)\b.*\b(suicide|kill|end|die)\b',
    r'\b(goodbye|farewell|last time|final)\b',
    r'\b(letter|note|message)\b.*\b(suicide|kill|end|die)\b'
]


class SafetyDetector:
    """
    Safety detector for content analysis.
    
    IMPORTANT: This is a non-clinical, rule-based safety detector.
    It is NOT a medical diagnostic tool and should NOT be used for
    clinical assessment or treatment decisions.
    
    Provides safety detection and risk assessment capabilities
    for the LUMIRA framework.
    """
    
    def __init__(self):
        """Initialize the safety detector."""
        self.self_harm_terms = SELF_HARM_TERMS
        self.escalation_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in ESCALATION_PATTERNS]
    
    def analyze(self, sample: TextSample) -> List[RiskFlag]:
        """
        Analyze text sample for safety concerns.
        
        Args:
            sample: Text sample to analyze
            
        Returns:
            List of risk flags with levels and confidence scores
        """
        text = sample.text.lower()
        risks = []
        
        # Check each category
        for category, terms in self.self_harm_terms.items():
            matches = []
            for term in terms:
                if term in text:
                    matches.append(term)
            
            if matches:
                # Calculate confidence based on number of matches and text length
                confidence = min(1.0, len(matches) / max(1, len(text.split()) / 10))
                
                # Determine risk level
                if category == "suicide_intent":
                    level = "high" if confidence > 0.3 else "medium" if confidence > 0.1 else "low"
                    kind = "suicide-intent"
                elif category == "self_harm_general":
                    level = "medium" if confidence > 0.2 else "low"
                    kind = "self-harm-ideation"
                elif category == "self_hate":
                    level = "medium" if confidence > 0.3 else "low"
                    kind = "self-hate"
                else:
                    level = "low"
                    kind = "isolation" if category == "isolation" else "hopelessness"
                
                # Check for escalation patterns
                escalation_found = any(pattern.search(sample.text) for pattern in self.escalation_patterns)
                if escalation_found and category == "suicide_intent":
                    level = "high"
                    confidence = min(1.0, confidence + 0.3)
                
                # Create excerpt (max 160 chars)
                excerpt = self._create_excerpt(sample.text, matches[0])
                
                risks.append(RiskFlag(
                    kind=kind,
                    level=level,
                    confidence=confidence,
                    excerpt=excerpt,
                    ts=sample.ts
                ))
        
        # Sort by confidence (highest first)
        risks.sort(key=lambda x: x.confidence, reverse=True)
        
        return risks
    
    def escalate_if_needed(self, risks: List[RiskFlag], meta: Dict[str, Any] = None) -> List[IntegritySignal]:
        """
        Escalate risks to integrity signals if needed.
        
        Args:
            risks: List of risk flags
            meta: Optional metadata
            
        Returns:
            List of integrity signals for escalation
        """
        signals = []
        
        for risk in risks:
            if risk.kind == "suicide-intent" and risk.level == "high":
                signals.append(IntegritySignal(
                    level="critical",
                    reason="suicide-intent",
                    weight=1.0,
                    details={
                        "risk_flag": {
                            "kind": risk.kind,
                            "level": risk.level,
                            "confidence": risk.confidence,
                            "excerpt": risk.excerpt
                        },
                        "escalation_reason": "High confidence suicide intent detected",
                        "meta": meta or {}
                    }
                ))
            elif risk.kind == "self-harm-ideation" and risk.level == "medium":
                signals.append(IntegritySignal(
                    level="high",
                    reason="self-harm-ideation",
                    weight=0.8,
                    details={
                        "risk_flag": {
                            "kind": risk.kind,
                            "level": risk.level,
                            "confidence": risk.confidence,
                            "excerpt": risk.excerpt
                        },
                        "escalation_reason": "Medium confidence self-harm ideation detected",
                        "meta": meta or {}
                    }
                ))
        
        return signals
    
    def _create_excerpt(self, text: str, match_term: str) -> str:
        """Create a safe excerpt around the matched term (max 160 chars)."""
        # Find the position of the match
        match_pos = text.lower().find(match_term.lower())
        if match_pos == -1:
            return text[:160] + "..." if len(text) > 160 else text
        
        # Get context around the match (80 chars before and after)
        start = max(0, match_pos - 80)
        end = min(len(text), match_pos + len(match_term) + 80)
        
        excerpt = text[start:end]
        
        # Add ellipsis if truncated
        if start > 0:
            excerpt = "..." + excerpt
        if end < len(text):
            excerpt = excerpt + "..."
        
        # Ensure max 160 chars
        if len(excerpt) > 160:
            excerpt = excerpt[:157] + "..."
        
        return excerpt
    
    def get_safety_summary(self, risks: List[RiskFlag]) -> Dict[str, Any]:
        """
        Get a summary of safety analysis results.
        
        Args:
            risks: List of risk flags
            
        Returns:
            Safety summary dictionary
        """
        if not risks:
            return {
                "overall_risk": "none",
                "highest_level": "none",
                "total_risks": 0,
                "categories": {}
            }
        
        # Count by level and kind
        levels = {}
        kinds = {}
        
        for risk in risks:
            levels[risk.level] = levels.get(risk.level, 0) + 1
            kinds[risk.kind] = kinds.get(risk.kind, 0) + 1
        
        # Determine overall risk level
        if "high" in levels:
            overall_risk = "high"
        elif "medium" in levels:
            overall_risk = "medium"
        else:
            overall_risk = "low"
        
        return {
            "overall_risk": overall_risk,
            "highest_level": max(levels.keys()) if levels else "none",
            "total_risks": len(risks),
            "by_level": levels,
            "by_kind": kinds,
            "highest_confidence": max(risk.confidence for risk in risks) if risks else 0.0
        }