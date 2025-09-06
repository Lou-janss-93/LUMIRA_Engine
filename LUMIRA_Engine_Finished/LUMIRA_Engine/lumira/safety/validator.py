"""
Safety Validator

Comprehensive safety validation for text content including
content filtering, risk assessment, and safety checks.
"""

import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

from ..utils.logging import get_logger


class SafetyLevel(Enum):
    """Safety levels for content."""
    SAFE = "safe"
    WARNING = "warning"
    UNSAFE = "unsafe"
    BLOCKED = "blocked"


class RiskType(Enum):
    """Types of safety risks."""
    HARMFUL_CONTENT = "harmful_content"
    INAPPROPRIATE_LANGUAGE = "inappropriate_language"
    PERSONAL_INFORMATION = "personal_information"
    SENSITIVE_TOPICS = "sensitive_topics"
    VIOLENCE = "violence"
    HATE_SPEECH = "hate_speech"
    SPAM = "spam"
    MALWARE = "malware"


@dataclass
class SafetyResult:
    """Result of safety validation."""
    is_safe: bool
    safety_level: SafetyLevel
    risk_score: float
    risks: List[RiskType]
    details: Dict[str, Any]
    metadata: Dict[str, Any]


class SafetyValidator:
    """
    Comprehensive safety validator for text content.
    
    Provides:
    - Content filtering
    - Risk assessment
    - Safety level determination
    - Harmful content detection
    - Inappropriate language detection
    - Personal information detection
    - Sensitive topic detection
    """
    
    def __init__(self):
        """Initialize the safety validator."""
        self.logger = get_logger(__name__)
        
        # Initialize safety models
        self._init_harmful_content_patterns()
        self._init_inappropriate_language_patterns()
        self._init_personal_information_patterns()
        self._init_sensitive_topic_patterns()
        self._init_violence_patterns()
        self._init_hate_speech_patterns()
        self._init_spam_patterns()
        
        # Safety thresholds
        self.safety_thresholds = {
            SafetyLevel.SAFE: 0.0,
            SafetyLevel.WARNING: 0.3,
            SafetyLevel.UNSAFE: 0.6,
            SafetyLevel.BLOCKED: 0.8
        }
        
        self.logger.info("Safety Validator initialized")
    
    def _init_harmful_content_patterns(self) -> None:
        """Initialize harmful content detection patterns."""
        self.harmful_content_patterns = {
            "self_harm": [
                r"\b(suicide|kill\s+myself|end\s+it\s+all|not\s+worth\s+living)\b",
                r"\b(cut\s+myself|hurt\s+myself|self\s+harm|self\s+injury)\b",
                r"\b(overdose|poison|hang\s+myself|jump\s+off)\b"
            ],
            "violence_against_others": [
                r"\b(kill\s+you|hurt\s+you|harm\s+you|attack\s+you)\b",
                r"\b(violence|assault|battery|murder|homicide)\b",
                r"\b(weapon|gun|knife|bomb|explosive)\b"
            ],
            "threats": [
                r"\b(threat|threaten|warning|ultimatum)\b",
                r"\b(consequences|pay\s+for\s+this|regret\s+this)\b",
                r"\b(you\s+will\s+pay|you\s+will\s+regret)\b"
            ]
        }
    
    def _init_inappropriate_language_patterns(self) -> None:
        """Initialize inappropriate language detection patterns."""
        self.inappropriate_language_patterns = {
            "profanity": [
                r"\b(fuck|shit|damn|hell|bitch|ass|bastard|piss|pissed)\b",
                r"\b(crap|bullshit|fucking|shitty|damned|hellish)\b"
            ],
            "offensive_terms": [
                r"\b(retard|idiot|moron|stupid|dumb|fool)\b",
                r"\b(loser|failure|worthless|pathetic|disgusting)\b"
            ],
            "sexual_content": [
                r"\b(sex|sexual|porn|pornography|nude|naked)\b",
                r"\b(breast|penis|vagina|orgasm|masturbation)\b"
            ]
        }
    
    def _init_personal_information_patterns(self) -> None:
        """Initialize personal information detection patterns."""
        self.personal_information_patterns = {
            "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
            "phone": r"\b(?:\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}\b",
            "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
            "credit_card": r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b",
            "address": r"\b\d+\s+[A-Za-z0-9\s,.-]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Drive|Dr|Lane|Ln|Way|Place|Pl|Court|Ct)\b"
        }
    
    def _init_sensitive_topic_patterns(self) -> None:
        """Initialize sensitive topic detection patterns."""
        self.sensitive_topic_patterns = {
            "politics": [
                r"\b(politics|political|government|election|vote|voting|campaign)\b",
                r"\b(democrat|republican|liberal|conservative|left|right)\b",
                r"\b(president|senator|congress|mayor|governor)\b"
            ],
            "religion": [
                r"\b(religion|religious|god|jesus|christ|allah|buddha|hindu|jewish|muslim|christian)\b",
                r"\b(church|mosque|temple|synagogue|prayer|worship|faith)\b"
            ],
            "health": [
                r"\b(health|medical|doctor|hospital|disease|illness|sick|medicine)\b",
                r"\b(mental\s+health|depression|anxiety|therapy|counseling)\b"
            ],
            "legal": [
                r"\b(legal|law|lawyer|attorney|court|lawsuit|litigation)\b",
                r"\b(arrest|jail|prison|crime|criminal|felony|misdemeanor)\b"
            ]
        }
    
    def _init_violence_patterns(self) -> None:
        """Initialize violence detection patterns."""
        self.violence_patterns = {
            "physical_violence": [
                r"\b(hit|punch|kick|slap|beat|strike|attack|assault)\b",
                r"\b(fight|battle|combat|war|conflict|struggle)\b"
            ],
            "weapon_violence": [
                r"\b(gun|pistol|rifle|shotgun|knife|sword|blade|weapon)\b",
                r"\b(bomb|explosive|grenade|missile|ammunition|bullet)\b"
            ],
            "threat_violence": [
                r"\b(threat|threaten|warning|ultimatum|intimidation)\b",
                r"\b(consequences|pay\s+for\s+this|regret\s+this)\b"
            ]
        }
    
    def _init_hate_speech_patterns(self) -> None:
        """Initialize hate speech detection patterns."""
        self.hate_speech_patterns = {
            "racial": [
                r"\b(nigger|negro|chink|gook|wetback|spic|kike|jap)\b",
                r"\b(white\s+supremacy|black\s+lives\s+matter|all\s+lives\s+matter)\b"
            ],
            "gender": [
                r"\b(whore|slut|bitch|cunt|dyke|fag|faggot|tranny)\b",
                r"\b(men\s+are\s+trash|women\s+belong\s+in\s+kitchen)\b"
            ],
            "religious": [
                r"\b(jew|muslim|christian|hindu|buddhist|atheist)\b",
                r"\b(religious\s+extremist|terrorist|jihad|holy\s+war)\b"
            ],
            "disability": [
                r"\b(retard|retarded|handicapped|cripple|spaz|retard)\b",
                r"\b(mentally\s+ill|psycho|crazy|insane|nuts)\b"
            ]
        }
    
    def _init_spam_patterns(self) -> None:
        """Initialize spam detection patterns."""
        self.spam_patterns = {
            "commercial": [
                r"\b(buy\s+now|click\s+here|limited\s+time|act\s+now|don't\s+miss)\b",
                r"\b(free\s+offer|special\s+deal|discount|sale|promotion)\b"
            ],
            "phishing": [
                r"\b(verify\s+account|update\s+information|confirm\s+identity)\b",
                r"\b(urgent\s+action|immediate\s+attention|security\s+alert)\b"
            ],
            "scam": [
                r"\b(win\s+prize|congratulations|you\s+won|claim\s+now)\b",
                r"\b(inheritance|lottery|sweepstakes|free\s+money)\b"
            ]
        }
    
    def detect_harmful_content(self, text: str) -> List[RiskType]:
        """
        Detect harmful content in text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            List of detected risk types
        """
        if not text:
            return []
        
        risks = []
        text_lower = text.lower()
        
        # Check for harmful content patterns
        for category, patterns in self.harmful_content_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower, re.IGNORECASE):
                    if category == "self_harm":
                        risks.append(RiskType.HARMFUL_CONTENT)
                    elif category == "violence_against_others":
                        risks.append(RiskType.VIOLENCE)
                    elif category == "threats":
                        risks.append(RiskType.HARMFUL_CONTENT)
                    break
        
        return risks
    
    def detect_inappropriate_language(self, text: str) -> List[RiskType]:
        """
        Detect inappropriate language in text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            List of detected risk types
        """
        if not text:
            return []
        
        risks = []
        text_lower = text.lower()
        
        # Check for inappropriate language patterns
        for category, patterns in self.inappropriate_language_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower, re.IGNORECASE):
                    risks.append(RiskType.INAPPROPRIATE_LANGUAGE)
                    break
        
        return risks
    
    def detect_personal_information(self, text: str) -> List[RiskType]:
        """
        Detect personal information in text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            List of detected risk types
        """
        if not text:
            return []
        
        risks = []
        
        # Check for personal information patterns
        for category, pattern in self.personal_information_patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                risks.append(RiskType.PERSONAL_INFORMATION)
        
        return risks
    
    def detect_sensitive_topics(self, text: str) -> List[RiskType]:
        """
        Detect sensitive topics in text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            List of detected risk types
        """
        if not text:
            return []
        
        risks = []
        text_lower = text.lower()
        
        # Check for sensitive topic patterns
        for category, patterns in self.sensitive_topic_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower, re.IGNORECASE):
                    risks.append(RiskType.SENSITIVE_TOPICS)
                    break
        
        return risks
    
    def detect_violence(self, text: str) -> List[RiskType]:
        """
        Detect violence in text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            List of detected risk types
        """
        if not text:
            return []
        
        risks = []
        text_lower = text.lower()
        
        # Check for violence patterns
        for category, patterns in self.violence_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower, re.IGNORECASE):
                    risks.append(RiskType.VIOLENCE)
                    break
        
        return risks
    
    def detect_hate_speech(self, text: str) -> List[RiskType]:
        """
        Detect hate speech in text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            List of detected risk types
        """
        if not text:
            return []
        
        risks = []
        text_lower = text.lower()
        
        # Check for hate speech patterns
        for category, patterns in self.hate_speech_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower, re.IGNORECASE):
                    risks.append(RiskType.HATE_SPEECH)
                    break
        
        return risks
    
    def detect_spam(self, text: str) -> List[RiskType]:
        """
        Detect spam in text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            List of detected risk types
        """
        if not text:
            return []
        
        risks = []
        text_lower = text.lower()
        
        # Check for spam patterns
        for category, patterns in self.spam_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower, re.IGNORECASE):
                    risks.append(RiskType.SPAM)
                    break
        
        return risks
    
    def calculate_risk_score(self, risks: List[RiskType]) -> float:
        """
        Calculate overall risk score from detected risks.
        
        Args:
            risks: List of detected risk types
            
        Returns:
            Risk score between 0.0 and 1.0
        """
        if not risks:
            return 0.0
        
        # Risk weights
        risk_weights = {
            RiskType.HARMFUL_CONTENT: 1.0,
            RiskType.INAPPROPRIATE_LANGUAGE: 0.3,
            RiskType.PERSONAL_INFORMATION: 0.5,
            RiskType.SENSITIVE_TOPICS: 0.2,
            RiskType.VIOLENCE: 0.8,
            RiskType.HATE_SPEECH: 0.9,
            RiskType.SPAM: 0.1,
            RiskType.MALWARE: 1.0
        }
        
        # Calculate weighted risk score
        total_weight = sum(risk_weights.get(risk, 0.5) for risk in risks)
        max_possible_weight = sum(risk_weights.values())
        
        risk_score = total_weight / max_possible_weight
        return min(1.0, max(0.0, risk_score))
    
    def determine_safety_level(self, risk_score: float) -> SafetyLevel:
        """
        Determine safety level based on risk score.
        
        Args:
            risk_score: Risk score between 0.0 and 1.0
            
        Returns:
            Safety level
        """
        if risk_score >= self.safety_thresholds[SafetyLevel.BLOCKED]:
            return SafetyLevel.BLOCKED
        elif risk_score >= self.safety_thresholds[SafetyLevel.UNSAFE]:
            return SafetyLevel.UNSAFE
        elif risk_score >= self.safety_thresholds[SafetyLevel.WARNING]:
            return SafetyLevel.WARNING
        else:
            return SafetyLevel.SAFE
    
    def validate(self, text: str, context: Optional[Dict[str, Any]] = None) -> SafetyResult:
        """
        Perform comprehensive safety validation.
        
        Args:
            text: Input text to validate
            context: Optional context information
            
        Returns:
            Complete safety validation result
        """
        if not text:
            return SafetyResult(
                is_safe=True,
                safety_level=SafetyLevel.SAFE,
                risk_score=0.0,
                risks=[],
                details={},
                metadata={"error": "Empty text"}
            )
        
        # Detect all types of risks
        all_risks = []
        all_risks.extend(self.detect_harmful_content(text))
        all_risks.extend(self.detect_inappropriate_language(text))
        all_risks.extend(self.detect_personal_information(text))
        all_risks.extend(self.detect_sensitive_topics(text))
        all_risks.extend(self.detect_violence(text))
        all_risks.extend(self.detect_hate_speech(text))
        all_risks.extend(self.detect_spam(text))
        
        # Remove duplicates
        unique_risks = list(set(all_risks))
        
        # Calculate risk score
        risk_score = self.calculate_risk_score(unique_risks)
        
        # Determine safety level
        safety_level = self.determine_safety_level(risk_score)
        
        # Determine if content is safe
        is_safe = safety_level in [SafetyLevel.SAFE, SafetyLevel.WARNING]
        
        # Prepare details
        details = {
            "risk_types": [risk.value for risk in unique_risks],
            "risk_count": len(unique_risks),
            "risk_score": risk_score,
            "safety_level": safety_level.value,
            "is_safe": is_safe
        }
        
        return SafetyResult(
            is_safe=is_safe,
            safety_level=safety_level,
            risk_score=risk_score,
            risks=unique_risks,
            details=details,
            metadata={
                "validator_version": "2.0.0",
                "text_length": len(text),
                "context": context or {}
            }
        )
    
    def reset(self) -> None:
        """Reset the validator state."""
        self.logger.info("Safety Validator reset")
