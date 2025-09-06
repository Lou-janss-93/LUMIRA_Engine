"""
LUMIRA Semantics Pipeline

Semantic analysis pipeline for context understanding.
"""

import re
from typing import Dict, Any, List, Optional
from datetime import datetime

from ..types import TextSample, EmotionScore, IntegritySignal


# 12-emotion lexicon (small seed)
LEXICON = {
    "joy": {
        "words": ["happy", "joy", "excited", "thrilled", "delighted", "cheerful", "optimistic", "pleased", "satisfied", "grateful", "blissful", "ecstatic", "elated", "jubilant", "merry", "glad", "content", "blij", "geweldig", "fantastisch"],
        "weight": 1.0
    },
    "sadness": {
        "words": ["sad", "sorrow", "grief", "melancholy", "depressed", "miserable", "heartbroken", "devastated", "despair", "gloomy", "downcast", "dejected", "disheartened", "crestfallen", "woeful", "mournful", "tearful", "verdrietig", "somber", "treurig"],
        "weight": 1.0
    },
    "anger": {
        "words": ["angry", "mad", "furious", "rage", "irritated", "annoyed", "frustrated", "enraged", "livid", "incensed", "outraged", "indignant", "resentful", "bitter", "hostile", "aggressive", "violent", "wrathful", "boos", "woedend", "kwaad"],
        "weight": 1.0
    },
    "fear": {
        "words": ["afraid", "scared", "terrified", "frightened", "anxious", "worried", "nervous", "panic", "dread", "horror", "alarm", "apprehension", "trepidation", "unease", "distress", "agitation", "restlessness", "tension", "bang", "angstig", "bezorgd"],
        "weight": 1.0
    },
    "surprise": {
        "words": ["surprised", "shocked", "amazed", "astonished", "startled", "stunned", "bewildered", "confused", "perplexed", "puzzled", "baffled", "mystified", "flabbergasted", "dumbfounded", "speechless", "taken aback", "caught off guard", "verrast", "verbaasd", "geschokt"],
        "weight": 1.0
    },
    "disgust": {
        "words": ["disgusted", "revolted", "repulsed", "sickened", "nauseated", "appalled", "horrified", "offended", "outraged", "scandalized", "shocked", "disturbed", "uncomfortable", "uneasy", "squeamish", "grossed out", "creeped out", "walgelijk", "afschuwelijk", "misselijk"],
        "weight": 1.0
    },
    "trust": {
        "words": ["trust", "confident", "secure", "safe", "reliable", "dependable", "faithful", "loyal", "devoted", "committed", "dedicated", "steadfast", "firm", "stable", "solid", "sure", "certain", "assured", "vertrouwen", "betrouwbaar", "veilig"],
        "weight": 1.0
    },
    "anticipation": {
        "words": ["excited", "eager", "enthusiastic", "hopeful", "optimistic", "expectant", "anticipating", "looking forward", "thrilled", "elated", "jubilant", "ecstatic", "overjoyed", "delighted", "pleased", "satisfied", "content", "verwachtingsvol", "uitkijkend", "hoopvol"],
        "weight": 1.0
    },
    "shame": {
        "words": ["ashamed", "embarrassed", "humiliated", "mortified", "disgraced", "guilty", "remorseful", "regretful", "contrite", "penitent", "apologetic", "sheepish", "abashed", "chagrined", "discomfited", "flustered", "uncomfortable", "schaamte", "beschaamd", "vernederd"],
        "weight": 1.0
    },
    "pride": {
        "words": ["proud", "accomplished", "achieved", "successful", "victorious", "triumphant", "elated", "exultant", "jubilant", "ecstatic", "thrilled", "delighted", "pleased", "satisfied", "content", "fulfilled", "gratified", "trots", "trots", "geslaagd"],
        "weight": 1.0
    },
    "love": {
        "words": ["love", "adore", "cherish", "treasure", "beloved", "darling", "sweetheart", "honey", "dear", "close", "intimate", "affectionate", "tender", "warm", "caring", "devoted", "passionate", "romantic", "liefde", "houden van", "dierbaar"],
        "weight": 1.0
    },
    "contempt": {
        "words": ["contempt", "disdain", "scorn", "derision", "mockery", "ridicule", "sarcasm", "cynicism", "skepticism", "doubt", "suspicion", "mistrust", "disbelief", "incredulity", "amazement", "astonishment", "surprise", "minachting", "verachting", "spot"],
        "weight": 1.0
    }
}

# Future tense and promise patterns
FUTURE_TENSE_PATTERNS = [
    r'\b(will|shall|going to|gonna|plan to|intend to|promise to|commit to|guarantee to)\b',
    r'\b(soon|later|eventually|tomorrow|next|future|ahead|coming)\b',
    r'\b(expect|anticipate|look forward to|hope to|wish to|want to)\b'
]

# Negation patterns
NEGATION_PATTERNS = [
    r'\b(not|no|never|nothing|nobody|nowhere|neither|nor|none|n\'t|won\'t|can\'t|don\'t|doesn\'t|didn\'t|haven\'t|hasn\'t|hadn\'t|shouldn\'t|wouldn\'t|couldn\'t|mustn\'t)\b',
    r'\b(without|lack|missing|absent|devoid|free from|exempt from)\b'
]


class SemanticPipeline:
    """
    Semantic analysis pipeline.
    
    Provides lightweight semantic analysis and context understanding
    capabilities for the LUMIRA framework.
    """
    
    def __init__(self):
        """Initialize the semantic pipeline."""
        self.lexicon = LEXICON
        self.future_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in FUTURE_TENSE_PATTERNS]
        self.negation_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in NEGATION_PATTERNS]
    
    def featurize(self, sample: TextSample) -> Dict[str, Any]:
        """
        Extract features from a text sample.
        
        Args:
            sample: Text sample to analyze
            
        Returns:
            Dictionary of extracted features
        """
        text = sample.text.lower()
        
        features = {
            "text_length": len(sample.text),
            "word_count": len(sample.text.split()),
            "sentence_count": len(re.split(r'[.!?]+', sample.text)),
            "has_question": '?' in sample.text,
            "has_exclamation": '!' in sample.text,
            "has_quotes": '"' in sample.text or "'" in sample.text,
            "emotion_indicators": {},
            "future_tense_count": 0,
            "negation_count": 0,
            "incongruence_indicators": []
        }
        
        # Count emotion indicators
        for emotion, data in self.lexicon.items():
            count = sum(1 for word in data["words"] if word in text)
            features["emotion_indicators"][emotion] = count
        
        # Count future tense patterns
        for pattern in self.future_patterns:
            features["future_tense_count"] += len(pattern.findall(sample.text))
        
        # Count negation patterns
        for pattern in self.negation_patterns:
            features["negation_count"] += len(pattern.findall(sample.text))
        
        # Detect incongruence indicators
        features["incongruence_indicators"] = self._detect_incongruence_indicators(sample.text)
        
        return features
    
    def classify_emotions(self, sample: TextSample) -> List[EmotionScore]:
        """
        Classify emotions in a text sample.
        
        Args:
            sample: Text sample to analyze
            
        Returns:
            List of emotion scores
        """
        text = sample.text.lower()
        emotion_scores = []
        
        for emotion, data in self.lexicon.items():
            # Count word matches
            word_count = sum(1 for word in data["words"] if word in text)
            
            # Calculate score (normalized by text length)
            if len(sample.text.split()) > 0:
                score = min(1.0, (word_count * data["weight"]) / len(sample.text.split()))
            else:
                score = 0.0
            
            # Only include emotions with non-zero scores
            if score > 0:
                emotion_scores.append(EmotionScore(name=emotion, score=score))
        
        # Sort by score (highest first)
        emotion_scores.sort(key=lambda x: x.score, reverse=True)
        
        return emotion_scores
    
    def detect_incongruence(self, text: str, claims: Optional[List[str]] = None) -> List[IntegritySignal]:
        """
        Detect incongruence in text.
        
        Args:
            text: Text to analyze
            claims: Optional list of claims to check against
            
        Returns:
            List of integrity signals
        """
        signals = []
        
        # Check for future-tense + negation pattern
        future_tense_found = any(pattern.search(text) for pattern in self.future_patterns)
        negation_found = any(pattern.search(text) for pattern in self.negation_patterns)
        
        if future_tense_found and negation_found:
            signals.append(IntegritySignal(
                level="low",
                reason="Future-tense promise with negation detected",
                weight=0.3,
                details={
                    "pattern": "future_tense_negation",
                    "future_tense_count": sum(len(pattern.findall(text)) for pattern in self.future_patterns),
                    "negation_count": sum(len(pattern.findall(text)) for pattern in self.negation_patterns)
                }
            ))
        
        # Check for contradictory claims if provided
        if claims:
            contradictions = self._find_contradictions(text, claims)
            for contradiction in contradictions:
                signals.append(IntegritySignal(
                    level="medium",
                    reason=f"Contradiction detected: {contradiction['reason']}",
                    weight=0.7,
                    details=contradiction
                ))
        
        return signals
    
    def _detect_incongruence_indicators(self, text: str) -> List[str]:
        """Detect incongruence indicators in text."""
        indicators = []
        
        # Check for future-tense + negation
        if (any(pattern.search(text) for pattern in self.future_patterns) and
            any(pattern.search(text) for pattern in self.negation_patterns)):
            indicators.append("future_tense_negation")
        
        # Check for emotional contradictions
        emotion_scores = self.classify_emotions(TextSample(
            id="temp", ts=datetime.now(), source="temp", text=text, meta={}
        ))
        
        if len(emotion_scores) > 1:
            # Check for conflicting emotions (e.g., joy + sadness)
            conflicting_pairs = [
                ("joy", "sadness"), ("love", "contempt"), ("trust", "fear"),
                ("pride", "shame"), ("anticipation", "fear")
            ]
            
            for pos_emotion, neg_emotion in conflicting_pairs:
                pos_score = next((e.score for e in emotion_scores if e.name == pos_emotion), 0)
                neg_score = next((e.score for e in emotion_scores if e.name == neg_emotion), 0)
                
                if pos_score > 0.3 and neg_score > 0.3:
                    indicators.append(f"conflicting_emotions_{pos_emotion}_{neg_emotion}")
        
        return indicators
    
    def _find_contradictions(self, text: str, claims: List[str]) -> List[Dict[str, Any]]:
        """Find contradictions between text and claims."""
        contradictions = []
        
        # Simple keyword-based contradiction detection
        text_lower = text.lower()
        
        for claim in claims:
            claim_lower = claim.lower()
            
            # Check for direct contradictions
            if "not" in claim_lower and "not" not in text_lower:
                # Claim says "not X" but text doesn't contain "not"
                if any(word in text_lower for word in claim_lower.split() if word != "not"):
                    contradictions.append({
                        "reason": f"Claim '{claim}' contradicts text",
                        "claim": claim,
                        "text_excerpt": text[:100] + "..." if len(text) > 100 else text
                    })
        
        return contradictions
