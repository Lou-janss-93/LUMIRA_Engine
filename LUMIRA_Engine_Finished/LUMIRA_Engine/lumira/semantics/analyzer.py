"""
Semantic Analyzer

Advanced semantic analysis for understanding context, meaning,
and emotional content in text. Provides comprehensive semantic
processing capabilities.
"""

import re
import math
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass
from enum import Enum

from ..utils.logging import get_logger


class SemanticType(Enum):
    """Types of semantic analysis."""
    EMOTIONAL = "emotional"
    CONTEXTUAL = "contextual"
    INTENTIONAL = "intentional"
    RELATIONAL = "relational"


@dataclass
class SemanticResult:
    """Result of semantic analysis."""
    semantic_type: SemanticType
    confidence: float
    score: float
    details: Dict[str, Any]
    metadata: Dict[str, Any]


class SemanticAnalyzer:
    """
    Advanced semantic analyzer for understanding text meaning and context.
    
    Provides:
    - Emotional semantic analysis
    - Contextual understanding
    - Intent detection
    - Relationship analysis
    - Semantic similarity
    """
    
    def __init__(self):
        """Initialize the semantic analyzer."""
        self.logger = get_logger(__name__)
        
        # Initialize semantic models
        self._init_emotional_models()
        self._init_contextual_models()
        self._init_intentional_models()
        self._init_relational_models()
        
        self.logger.info("Semantic Analyzer initialized")
    
    def _init_emotional_models(self) -> None:
        """Initialize emotional semantic models."""
        self.emotional_models = {
            "valence": {
                "positive": {
                    "words": ["happy", "joy", "excited", "great", "wonderful", "amazing", "fantastic", "love", "excellent", "brilliant", "awesome", "perfect", "delighted", "thrilled", "cheerful", "optimistic", "pleased", "satisfied", "grateful"],
                    "weight": 1.0
                },
                "negative": {
                    "words": ["sad", "angry", "upset", "disappointed", "frustrated", "terrible", "awful", "horrible", "hate", "disgusted", "furious", "depressed", "miserable", "devastated", "heartbroken", "lonely", "hopeless"],
                    "weight": -1.0
                },
                "neutral": {
                    "words": ["okay", "fine", "normal", "average", "regular", "standard", "typical", "usual", "alright", "decent"],
                    "weight": 0.0
                }
            },
            "arousal": {
                "high": {
                    "words": ["excited", "thrilled", "furious", "terrified", "ecstatic", "enraged", "panicked", "elated", "frenzied", "overwhelmed"],
                    "weight": 1.0
                },
                "medium": {
                    "words": ["interested", "concerned", "pleased", "annoyed", "curious", "worried", "satisfied", "frustrated", "hopeful", "anxious"],
                    "weight": 0.5
                },
                "low": {
                    "words": ["calm", "peaceful", "relaxed", "serene", "tranquil", "bored", "indifferent", "apathetic", "content", "placid"],
                    "weight": 0.0
                }
            },
            "dominance": {
                "high": {
                    "words": ["confident", "powerful", "strong", "capable", "competent", "assertive", "dominant", "authoritative", "commanding", "influential"],
                    "weight": 1.0
                },
                "medium": {
                    "words": ["balanced", "stable", "steady", "moderate", "reasonable", "practical", "realistic", "sensible", "level-headed", "composed"],
                    "weight": 0.5
                },
                "low": {
                    "words": ["submissive", "weak", "helpless", "vulnerable", "dependent", "passive", "meek", "timid", "shy", "insecure"],
                    "weight": 0.0
                }
            }
        }
    
    def _init_contextual_models(self) -> None:
        """Initialize contextual semantic models."""
        self.contextual_models = {
            "domain": {
                "work": ["work", "job", "office", "meeting", "project", "deadline", "colleague", "boss", "manager", "team", "business", "professional", "career", "employment"],
                "personal": ["family", "friend", "home", "personal", "private", "relationship", "partner", "spouse", "child", "parent", "sibling", "relative"],
                "health": ["health", "sick", "ill", "doctor", "hospital", "medicine", "pain", "tired", "exhausted", "medical", "treatment", "therapy", "recovery"],
                "social": ["party", "social", "event", "gathering", "celebration", "festival", "conference", "meeting", "group", "community", "society", "public"],
                "academic": ["study", "school", "university", "college", "education", "learning", "research", "academic", "student", "teacher", "professor", "course"],
                "financial": ["money", "financial", "budget", "cost", "price", "expensive", "cheap", "affordable", "investment", "savings", "debt", "income"]
            },
            "temporal": {
                "past": ["was", "were", "had", "did", "went", "came", "saw", "heard", "felt", "thought", "remembered", "recalled", "yesterday", "before", "ago"],
                "present": ["am", "is", "are", "have", "has", "do", "does", "go", "goes", "come", "comes", "see", "sees", "hear", "hears", "feel", "feels", "think", "thinks", "now", "today", "currently"],
                "future": ["will", "shall", "going to", "gonna", "tomorrow", "next", "soon", "later", "eventually", "plan", "intend", "expect", "hope", "anticipate"]
            },
            "modality": {
                "certainty": ["definitely", "certainly", "surely", "absolutely", "positively", "undoubtedly", "clearly", "obviously", "evidently", "indisputably"],
                "possibility": ["maybe", "perhaps", "possibly", "might", "could", "may", "potentially", "conceivably", "plausibly", "feasibly"],
                "necessity": ["must", "have to", "need to", "required", "obligated", "compelled", "forced", "mandatory", "essential", "critical"]
            }
        }
    
    def _init_intentional_models(self) -> None:
        """Initialize intentional semantic models."""
        self.intentional_models = {
            "intent": {
                "question": ["what", "when", "where", "why", "how", "who", "which", "?", "ask", "wonder", "curious", "inquire"],
                "request": ["please", "could you", "would you", "can you", "help", "assist", "support", "favor", "request", "ask for"],
                "command": ["do", "don't", "stop", "start", "go", "come", "give", "take", "put", "get", "make", "create"],
                "statement": ["is", "are", "was", "were", "have", "has", "had", "will", "shall", "can", "could", "should", "would"],
                "exclamation": ["!", "wow", "amazing", "incredible", "fantastic", "terrible", "awful", "horrible", "wonderful", "great"]
            },
            "purpose": {
                "inform": ["tell", "inform", "explain", "describe", "clarify", "elaborate", "detail", "specify", "outline", "present"],
                "persuade": ["convince", "persuade", "argue", "debate", "discuss", "negotiate", "bargain", "influence", "sway", "motivate"],
                "entertain": ["fun", "funny", "joke", "laugh", "amuse", "entertain", "enjoy", "pleasure", "delight", "comedy"],
                "express": ["feel", "emotion", "mood", "attitude", "opinion", "view", "perspective", "stance", "position", "belief"]
            }
        }
    
    def _init_relational_models(self) -> None:
        """Initialize relational semantic models."""
        self.relational_models = {
            "social_roles": {
                "authority": ["boss", "manager", "supervisor", "leader", "director", "chief", "head", "president", "commander", "officer"],
                "peer": ["colleague", "coworker", "friend", "buddy", "mate", "partner", "associate", "teammate", "classmate", "neighbor"],
                "subordinate": ["employee", "staff", "worker", "assistant", "helper", "subordinate", "junior", "intern", "trainee", "apprentice"],
                "family": ["parent", "child", "sibling", "spouse", "partner", "relative", "family", "mother", "father", "brother", "sister"]
            },
            "emotional_distance": {
                "intimate": ["love", "adore", "cherish", "treasure", "beloved", "darling", "sweetheart", "honey", "dear", "close"],
                "personal": ["friend", "buddy", "pal", "mate", "companion", "confidant", "ally", "supporter", "advocate", "champion"],
                "professional": ["colleague", "coworker", "associate", "partner", "teammate", "collaborator", "counterpart", "peer", "equal", "contemporary"],
                "distant": ["stranger", "acquaintance", "outsider", "foreigner", "unknown", "unfamiliar", "distant", "remote", "separate", "isolated"]
            }
        }
    
    def analyze_emotional_semantics(self, text: str) -> SemanticResult:
        """
        Analyze emotional semantics in text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Emotional semantic analysis result
        """
        if not text:
            return SemanticResult(
                semantic_type=SemanticType.EMOTIONAL,
                confidence=0.0,
                score=0.0,
                details={},
                metadata={"error": "Empty text"}
            )
        
        text_lower = text.lower()
        scores = {}
        
        # Analyze valence, arousal, and dominance
        for dimension, categories in self.emotional_models.items():
            dimension_scores = {}
            for category, model in categories.items():
                word_count = sum(1 for word in model["words"] if word in text_lower)
                score = word_count * model["weight"]
                dimension_scores[category] = score
            
            # Normalize scores
            total_score = sum(dimension_scores.values())
            if total_score != 0:
                dimension_scores = {k: v / total_score for k, v in dimension_scores.items()}
            
            scores[dimension] = dimension_scores
        
        # Calculate overall emotional score
        valence_score = scores["valence"].get("positive", 0) - scores["valence"].get("negative", 0)
        arousal_score = scores["arousal"].get("high", 0) + scores["arousal"].get("medium", 0) * 0.5
        dominance_score = scores["dominance"].get("high", 0) + scores["dominance"].get("medium", 0) * 0.5
        
        overall_score = (valence_score + arousal_score + dominance_score) / 3.0
        
        # Calculate confidence
        total_indicators = sum(
            sum(len([w for w in model["words"] if w in text_lower]) for model in categories.values())
            for categories in self.emotional_models.values()
        )
        confidence = min(1.0, total_indicators / 10.0)
        
        return SemanticResult(
            semantic_type=SemanticType.EMOTIONAL,
            confidence=confidence,
            score=overall_score,
            details={
                "valence": scores["valence"],
                "arousal": scores["arousal"],
                "dominance": scores["dominance"],
                "overall_score": overall_score
            },
            metadata={
                "text_length": len(text),
                "indicators_found": total_indicators,
                "dimensions_analyzed": len(self.emotional_models)
            }
        )
    
    def analyze_contextual_semantics(self, text: str) -> SemanticResult:
        """
        Analyze contextual semantics in text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Contextual semantic analysis result
        """
        if not text:
            return SemanticResult(
                semantic_type=SemanticType.CONTEXTUAL,
                confidence=0.0,
                score=0.0,
                details={},
                metadata={"error": "Empty text"}
            )
        
        text_lower = text.lower()
        scores = {}
        
        # Analyze domain, temporal, and modality
        for dimension, categories in self.contextual_models.items():
            dimension_scores = {}
            for category, words in categories.items():
                word_count = sum(1 for word in words if word in text_lower)
                dimension_scores[category] = word_count
            
            # Normalize scores
            total_score = sum(dimension_scores.values())
            if total_score != 0:
                dimension_scores = {k: v / total_score for k, v in dimension_scores.items()}
            
            scores[dimension] = dimension_scores
        
        # Calculate overall contextual score
        domain_diversity = len([k for k, v in scores["domain"].items() if v > 0])
        temporal_clarity = max(scores["temporal"].values()) if scores["temporal"] else 0
        modality_strength = max(scores["modality"].values()) if scores["modality"] else 0
        
        overall_score = (domain_diversity + temporal_clarity + modality_strength) / 3.0
        
        # Calculate confidence
        total_indicators = sum(
            sum(len([w for w in words if w in text_lower]) for words in categories.values())
            for categories in self.contextual_models.values()
        )
        confidence = min(1.0, total_indicators / 15.0)
        
        return SemanticResult(
            semantic_type=SemanticType.CONTEXTUAL,
            confidence=confidence,
            score=overall_score,
            details={
                "domain": scores["domain"],
                "temporal": scores["temporal"],
                "modality": scores["modality"],
                "overall_score": overall_score
            },
            metadata={
                "text_length": len(text),
                "indicators_found": total_indicators,
                "dimensions_analyzed": len(self.contextual_models)
            }
        )
    
    def analyze_intentional_semantics(self, text: str) -> SemanticResult:
        """
        Analyze intentional semantics in text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Intentional semantic analysis result
        """
        if not text:
            return SemanticResult(
                semantic_type=SemanticType.INTENTIONAL,
                confidence=0.0,
                score=0.0,
                details={},
                metadata={"error": "Empty text"}
            )
        
        text_lower = text.lower()
        scores = {}
        
        # Analyze intent and purpose
        for dimension, categories in self.intentional_models.items():
            dimension_scores = {}
            for category, words in categories.items():
                word_count = sum(1 for word in words if word in text_lower)
                dimension_scores[category] = word_count
            
            # Normalize scores
            total_score = sum(dimension_scores.values())
            if total_score != 0:
                dimension_scores = {k: v / total_score for k, v in dimension_scores.items()}
            
            scores[dimension] = dimension_scores
        
        # Calculate overall intentional score
        intent_clarity = max(scores["intent"].values()) if scores["intent"] else 0
        purpose_strength = max(scores["purpose"].values()) if scores["purpose"] else 0
        
        overall_score = (intent_clarity + purpose_strength) / 2.0
        
        # Calculate confidence
        total_indicators = sum(
            sum(len([w for w in words if w in text_lower]) for words in categories.values())
            for categories in self.intentional_models.values()
        )
        confidence = min(1.0, total_indicators / 10.0)
        
        return SemanticResult(
            semantic_type=SemanticType.INTENTIONAL,
            confidence=confidence,
            score=overall_score,
            details={
                "intent": scores["intent"],
                "purpose": scores["purpose"],
                "overall_score": overall_score
            },
            metadata={
                "text_length": len(text),
                "indicators_found": total_indicators,
                "dimensions_analyzed": len(self.intentional_models)
            }
        )
    
    def analyze_relational_semantics(self, text: str) -> SemanticResult:
        """
        Analyze relational semantics in text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Relational semantic analysis result
        """
        if not text:
            return SemanticResult(
                semantic_type=SemanticType.RELATIONAL,
                confidence=0.0,
                score=0.0,
                details={},
                metadata={"error": "Empty text"}
            )
        
        text_lower = text.lower()
        scores = {}
        
        # Analyze social roles and emotional distance
        for dimension, categories in self.relational_models.items():
            dimension_scores = {}
            for category, words in categories.items():
                word_count = sum(1 for word in words if word in text_lower)
                dimension_scores[category] = word_count
            
            # Normalize scores
            total_score = sum(dimension_scores.values())
            if total_score != 0:
                dimension_scores = {k: v / total_score for k, v in dimension_scores.items()}
            
            scores[dimension] = dimension_scores
        
        # Calculate overall relational score
        role_clarity = max(scores["social_roles"].values()) if scores["social_roles"] else 0
        distance_clarity = max(scores["emotional_distance"].values()) if scores["emotional_distance"] else 0
        
        overall_score = (role_clarity + distance_clarity) / 2.0
        
        # Calculate confidence
        total_indicators = sum(
            sum(len([w for w in words if w in text_lower]) for words in categories.values())
            for categories in self.relational_models.values()
        )
        confidence = min(1.0, total_indicators / 10.0)
        
        return SemanticResult(
            semantic_type=SemanticType.RELATIONAL,
            confidence=confidence,
            score=overall_score,
            details={
                "social_roles": scores["social_roles"],
                "emotional_distance": scores["emotional_distance"],
                "overall_score": overall_score
            },
            metadata={
                "text_length": len(text),
                "indicators_found": total_indicators,
                "dimensions_analyzed": len(self.relational_models)
            }
        )
    
    def analyze(self, text: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Perform comprehensive semantic analysis.
        
        Args:
            text: Input text to analyze
            context: Optional context information
            
        Returns:
            Complete semantic analysis results
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
        
        # Perform all semantic analyses
        emotional_result = self.analyze_emotional_semantics(text)
        contextual_result = self.analyze_contextual_semantics(text)
        intentional_result = self.analyze_intentional_semantics(text)
        relational_result = self.analyze_relational_semantics(text)
        
        # Calculate overall scores
        all_scores = [emotional_result.score, contextual_result.score, 
                     intentional_result.score, relational_result.score]
        overall_score = sum(all_scores) / len(all_scores)
        
        all_confidences = [emotional_result.confidence, contextual_result.confidence,
                          intentional_result.confidence, relational_result.confidence]
        overall_confidence = sum(all_confidences) / len(all_confidences)
        
        return {
            "text": text,
            "context": context or {},
            "analysis": {
                "emotional": {
                    "score": emotional_result.score,
                    "confidence": emotional_result.confidence,
                    "details": emotional_result.details
                },
                "contextual": {
                    "score": contextual_result.score,
                    "confidence": contextual_result.confidence,
                    "details": contextual_result.details
                },
                "intentional": {
                    "score": intentional_result.score,
                    "confidence": intentional_result.confidence,
                    "details": intentional_result.details
                },
                "relational": {
                    "score": relational_result.score,
                    "confidence": relational_result.confidence,
                    "details": relational_result.details
                }
            },
            "overall_score": overall_score,
            "confidence": overall_confidence,
            "metadata": {
                "analyzer_version": "2.0.0",
                "analysis_types": [t.value for t in SemanticType],
                "text_length": len(text)
            }
        }
    
    def reset(self) -> None:
        """Reset the analyzer state."""
        self.logger.info("Semantic Analyzer reset")
