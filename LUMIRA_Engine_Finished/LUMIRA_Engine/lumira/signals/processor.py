"""
Signal Processor

Signal processing capabilities for analyzing patterns, trends,
and signals in text content and emotional data.
"""

import re
import math
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

from ..utils.logging import get_logger


class SignalType(Enum):
    """Types of signals."""
    EMOTIONAL = "emotional"
    LINGUISTIC = "linguistic"
    TEMPORAL = "temporal"
    CONTEXTUAL = "contextual"
    BEHAVIORAL = "behavioral"


class SignalStrength(Enum):
    """Signal strength levels."""
    WEAK = "weak"
    MODERATE = "moderate"
    STRONG = "strong"
    VERY_STRONG = "very_strong"


@dataclass
class SignalResult:
    """Result of signal processing."""
    signal_type: SignalType
    strength: SignalStrength
    confidence: float
    score: float
    details: Dict[str, Any]
    metadata: Dict[str, Any]


class SignalProcessor:
    """
    Signal processor for analyzing patterns and trends in text.
    
    Provides:
    - Emotional signal processing
    - Linguistic signal analysis
    - Temporal signal detection
    - Contextual signal processing
    - Behavioral signal analysis
    """
    
    def __init__(self):
        """Initialize the signal processor."""
        self.logger = get_logger(__name__)
        
        # Initialize signal models
        self._init_emotional_signals()
        self._init_linguistic_signals()
        self._init_temporal_signals()
        self._init_contextual_signals()
        self._init_behavioral_signals()
        
        self.logger.info("Signal Processor initialized")
    
    def _init_emotional_signals(self) -> None:
        """Initialize emotional signal models."""
        self.emotional_signals = {
            "intensity_indicators": {
                "high": ["very", "extremely", "incredibly", "absolutely", "completely", "totally", "utterly", "entirely", "thoroughly", "profoundly", "deeply", "intensely", "powerfully", "strongly", "greatly", "immensely"],
                "medium": ["quite", "rather", "pretty", "fairly", "somewhat", "moderately", "reasonably", "adequately", "sufficiently", "appropriately", "suitably", "acceptably", "tolerably", "passably", "decently", "respectably", "competently"],
                "low": ["slightly", "barely", "hardly", "scarcely", "minimally", "a little", "kind of", "sort of", "rather", "quite", "pretty", "fairly"]
            },
            "emotion_indicators": {
                "positive": ["happy", "joy", "excited", "thrilled", "delighted", "cheerful", "optimistic", "pleased", "satisfied", "grateful", "blissful", "ecstatic", "elated", "jubilant", "merry", "glad", "content", "pleased", "satisfied"],
                "negative": ["sad", "sorrow", "grief", "melancholy", "depressed", "miserable", "heartbroken", "devastated", "despair", "gloomy", "downcast", "dejected", "disheartened", "crestfallen", "woeful", "mournful", "tearful", "weepy"],
                "anger": ["angry", "mad", "furious", "rage", "irritated", "annoyed", "frustrated", "enraged", "livid", "incensed", "outraged", "indignant", "resentful", "bitter", "hostile", "aggressive", "violent", "wrathful"],
                "fear": ["afraid", "scared", "terrified", "frightened", "anxious", "worried", "nervous", "panic", "dread", "horror", "alarm", "apprehension", "trepidation", "unease", "distress", "agitation", "restlessness", "tension"],
                "surprise": ["surprised", "shocked", "amazed", "astonished", "startled", "stunned", "bewildered", "confused", "perplexed", "puzzled", "baffled", "mystified", "flabbergasted", "dumbfounded", "speechless", "taken aback", "caught off guard"],
                "disgust": ["disgusted", "revolted", "repulsed", "sickened", "nauseated", "appalled", "horrified", "offended", "outraged", "scandalized", "shocked", "disturbed", "uncomfortable", "uneasy", "squeamish", "grossed out", "creeped out"],
                "trust": ["trust", "confident", "secure", "safe", "reliable", "dependable", "faithful", "loyal", "devoted", "committed", "dedicated", "steadfast", "firm", "stable", "solid", "sure", "certain", "assured"],
                "anticipation": ["excited", "eager", "enthusiastic", "hopeful", "optimistic", "expectant", "anticipating", "looking forward", "thrilled", "elated", "jubilant", "ecstatic", "overjoyed", "delighted", "pleased", "satisfied", "content"]
            }
        }
    
    def _init_linguistic_signals(self) -> None:
        """Initialize linguistic signal models."""
        self.linguistic_signals = {
            "complexity_indicators": {
                "high": ["complex", "complicated", "sophisticated", "advanced", "intricate", "elaborate", "detailed", "comprehensive", "thorough", "extensive", "profound", "deep", "intellectual", "academic", "scholarly", "technical", "specialized"],
                "medium": ["moderate", "reasonable", "adequate", "sufficient", "appropriate", "suitable", "acceptable", "tolerable", "passable", "decent", "respectable", "competent", "standard", "normal", "regular", "typical", "usual"],
                "low": ["simple", "basic", "elementary", "fundamental", "straightforward", "clear", "obvious", "evident", "plain", "easy", "uncomplicated", "straightforward", "direct", "concise", "brief", "short", "minimal"]
            },
            "formality_indicators": {
                "formal": ["formal", "official", "professional", "business", "academic", "scholarly", "intellectual", "serious", "solemn", "grave", "important", "significant", "crucial", "critical", "essential", "vital", "necessary"],
                "informal": ["casual", "informal", "relaxed", "friendly", "chatty", "conversational", "colloquial", "slang", "jargon", "dialect", "vernacular", "everyday", "common", "ordinary", "regular", "normal", "typical"]
            },
            "certainty_indicators": {
                "high": ["definitely", "certainly", "surely", "absolutely", "positively", "undoubtedly", "clearly", "obviously", "evidently", "indisputably", "unquestionably", "incontestably", "inarguably", "irrefutably", "conclusively", "decisively", "finally"],
                "medium": ["probably", "likely", "possibly", "perhaps", "maybe", "might", "could", "may", "potentially", "conceivably", "plausibly", "feasibly", "reasonably", "credibly", "believably", "acceptably", "tolerably"],
                "low": ["unlikely", "improbably", "doubtfully", "questionably", "uncertainly", "unclearly", "ambiguously", "vaguely", "indefinitely", "tentatively", "hesitantly", "cautiously", "carefully", "prudently", "warily", "suspiciously", "doubtfully"]
            }
        }
    
    def _init_temporal_signals(self) -> None:
        """Initialize temporal signal models."""
        self.temporal_signals = {
            "time_indicators": {
                "past": ["was", "were", "had", "did", "went", "came", "saw", "heard", "felt", "thought", "remembered", "recalled", "yesterday", "before", "ago", "previously", "earlier", "once", "used to", "formerly", "historically", "traditionally"],
                "present": ["am", "is", "are", "have", "has", "do", "does", "go", "goes", "come", "comes", "see", "sees", "hear", "hears", "feel", "feels", "think", "thinks", "now", "today", "currently", "at the moment", "right now", "presently", "immediately", "instantly"],
                "future": ["will", "shall", "going to", "gonna", "tomorrow", "next", "soon", "later", "eventually", "plan", "intend", "expect", "hope", "anticipate", "predict", "forecast", "upcoming", "forthcoming", "prospective", "potential", "possible"]
            },
            "urgency_indicators": {
                "high": ["urgent", "immediate", "critical", "emergency", "crisis", "pressing", "pressing", "desperate", "dire", "acute", "severe", "serious", "grave", "important", "significant", "crucial", "essential", "vital", "necessary"],
                "medium": ["important", "significant", "notable", "remarkable", "considerable", "substantial", "meaningful", "relevant", "pertinent", "applicable", "appropriate", "suitable", "fitting", "proper", "correct", "right", "good"],
                "low": ["minor", "slight", "small", "little", "tiny", "minimal", "negligible", "insignificant", "unimportant", "trivial", "petty", "inconsequential", "irrelevant", "inapplicable", "unsuitable", "inappropriate", "improper", "wrong", "bad"]
            }
        }
    
    def _init_contextual_signals(self) -> None:
        """Initialize contextual signal models."""
        self.contextual_signals = {
            "domain_indicators": {
                "work": ["work", "job", "office", "meeting", "project", "deadline", "colleague", "boss", "manager", "team", "business", "professional", "career", "employment", "task", "assignment", "report", "presentation", "conference", "workshop"],
                "personal": ["family", "friend", "home", "personal", "private", "relationship", "partner", "spouse", "child", "parent", "sibling", "relative", "love", "marriage", "dating", "romance", "intimate", "close", "dear", "beloved"],
                "health": ["health", "sick", "ill", "doctor", "hospital", "medicine", "pain", "tired", "exhausted", "medical", "treatment", "therapy", "recovery", "wellness", "fitness", "exercise", "diet", "nutrition", "mental", "physical"],
                "social": ["party", "social", "event", "gathering", "celebration", "festival", "conference", "meeting", "group", "community", "society", "public", "crowd", "audience", "spectators", "participants", "members", "colleagues", "friends", "family"]
            },
            "modality_indicators": {
                "certainty": ["definitely", "certainly", "surely", "absolutely", "positively", "undoubtedly", "clearly", "obviously", "evidently", "indisputably", "unquestionably", "incontestably", "inarguably", "irrefutably", "conclusively", "decisively", "finally"],
                "possibility": ["maybe", "perhaps", "possibly", "might", "could", "may", "potentially", "conceivably", "plausibly", "feasibly", "reasonably", "credibly", "believably", "acceptably", "tolerably", "passably", "decently", "respectably"],
                "necessity": ["must", "have to", "need to", "required", "obligated", "compelled", "forced", "mandatory", "essential", "critical", "vital", "necessary", "indispensable", "irreplaceable", "irreversible", "irrevocable", "irreparable", "irremediable"]
            }
        }
    
    def _init_behavioral_signals(self) -> None:
        """Initialize behavioral signal models."""
        self.behavioral_signals = {
            "assertiveness_indicators": {
                "high": ["assertive", "confident", "decisive", "determined", "resolute", "firm", "strong", "powerful", "authoritative", "commanding", "dominant", "influential", "persuasive", "convincing", "compelling", "forceful", "aggressive", "pushy"],
                "medium": ["balanced", "stable", "steady", "moderate", "reasonable", "practical", "realistic", "sensible", "level-headed", "composed", "calm", "collected", "cool", "relaxed", "easy-going", "laid-back", "chill", "mellow"],
                "low": ["submissive", "passive", "meek", "timid", "shy", "reserved", "quiet", "withdrawn", "introverted", "private", "personal", "intimate", "close", "dear", "beloved", "loved", "cherished", "treasured", "valued", "appreciated"]
            },
            "cooperation_indicators": {
                "high": ["cooperative", "collaborative", "helpful", "supportive", "assisting", "aiding", "facilitating", "enabling", "empowering", "encouraging", "motivating", "inspiring", "uplifting", "positive", "constructive", "productive", "effective", "efficient"],
                "medium": ["neutral", "indifferent", "apathetic", "unconcerned", "disinterested", "uninvolved", "detached", "distant", "remote", "separate", "isolated", "alone", "lonely", "solitary", "independent", "self-reliant", "autonomous", "free"],
                "low": ["uncooperative", "unhelpful", "unsupportive", "hindering", "obstructing", "blocking", "preventing", "stopping", "halting", "ceasing", "ending", "finishing", "completing", "concluding", "terminating", "stopping", "halting", "ceasing"]
            }
        }
    
    def process_emotional_signals(self, text: str) -> SignalResult:
        """
        Process emotional signals in text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Emotional signal processing result
        """
        if not text:
            return SignalResult(
                signal_type=SignalType.EMOTIONAL,
                strength=SignalStrength.WEAK,
                confidence=0.0,
                score=0.0,
                details={},
                metadata={"error": "Empty text"}
            )
        
        text_lower = text.lower()
        scores = {}
        
        # Analyze emotion indicators
        for emotion, indicators in self.emotional_signals["emotion_indicators"].items():
            emotion_count = sum(1 for indicator in indicators if indicator in text_lower)
            scores[emotion] = emotion_count
        
        # Analyze intensity indicators
        intensity_scores = {}
        for intensity, indicators in self.emotional_signals["intensity_indicators"].items():
            intensity_count = sum(1 for indicator in indicators if indicator in text_lower)
            intensity_scores[intensity] = intensity_count
        
        # Calculate overall emotional signal strength
        total_emotion_indicators = sum(scores.values())
        total_intensity_indicators = sum(intensity_scores.values())
        
        # Determine signal strength
        if total_emotion_indicators >= 10 or total_intensity_indicators >= 5:
            strength = SignalStrength.VERY_STRONG
        elif total_emotion_indicators >= 5 or total_intensity_indicators >= 3:
            strength = SignalStrength.STRONG
        elif total_emotion_indicators >= 2 or total_intensity_indicators >= 1:
            strength = SignalStrength.MODERATE
        else:
            strength = SignalStrength.WEAK
        
        # Calculate confidence
        confidence = min(1.0, (total_emotion_indicators + total_intensity_indicators) / 15.0)
        
        # Calculate score
        score = min(1.0, (total_emotion_indicators + total_intensity_indicators) / 20.0)
        
        return SignalResult(
            signal_type=SignalType.EMOTIONAL,
            strength=strength,
            confidence=confidence,
            score=score,
            details={
                "emotion_scores": scores,
                "intensity_scores": intensity_scores,
                "total_indicators": total_emotion_indicators + total_intensity_indicators
            },
            metadata={
                "text_length": len(text),
                "emotions_analyzed": len(scores),
                "intensities_analyzed": len(intensity_scores)
            }
        )
    
    def process_linguistic_signals(self, text: str) -> SignalResult:
        """
        Process linguistic signals in text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Linguistic signal processing result
        """
        if not text:
            return SignalResult(
                signal_type=SignalType.LINGUISTIC,
                strength=SignalStrength.WEAK,
                confidence=0.0,
                score=0.0,
                details={},
                metadata={"error": "Empty text"}
            )
        
        text_lower = text.lower()
        scores = {}
        
        # Analyze complexity indicators
        for complexity, indicators in self.linguistic_signals["complexity_indicators"].items():
            complexity_count = sum(1 for indicator in indicators if indicator in text_lower)
            scores[complexity] = complexity_count
        
        # Analyze formality indicators
        formality_scores = {}
        for formality, indicators in self.linguistic_signals["formality_indicators"].items():
            formality_count = sum(1 for indicator in indicators if indicator in text_lower)
            formality_scores[formality] = formality_count
        
        # Analyze certainty indicators
        certainty_scores = {}
        for certainty, indicators in self.linguistic_signals["certainty_indicators"].items():
            certainty_count = sum(1 for indicator in indicators if indicator in text_lower)
            certainty_scores[certainty] = certainty_count
        
        # Calculate overall linguistic signal strength
        total_indicators = sum(scores.values()) + sum(formality_scores.values()) + sum(certainty_scores.values())
        
        # Determine signal strength
        if total_indicators >= 15:
            strength = SignalStrength.VERY_STRONG
        elif total_indicators >= 8:
            strength = SignalStrength.STRONG
        elif total_indicators >= 3:
            strength = SignalStrength.MODERATE
        else:
            strength = SignalStrength.WEAK
        
        # Calculate confidence
        confidence = min(1.0, total_indicators / 20.0)
        
        # Calculate score
        score = min(1.0, total_indicators / 25.0)
        
        return SignalResult(
            signal_type=SignalType.LINGUISTIC,
            strength=strength,
            confidence=confidence,
            score=score,
            details={
                "complexity_scores": scores,
                "formality_scores": formality_scores,
                "certainty_scores": certainty_scores,
                "total_indicators": total_indicators
            },
            metadata={
                "text_length": len(text),
                "complexities_analyzed": len(scores),
                "formalities_analyzed": len(formality_scores),
                "certainties_analyzed": len(certainty_scores)
            }
        )
    
    def process_temporal_signals(self, text: str) -> SignalResult:
        """
        Process temporal signals in text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Temporal signal processing result
        """
        if not text:
            return SignalResult(
                signal_type=SignalType.TEMPORAL,
                strength=SignalStrength.WEAK,
                confidence=0.0,
                score=0.0,
                details={},
                metadata={"error": "Empty text"}
            )
        
        text_lower = text.lower()
        scores = {}
        
        # Analyze time indicators
        for time, indicators in self.temporal_signals["time_indicators"].items():
            time_count = sum(1 for indicator in indicators if indicator in text_lower)
            scores[time] = time_count
        
        # Analyze urgency indicators
        urgency_scores = {}
        for urgency, indicators in self.temporal_signals["urgency_indicators"].items():
            urgency_count = sum(1 for indicator in indicators if indicator in text_lower)
            urgency_scores[urgency] = urgency_count
        
        # Calculate overall temporal signal strength
        total_indicators = sum(scores.values()) + sum(urgency_scores.values())
        
        # Determine signal strength
        if total_indicators >= 10:
            strength = SignalStrength.VERY_STRONG
        elif total_indicators >= 5:
            strength = SignalStrength.STRONG
        elif total_indicators >= 2:
            strength = SignalStrength.MODERATE
        else:
            strength = SignalStrength.WEAK
        
        # Calculate confidence
        confidence = min(1.0, total_indicators / 15.0)
        
        # Calculate score
        score = min(1.0, total_indicators / 20.0)
        
        return SignalResult(
            signal_type=SignalType.TEMPORAL,
            strength=strength,
            confidence=confidence,
            score=score,
            details={
                "time_scores": scores,
                "urgency_scores": urgency_scores,
                "total_indicators": total_indicators
            },
            metadata={
                "text_length": len(text),
                "times_analyzed": len(scores),
                "urgencies_analyzed": len(urgency_scores)
            }
        )
    
    def process_contextual_signals(self, text: str) -> SignalResult:
        """
        Process contextual signals in text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Contextual signal processing result
        """
        if not text:
            return SignalResult(
                signal_type=SignalType.CONTEXTUAL,
                strength=SignalStrength.WEAK,
                confidence=0.0,
                score=0.0,
                details={},
                metadata={"error": "Empty text"}
            )
        
        text_lower = text.lower()
        scores = {}
        
        # Analyze domain indicators
        for domain, indicators in self.contextual_signals["domain_indicators"].items():
            domain_count = sum(1 for indicator in indicators if indicator in text_lower)
            scores[domain] = domain_count
        
        # Analyze modality indicators
        modality_scores = {}
        for modality, indicators in self.contextual_signals["modality_indicators"].items():
            modality_count = sum(1 for indicator in indicators if indicator in text_lower)
            modality_scores[modality] = modality_count
        
        # Calculate overall contextual signal strength
        total_indicators = sum(scores.values()) + sum(modality_scores.values())
        
        # Determine signal strength
        if total_indicators >= 12:
            strength = SignalStrength.VERY_STRONG
        elif total_indicators >= 6:
            strength = SignalStrength.STRONG
        elif total_indicators >= 2:
            strength = SignalStrength.MODERATE
        else:
            strength = SignalStrength.WEAK
        
        # Calculate confidence
        confidence = min(1.0, total_indicators / 18.0)
        
        # Calculate score
        score = min(1.0, total_indicators / 25.0)
        
        return SignalResult(
            signal_type=SignalType.CONTEXTUAL,
            strength=strength,
            confidence=confidence,
            score=score,
            details={
                "domain_scores": scores,
                "modality_scores": modality_scores,
                "total_indicators": total_indicators
            },
            metadata={
                "text_length": len(text),
                "domains_analyzed": len(scores),
                "modalities_analyzed": len(modality_scores)
            }
        )
    
    def process_behavioral_signals(self, text: str) -> SignalResult:
        """
        Process behavioral signals in text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Behavioral signal processing result
        """
        if not text:
            return SignalResult(
                signal_type=SignalType.BEHAVIORAL,
                strength=SignalStrength.WEAK,
                confidence=0.0,
                score=0.0,
                details={},
                metadata={"error": "Empty text"}
            )
        
        text_lower = text.lower()
        scores = {}
        
        # Analyze assertiveness indicators
        for assertiveness, indicators in self.behavioral_signals["assertiveness_indicators"].items():
            assertiveness_count = sum(1 for indicator in indicators if indicator in text_lower)
            scores[assertiveness] = assertiveness_count
        
        # Analyze cooperation indicators
        cooperation_scores = {}
        for cooperation, indicators in self.behavioral_signals["cooperation_indicators"].items():
            cooperation_count = sum(1 for indicator in indicators if indicator in text_lower)
            cooperation_scores[cooperation] = cooperation_count
        
        # Calculate overall behavioral signal strength
        total_indicators = sum(scores.values()) + sum(cooperation_scores.values())
        
        # Determine signal strength
        if total_indicators >= 8:
            strength = SignalStrength.VERY_STRONG
        elif total_indicators >= 4:
            strength = SignalStrength.STRONG
        elif total_indicators >= 1:
            strength = SignalStrength.MODERATE
        else:
            strength = SignalStrength.WEAK
        
        # Calculate confidence
        confidence = min(1.0, total_indicators / 12.0)
        
        # Calculate score
        score = min(1.0, total_indicators / 16.0)
        
        return SignalResult(
            signal_type=SignalType.BEHAVIORAL,
            strength=strength,
            confidence=confidence,
            score=score,
            details={
                "assertiveness_scores": scores,
                "cooperation_scores": cooperation_scores,
                "total_indicators": total_indicators
            },
            metadata={
                "text_length": len(text),
                "assertivenesses_analyzed": len(scores),
                "cooperations_analyzed": len(cooperation_scores)
            }
        )
    
    def process(self, text: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Perform comprehensive signal processing.
        
        Args:
            text: Input text to analyze
            context: Optional context information
            
        Returns:
            Complete signal processing results
        """
        if not text:
            return {
                "text": text,
                "context": context or {},
                "signals": {},
                "overall_score": 0.0,
                "confidence": 0.0,
                "error": "Empty text"
            }
        
        # Process all signal types
        emotional_result = self.process_emotional_signals(text)
        linguistic_result = self.process_linguistic_signals(text)
        temporal_result = self.process_temporal_signals(text)
        contextual_result = self.process_contextual_signals(text)
        behavioral_result = self.process_behavioral_signals(text)
        
        # Calculate overall scores
        all_scores = [emotional_result.score, linguistic_result.score, 
                     temporal_result.score, contextual_result.score, behavioral_result.score]
        overall_score = sum(all_scores) / len(all_scores)
        
        all_confidences = [emotional_result.confidence, linguistic_result.confidence,
                          temporal_result.confidence, contextual_result.confidence, behavioral_result.confidence]
        overall_confidence = sum(all_confidences) / len(all_confidences)
        
        return {
            "text": text,
            "context": context or {},
            "signals": {
                "emotional": {
                    "strength": emotional_result.strength.value,
                    "confidence": emotional_result.confidence,
                    "score": emotional_result.score,
                    "details": emotional_result.details
                },
                "linguistic": {
                    "strength": linguistic_result.strength.value,
                    "confidence": linguistic_result.confidence,
                    "score": linguistic_result.score,
                    "details": linguistic_result.details
                },
                "temporal": {
                    "strength": temporal_result.strength.value,
                    "confidence": temporal_result.confidence,
                    "score": temporal_result.score,
                    "details": temporal_result.details
                },
                "contextual": {
                    "strength": contextual_result.strength.value,
                    "confidence": contextual_result.confidence,
                    "score": contextual_result.score,
                    "details": contextual_result.details
                },
                "behavioral": {
                    "strength": behavioral_result.strength.value,
                    "confidence": behavioral_result.confidence,
                    "score": behavioral_result.score,
                    "details": behavioral_result.details
                }
            },
            "overall_score": overall_score,
            "confidence": overall_confidence,
            "metadata": {
                "processor_version": "2.0.0",
                "signal_types": [t.value for t in SignalType],
                "text_length": len(text)
            }
        }
    
    def reset(self) -> None:
        """Reset the processor state."""
        self.logger.info("Signal Processor reset")
