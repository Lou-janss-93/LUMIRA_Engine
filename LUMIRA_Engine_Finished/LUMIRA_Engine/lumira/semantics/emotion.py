"""
Emotion Analyzer

Specialized emotion analysis for understanding emotional content,
intensity, and emotional patterns in text.
"""

import re
import math
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

from ..utils.logging import get_logger


class EmotionType(Enum):
    """Types of emotions."""
    JOY = "joy"
    SADNESS = "sadness"
    ANGER = "anger"
    FEAR = "fear"
    SURPRISE = "surprise"
    DISGUST = "disgust"
    TRUST = "trust"
    ANTICIPATION = "anticipation"


class EmotionIntensity(Enum):
    """Emotion intensity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    EXTREME = "extreme"


@dataclass
class EmotionResult:
    """Result of emotion analysis."""
    emotion_type: EmotionType
    intensity: EmotionIntensity
    confidence: float
    score: float
    details: Dict[str, Any]
    metadata: Dict[str, Any]


class EmotionAnalyzer:
    """
    Specialized emotion analyzer for understanding emotional content.
    
    Provides:
    - Basic emotion detection
    - Emotion intensity analysis
    - Emotional pattern recognition
    - Emotion transition analysis
    - Emotional context understanding
    """
    
    def __init__(self):
        """Initialize the emotion analyzer."""
        self.logger = get_logger(__name__)
        
        # Initialize emotion models
        self._init_basic_emotions()
        self._init_emotion_intensities()
        self._init_emotion_patterns()
        
        self.logger.info("Emotion Analyzer initialized")
    
    def _init_basic_emotions(self) -> None:
        """Initialize basic emotion models."""
        self.basic_emotions = {
            EmotionType.JOY: {
                "keywords": ["happy", "joy", "excited", "thrilled", "delighted", "cheerful", "optimistic", "pleased", "satisfied", "grateful", "blissful", "ecstatic", "elated", "jubilant", "merry", "glad", "content", "pleased", "satisfied"],
                "weight": 1.0
            },
            EmotionType.SADNESS: {
                "keywords": ["sad", "sorrow", "grief", "melancholy", "depressed", "miserable", "heartbroken", "devastated", "despair", "gloomy", "downcast", "dejected", "disheartened", "crestfallen", "woeful", "mournful", "tearful", "weepy"],
                "weight": 1.0
            },
            EmotionType.ANGER: {
                "keywords": ["angry", "mad", "furious", "rage", "irritated", "annoyed", "frustrated", "enraged", "livid", "incensed", "outraged", "indignant", "resentful", "bitter", "hostile", "aggressive", "violent", "wrathful"],
                "weight": 1.0
            },
            EmotionType.FEAR: {
                "keywords": ["afraid", "scared", "terrified", "frightened", "anxious", "worried", "nervous", "panic", "dread", "horror", "alarm", "apprehension", "trepidation", "unease", "distress", "agitation", "restlessness", "tension"],
                "weight": 1.0
            },
            EmotionType.SURPRISE: {
                "keywords": ["surprised", "shocked", "amazed", "astonished", "startled", "stunned", "bewildered", "confused", "perplexed", "puzzled", "baffled", "mystified", "flabbergasted", "dumbfounded", "speechless", "taken aback", "caught off guard"],
                "weight": 1.0
            },
            EmotionType.DISGUST: {
                "keywords": ["disgusted", "revolted", "repulsed", "sickened", "nauseated", "appalled", "horrified", "offended", "outraged", "scandalized", "shocked", "disturbed", "uncomfortable", "uneasy", "squeamish", "grossed out", "creeped out"],
                "weight": 1.0
            },
            EmotionType.TRUST: {
                "keywords": ["trust", "confident", "secure", "safe", "reliable", "dependable", "faithful", "loyal", "devoted", "committed", "dedicated", "steadfast", "firm", "stable", "solid", "sure", "certain", "assured"],
                "weight": 1.0
            },
            EmotionType.ANTICIPATION: {
                "keywords": ["excited", "eager", "enthusiastic", "hopeful", "optimistic", "expectant", "anticipating", "looking forward", "thrilled", "elated", "jubilant", "ecstatic", "overjoyed", "delighted", "pleased", "satisfied", "content"],
                "weight": 1.0
            }
        }
    
    def _init_emotion_intensities(self) -> None:
        """Initialize emotion intensity models."""
        self.emotion_intensities = {
            EmotionIntensity.LOW: {
                "keywords": ["slightly", "barely", "hardly", "scarcely", "minimally", "a little", "somewhat", "kind of", "sort of", "rather", "quite", "pretty", "fairly"],
                "weight": 0.5
            },
            EmotionIntensity.MEDIUM: {
                "keywords": ["moderately", "reasonably", "adequately", "sufficiently", "appropriately", "suitably", "acceptably", "tolerably", "passably", "decently", "respectably", "competently"],
                "weight": 1.0
            },
            EmotionIntensity.HIGH: {
                "keywords": ["very", "extremely", "incredibly", "absolutely", "completely", "totally", "utterly", "entirely", "thoroughly", "profoundly", "deeply", "intensely", "powerfully", "strongly", "greatly", "immensely"],
                "weight": 2.0
            },
            EmotionIntensity.EXTREME: {
                "keywords": ["overwhelmingly", "unbearably", "uncontrollably", "unmanageably", "unendurably", "intolerably", "insufferably", "unbearably", "uncontrollably", "unmanageably", "unendurably", "intolerably", "insufferably"],
                "weight": 3.0
            }
        }
    
    def _init_emotion_patterns(self) -> None:
        """Initialize emotion pattern models."""
        self.emotion_patterns = {
            "positive_emotions": [EmotionType.JOY, EmotionType.TRUST, EmotionType.ANTICIPATION],
            "negative_emotions": [EmotionType.SADNESS, EmotionType.ANGER, EmotionType.FEAR, EmotionType.DISGUST],
            "neutral_emotions": [EmotionType.SURPRISE],
            "high_arousal": [EmotionType.JOY, EmotionType.ANGER, EmotionType.FEAR, EmotionType.SURPRISE],
            "low_arousal": [EmotionType.SADNESS, EmotionType.TRUST, EmotionType.DISGUST],
            "positive_valence": [EmotionType.JOY, EmotionType.TRUST, EmotionType.ANTICIPATION],
            "negative_valence": [EmotionType.SADNESS, EmotionType.ANGER, EmotionType.FEAR, EmotionType.DISGUST]
        }
    
    def detect_emotions(self, text: str) -> Dict[EmotionType, float]:
        """
        Detect emotions in text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary of emotions and their scores
        """
        if not text:
            return {}
        
        text_lower = text.lower()
        emotion_scores = {}
        
        for emotion, model in self.basic_emotions.items():
            word_count = sum(1 for word in model["keywords"] if word in text_lower)
            score = word_count * model["weight"]
            emotion_scores[emotion] = score
        
        # Normalize scores
        total_score = sum(emotion_scores.values())
        if total_score > 0:
            emotion_scores = {k: v / total_score for k, v in emotion_scores.items()}
        
        return emotion_scores
    
    def detect_emotion_intensity(self, text: str) -> EmotionIntensity:
        """
        Detect emotion intensity in text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Detected emotion intensity
        """
        if not text:
            return EmotionIntensity.LOW
        
        text_lower = text.lower()
        intensity_scores = {}
        
        for intensity, model in self.emotion_intensities.items():
            word_count = sum(1 for word in model["keywords"] if word in text_lower)
            score = word_count * model["weight"]
            intensity_scores[intensity] = score
        
        # Find dominant intensity
        if intensity_scores:
            dominant_intensity = max(intensity_scores.items(), key=lambda x: x[1])[0]
            return dominant_intensity
        else:
            return EmotionIntensity.LOW
    
    def analyze_emotion_patterns(self, text: str) -> Dict[str, float]:
        """
        Analyze emotion patterns in text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary of emotion pattern scores
        """
        if not text:
            return {}
        
        emotion_scores = self.detect_emotions(text)
        pattern_scores = {}
        
        for pattern_name, emotions in self.emotion_patterns.items():
            pattern_score = sum(emotion_scores.get(emotion, 0.0) for emotion in emotions)
            pattern_scores[pattern_name] = pattern_score
        
        return pattern_scores
    
    def calculate_emotional_valence(self, text: str) -> float:
        """
        Calculate emotional valence (positive/negative) of text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Valence score between -1.0 (negative) and 1.0 (positive)
        """
        if not text:
            return 0.0
        
        emotion_scores = self.detect_emotions(text)
        
        positive_score = sum(emotion_scores.get(emotion, 0.0) for emotion in self.emotion_patterns["positive_valence"])
        negative_score = sum(emotion_scores.get(emotion, 0.0) for emotion in self.emotion_patterns["negative_valence"])
        
        total_score = positive_score + negative_score
        if total_score == 0:
            return 0.0
        
        valence = (positive_score - negative_score) / total_score
        return max(-1.0, min(1.0, valence))
    
    def calculate_emotional_arousal(self, text: str) -> float:
        """
        Calculate emotional arousal (high/low) of text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Arousal score between 0.0 (low) and 1.0 (high)
        """
        if not text:
            return 0.0
        
        emotion_scores = self.detect_emotions(text)
        
        high_arousal_score = sum(emotion_scores.get(emotion, 0.0) for emotion in self.emotion_patterns["high_arousal"])
        low_arousal_score = sum(emotion_scores.get(emotion, 0.0) for emotion in self.emotion_patterns["low_arousal"])
        
        total_score = high_arousal_score + low_arousal_score
        if total_score == 0:
            return 0.0
        
        arousal = high_arousal_score / total_score
        return max(0.0, min(1.0, arousal))
    
    def analyze(self, text: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Perform comprehensive emotion analysis.
        
        Args:
            text: Input text to analyze
            context: Optional context information
            
        Returns:
            Complete emotion analysis results
        """
        if not text:
            return {
                "text": text,
                "context": context or {},
                "analysis": {},
                "overall_score": 0.0,
                "confidence": 0.0,
                "error": "Empty text"
            }
        
        # Detect emotions
        emotion_scores = self.detect_emotions(text)
        
        # Detect emotion intensity
        intensity = self.detect_emotion_intensity(text)
        
        # Analyze emotion patterns
        pattern_scores = self.analyze_emotion_patterns(text)
        
        # Calculate valence and arousal
        valence = self.calculate_emotional_valence(text)
        arousal = self.calculate_emotional_arousal(text)
        
        # Find dominant emotion
        dominant_emotion = max(emotion_scores.items(), key=lambda x: x[1])[0] if emotion_scores else EmotionType.JOY
        
        # Calculate overall confidence
        total_indicators = sum(emotion_scores.values())
        confidence = min(1.0, total_indicators / 10.0)
        
        # Calculate overall score
        overall_score = (valence + arousal) / 2.0
        
        return {
            "text": text,
            "context": context or {},
            "analysis": {
                "emotions": {emotion.value: score for emotion, score in emotion_scores.items()},
                "intensity": intensity.value,
                "patterns": pattern_scores,
                "valence": valence,
                "arousal": arousal,
                "dominant_emotion": dominant_emotion.value
            },
            "overall_score": overall_score,
            "confidence": confidence,
            "metadata": {
                "analyzer_version": "2.0.0",
                "emotions_analyzed": len(emotion_scores),
                "text_length": len(text),
                "total_indicators": total_indicators
            }
        }
    
    def reset(self) -> None:
        """Reset the analyzer state."""
        self.logger.info("Emotion Analyzer reset")
