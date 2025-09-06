"""
Context Analyzer

Specialized context analysis for understanding situational context,
domain-specific meaning, and contextual relationships in text.
"""

import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

from ..utils.logging import get_logger


class ContextType(Enum):
    """Types of context analysis."""
    DOMAIN = "domain"
    TEMPORAL = "temporal"
    SPATIAL = "spatial"
    SOCIAL = "social"
    CULTURAL = "cultural"


@dataclass
class ContextResult:
    """Result of context analysis."""
    context_type: ContextType
    confidence: float
    score: float
    details: Dict[str, Any]
    metadata: Dict[str, Any]


class ContextAnalyzer:
    """
    Specialized context analyzer for understanding situational context.
    
    Provides:
    - Domain context analysis
    - Temporal context understanding
    - Spatial context detection
    - Social context analysis
    - Cultural context recognition
    """
    
    def __init__(self):
        """Initialize the context analyzer."""
        self.logger = get_logger(__name__)
        
        # Initialize context models
        self._init_domain_models()
        self._init_temporal_models()
        self._init_spatial_models()
        self._init_social_models()
        self._init_cultural_models()
        
        self.logger.info("Context Analyzer initialized")
    
    def _init_domain_models(self) -> None:
        """Initialize domain context models."""
        self.domain_models = {
            "work": {
                "keywords": ["work", "job", "office", "meeting", "project", "deadline", "colleague", "boss", "manager", "team", "business", "professional", "career", "employment", "task", "assignment", "report", "presentation"],
                "weight": 1.0
            },
            "personal": {
                "keywords": ["family", "friend", "home", "personal", "private", "relationship", "partner", "spouse", "child", "parent", "sibling", "relative", "love", "marriage", "dating", "romance"],
                "weight": 1.0
            },
            "health": {
                "keywords": ["health", "sick", "ill", "doctor", "hospital", "medicine", "pain", "tired", "exhausted", "medical", "treatment", "therapy", "recovery", "wellness", "fitness", "exercise", "diet"],
                "weight": 1.0
            },
            "social": {
                "keywords": ["party", "social", "event", "gathering", "celebration", "festival", "conference", "meeting", "group", "community", "society", "public", "crowd", "audience", "spectators"],
                "weight": 1.0
            },
            "academic": {
                "keywords": ["study", "school", "university", "college", "education", "learning", "research", "academic", "student", "teacher", "professor", "course", "class", "lecture", "exam", "test", "assignment"],
                "weight": 1.0
            },
            "financial": {
                "keywords": ["money", "financial", "budget", "cost", "price", "expensive", "cheap", "affordable", "investment", "savings", "debt", "income", "salary", "wage", "payment", "bill", "expense"],
                "weight": 1.0
            },
            "technology": {
                "keywords": ["computer", "software", "hardware", "technology", "digital", "online", "internet", "website", "app", "program", "code", "data", "system", "network", "device", "gadget"],
                "weight": 1.0
            },
            "entertainment": {
                "keywords": ["movie", "film", "music", "book", "game", "sport", "entertainment", "fun", "enjoyment", "leisure", "hobby", "recreation", "vacation", "travel", "adventure"],
                "weight": 1.0
            }
        }
    
    def _init_temporal_models(self) -> None:
        """Initialize temporal context models."""
        self.temporal_models = {
            "past": {
                "keywords": ["was", "were", "had", "did", "went", "came", "saw", "heard", "felt", "thought", "remembered", "recalled", "yesterday", "before", "ago", "previously", "earlier", "once", "used to"],
                "weight": 1.0
            },
            "present": {
                "keywords": ["am", "is", "are", "have", "has", "do", "does", "go", "goes", "come", "comes", "see", "sees", "hear", "hears", "feel", "feels", "think", "thinks", "now", "today", "currently", "at the moment", "right now"],
                "weight": 1.0
            },
            "future": {
                "keywords": ["will", "shall", "going to", "gonna", "tomorrow", "next", "soon", "later", "eventually", "plan", "intend", "expect", "hope", "anticipate", "predict", "forecast", "upcoming", "forthcoming"],
                "weight": 1.0
            }
        }
    
    def _init_spatial_models(self) -> None:
        """Initialize spatial context models."""
        self.spatial_models = {
            "indoor": {
                "keywords": ["inside", "indoor", "room", "house", "home", "office", "building", "apartment", "kitchen", "bedroom", "living room", "bathroom", "garage", "basement", "attic"],
                "weight": 1.0
            },
            "outdoor": {
                "keywords": ["outside", "outdoor", "street", "park", "garden", "yard", "beach", "mountain", "forest", "field", "road", "sidewalk", "playground", "stadium", "arena"],
                "weight": 1.0
            },
            "public": {
                "keywords": ["public", "restaurant", "store", "shop", "mall", "hospital", "school", "library", "museum", "theater", "cinema", "airport", "station", "bus", "train", "subway"],
                "weight": 1.0
            },
            "private": {
                "keywords": ["private", "personal", "home", "house", "apartment", "room", "bedroom", "office", "study", "workshop", "studio", "garage", "basement"],
                "weight": 1.0
            }
        }
    
    def _init_social_models(self) -> None:
        """Initialize social context models."""
        self.social_models = {
            "formal": {
                "keywords": ["formal", "official", "professional", "business", "meeting", "conference", "presentation", "interview", "ceremony", "event", "occasion", "gathering", "function"],
                "weight": 1.0
            },
            "informal": {
                "keywords": ["casual", "informal", "relaxed", "friendly", "chat", "conversation", "talk", "discussion", "hangout", "get-together", "party", "celebration", "fun"],
                "weight": 1.0
            },
            "intimate": {
                "keywords": ["intimate", "personal", "private", "close", "family", "loved", "dear", "beloved", "romantic", "romance", "love", "affection", "tender", "warm"],
                "weight": 1.0
            },
            "group": {
                "keywords": ["group", "team", "crowd", "audience", "spectators", "participants", "members", "colleagues", "friends", "family", "community", "society", "public"],
                "weight": 1.0
            }
        }
    
    def _init_cultural_models(self) -> None:
        """Initialize cultural context models."""
        self.cultural_models = {
            "western": {
                "keywords": ["democracy", "freedom", "individual", "rights", "liberty", "equality", "justice", "law", "order", "system", "institution", "government", "society", "culture"],
                "weight": 1.0
            },
            "eastern": {
                "keywords": ["harmony", "balance", "tradition", "respect", "honor", "duty", "obligation", "family", "community", "collective", "wisdom", "philosophy", "spirituality", "meditation"],
                "weight": 1.0
            },
            "religious": {
                "keywords": ["god", "prayer", "faith", "belief", "spiritual", "divine", "sacred", "holy", "blessing", "grace", "mercy", "forgiveness", "salvation", "eternal", "heaven"],
                "weight": 1.0
            },
            "secular": {
                "keywords": ["science", "reason", "logic", "evidence", "fact", "truth", "reality", "material", "physical", "natural", "human", "rational", "empirical", "objective"],
                "weight": 1.0
            }
        }
    
    def analyze_domain_context(self, text: str) -> ContextResult:
        """
        Analyze domain context in text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Domain context analysis result
        """
        if not text:
            return ContextResult(
                context_type=ContextType.DOMAIN,
                confidence=0.0,
                score=0.0,
                details={},
                metadata={"error": "Empty text"}
            )
        
        text_lower = text.lower()
        scores = {}
        
        for domain, model in self.domain_models.items():
            word_count = sum(1 for word in model["keywords"] if word in text_lower)
            score = word_count * model["weight"]
            scores[domain] = score
        
        # Normalize scores
        total_score = sum(scores.values())
        if total_score > 0:
            scores = {k: v / total_score for k, v in scores.items()}
        
        # Find dominant domain
        dominant_domain = max(scores.items(), key=lambda x: x[1])[0] if scores else "unknown"
        
        # Calculate confidence
        confidence = min(1.0, total_score / 10.0)
        
        return ContextResult(
            context_type=ContextType.DOMAIN,
            confidence=confidence,
            score=scores.get(dominant_domain, 0.0),
            details={
                "scores": scores,
                "dominant_domain": dominant_domain,
                "total_indicators": total_score
            },
            metadata={
                "text_length": len(text),
                "domains_analyzed": len(self.domain_models)
            }
        )
    
    def analyze_temporal_context(self, text: str) -> ContextResult:
        """
        Analyze temporal context in text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Temporal context analysis result
        """
        if not text:
            return ContextResult(
                context_type=ContextType.TEMPORAL,
                confidence=0.0,
                score=0.0,
                details={},
                metadata={"error": "Empty text"}
            )
        
        text_lower = text.lower()
        scores = {}
        
        for temporal, model in self.temporal_models.items():
            word_count = sum(1 for word in model["keywords"] if word in text_lower)
            score = word_count * model["weight"]
            scores[temporal] = score
        
        # Normalize scores
        total_score = sum(scores.values())
        if total_score > 0:
            scores = {k: v / total_score for k, v in scores.items()}
        
        # Find dominant temporal context
        dominant_temporal = max(scores.items(), key=lambda x: x[1])[0] if scores else "unknown"
        
        # Calculate confidence
        confidence = min(1.0, total_score / 5.0)
        
        return ContextResult(
            context_type=ContextType.TEMPORAL,
            confidence=confidence,
            score=scores.get(dominant_temporal, 0.0),
            details={
                "scores": scores,
                "dominant_temporal": dominant_temporal,
                "total_indicators": total_score
            },
            metadata={
                "text_length": len(text),
                "temporal_contexts_analyzed": len(self.temporal_models)
            }
        )
    
    def analyze_spatial_context(self, text: str) -> ContextResult:
        """
        Analyze spatial context in text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Spatial context analysis result
        """
        if not text:
            return ContextResult(
                context_type=ContextType.SPATIAL,
                confidence=0.0,
                score=0.0,
                details={},
                metadata={"error": "Empty text"}
            )
        
        text_lower = text.lower()
        scores = {}
        
        for spatial, model in self.spatial_models.items():
            word_count = sum(1 for word in model["keywords"] if word in text_lower)
            score = word_count * model["weight"]
            scores[spatial] = score
        
        # Normalize scores
        total_score = sum(scores.values())
        if total_score > 0:
            scores = {k: v / total_score for k, v in scores.items()}
        
        # Find dominant spatial context
        dominant_spatial = max(scores.items(), key=lambda x: x[1])[0] if scores else "unknown"
        
        # Calculate confidence
        confidence = min(1.0, total_score / 5.0)
        
        return ContextResult(
            context_type=ContextType.SPATIAL,
            confidence=confidence,
            score=scores.get(dominant_spatial, 0.0),
            details={
                "scores": scores,
                "dominant_spatial": dominant_spatial,
                "total_indicators": total_score
            },
            metadata={
                "text_length": len(text),
                "spatial_contexts_analyzed": len(self.spatial_models)
            }
        )
    
    def analyze_social_context(self, text: str) -> ContextResult:
        """
        Analyze social context in text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Social context analysis result
        """
        if not text:
            return ContextResult(
                context_type=ContextType.SOCIAL,
                confidence=0.0,
                score=0.0,
                details={},
                metadata={"error": "Empty text"}
            )
        
        text_lower = text.lower()
        scores = {}
        
        for social, model in self.social_models.items():
            word_count = sum(1 for word in model["keywords"] if word in text_lower)
            score = word_count * model["weight"]
            scores[social] = score
        
        # Normalize scores
        total_score = sum(scores.values())
        if total_score > 0:
            scores = {k: v / total_score for k, v in scores.items()}
        
        # Find dominant social context
        dominant_social = max(scores.items(), key=lambda x: x[1])[0] if scores else "unknown"
        
        # Calculate confidence
        confidence = min(1.0, total_score / 5.0)
        
        return ContextResult(
            context_type=ContextType.SOCIAL,
            confidence=confidence,
            score=scores.get(dominant_social, 0.0),
            details={
                "scores": scores,
                "dominant_social": dominant_social,
                "total_indicators": total_score
            },
            metadata={
                "text_length": len(text),
                "social_contexts_analyzed": len(self.social_models)
            }
        )
    
    def analyze_cultural_context(self, text: str) -> ContextResult:
        """
        Analyze cultural context in text.
        
        Args:
            text: Input text to analyze
            
        Returns:
            Cultural context analysis result
        """
        if not text:
            return ContextResult(
                context_type=ContextType.CULTURAL,
                confidence=0.0,
                score=0.0,
                details={},
                metadata={"error": "Empty text"}
            )
        
        text_lower = text.lower()
        scores = {}
        
        for cultural, model in self.cultural_models.items():
            word_count = sum(1 for word in model["keywords"] if word in text_lower)
            score = word_count * model["weight"]
            scores[cultural] = score
        
        # Normalize scores
        total_score = sum(scores.values())
        if total_score > 0:
            scores = {k: v / total_score for k, v in scores.items()}
        
        # Find dominant cultural context
        dominant_cultural = max(scores.items(), key=lambda x: x[1])[0] if scores else "unknown"
        
        # Calculate confidence
        confidence = min(1.0, total_score / 5.0)
        
        return ContextResult(
            context_type=ContextType.CULTURAL,
            confidence=confidence,
            score=scores.get(dominant_cultural, 0.0),
            details={
                "scores": scores,
                "dominant_cultural": dominant_cultural,
                "total_indicators": total_score
            },
            metadata={
                "text_length": len(text),
                "cultural_contexts_analyzed": len(self.cultural_models)
            }
        )
    
    def analyze(self, text: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Perform comprehensive context analysis.
        
        Args:
            text: Input text to analyze
            context: Optional context information
            
        Returns:
            Complete context analysis results
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
        
        # Perform all context analyses
        domain_result = self.analyze_domain_context(text)
        temporal_result = self.analyze_temporal_context(text)
        spatial_result = self.analyze_spatial_context(text)
        social_result = self.analyze_social_context(text)
        cultural_result = self.analyze_cultural_context(text)
        
        # Calculate overall scores
        all_scores = [domain_result.score, temporal_result.score, 
                     spatial_result.score, social_result.score, cultural_result.score]
        overall_score = sum(all_scores) / len(all_scores)
        
        all_confidences = [domain_result.confidence, temporal_result.confidence,
                          spatial_result.confidence, social_result.confidence, cultural_result.confidence]
        overall_confidence = sum(all_confidences) / len(all_confidences)
        
        return {
            "text": text,
            "context": context or {},
            "analysis": {
                "domain": {
                    "score": domain_result.score,
                    "confidence": domain_result.confidence,
                    "details": domain_result.details
                },
                "temporal": {
                    "score": temporal_result.score,
                    "confidence": temporal_result.confidence,
                    "details": temporal_result.details
                },
                "spatial": {
                    "score": spatial_result.score,
                    "confidence": spatial_result.confidence,
                    "details": spatial_result.details
                },
                "social": {
                    "score": social_result.score,
                    "confidence": social_result.confidence,
                    "details": social_result.details
                },
                "cultural": {
                    "score": cultural_result.score,
                    "confidence": cultural_result.confidence,
                    "details": cultural_result.details
                }
            },
            "overall_score": overall_score,
            "confidence": overall_confidence,
            "metadata": {
                "analyzer_version": "2.0.0",
                "context_types": [t.value for t in ContextType],
                "text_length": len(text)
            }
        }
    
    def reset(self) -> None:
        """Reset the analyzer state."""
        self.logger.info("Context Analyzer reset")
