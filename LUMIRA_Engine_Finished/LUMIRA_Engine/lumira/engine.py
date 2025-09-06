"""
LUMIRA Engine

Main engine orchestration for the LUMIRA framework.
"""

from typing import Dict, Any, Optional, List
from datetime import datetime

from .config import LUMIRAConfig, env_bool
from .types import (
    TextSample, AnalysisReport, EmotionScore, IntegritySignal, RiskFlag
)
from .semantics import SemanticPipeline
from .safety import SafetyDetector
from .signals import LightweightSignalStore, downhill_alert


class LumiraEngine:
    """
    Main LUMIRA engine.
    
    Orchestrates the various LUMIRA modules and provides
    the main interface for text analysis and processing.
    """
    
    def __init__(self, base_engine=None, store_path: Optional[str] = None, flags: Optional[Dict[str, bool]] = None):
        """
        Initialize the LUMIRA engine.
        
        Args:
            base_engine: Optional existing EFC engine instance for backward compatibility
            store_path: Optional path for signal store
            flags: Optional feature flags dictionary
        """
        self.base_engine = base_engine
        self.config = LUMIRAConfig()
        
        # Override config with provided flags
        if flags:
            for key, value in flags.items():
                if hasattr(self.config, key):
                    setattr(self.config, key, value)
        
        # Initialize modules based on feature flags
        self.semantic_pipeline = None
        self.safety_detector = None
        self.signal_store = None
        
        if self.config.LUMIRA_SEMANTICS_ENABLED:
            self.semantic_pipeline = SemanticPipeline()
        
        if self.config.LUMIRA_SAFETY_ENABLED:
            self.safety_detector = SafetyDetector()
        
        if self.config.LUMIRA_SIGNALS_ENABLED:
            store_path = store_path or self.config.LUMIRA_DB_PATH
            self.signal_store = LightweightSignalStore(store_path)
    
    def process_sample(self, sample: TextSample) -> AnalysisReport:
        """
        Process a text sample through the LUMIRA pipeline.
        
        Args:
            sample: Text sample to analyze
            
        Returns:
            Complete analysis report
        """
        emotions = []
        integrity_signals = []
        risks = []
        
        # Run semantic analysis if enabled
        if self.semantic_pipeline and self.config.LUMIRA_SEMANTICS_ENABLED:
            try:
                # Classify emotions
                emotions = self.semantic_pipeline.classify_emotions(sample)
                
                # Detect incongruence
                incongruence_signals = self.semantic_pipeline.detect_incongruence(sample.text)
                integrity_signals.extend(incongruence_signals)
                
            except Exception as e:
                print(f"Warning: Semantic analysis failed: {e}")
        
        # Run safety analysis if enabled
        if self.safety_detector and self.config.LUMIRA_SAFETY_ENABLED:
            try:
                # Analyze for safety risks
                risks = self.safety_detector.analyze(sample)
                
                # Escalate if needed
                escalation_signals = self.safety_detector.escalate_if_needed(risks, sample.meta)
                integrity_signals.extend(escalation_signals)
                
            except Exception as e:
                print(f"Warning: Safety analysis failed: {e}")
        
        # Store signals if enabled
        if self.signal_store and self.config.LUMIRA_SIGNALS_ENABLED:
            try:
                # Convert to serializable format
                emotions_data = [{"name": e.name, "score": e.score} for e in emotions]
                risks_data = [
                    {
                        "kind": r.kind,
                        "level": r.level,
                        "confidence": r.confidence,
                        "excerpt": r.excerpt,
                        "ts": r.ts.isoformat()
                    } for r in risks
                ]
                integrity_data = [
                    {
                        "level": s.level,
                        "reason": s.reason,
                        "weight": s.weight,
                        "details": s.details
                    } for s in integrity_signals
                ]
                
                # Store in signal store
                if emotions_data:
                    self.signal_store.append_emotions(sample.id, sample.ts, emotions_data)
                if risks_data:
                    self.signal_store.append_risks(sample.id, sample.ts, risks_data)
                if integrity_data:
                    self.signal_store.append_integrity(sample.id, sample.ts, integrity_data)
                    
            except Exception as e:
                print(f"Warning: Signal storage failed: {e}")
        
        # Create analysis report
        report = AnalysisReport(
            sample_id=sample.id,
            emotions=emotions,
            integrity=integrity_signals,
            risks=risks
        )
        
        return report
    
    def analyze_window(self, days: int = 7) -> Optional[Dict[str, Any]]:
        """
        Analyze trends over a time window.
        
        Args:
            days: Number of days to analyze
            
        Returns:
            Trend analysis results or None if no data
        """
        if not self.signal_store or not self.config.LUMIRA_SIGNALS_ENABLED:
            return None
        
        try:
            # Load recent records
            records = self.signal_store.load_recent(days)
            
            if not records:
                return None
            
            # Run downhill alert analysis
            alert = downhill_alert(records, window_days=days)
            
            if alert:
                return {
                    "alert_detected": True,
                    "alert": alert,
                    "window_days": days,
                    "total_records": len(records)
                }
            else:
                return {
                    "alert_detected": False,
                    "window_days": days,
                    "total_records": len(records)
                }
                
        except Exception as e:
            print(f"Warning: Window analysis failed: {e}")
            return None
    
    def get_signal_stats(self) -> Dict[str, Any]:
        """
        Get statistics about stored signals.
        
        Returns:
            Signal store statistics
        """
        if not self.signal_store or not self.config.LUMIRA_SIGNALS_ENABLED:
            return {"enabled": False}
        
        try:
            stats = self.signal_store.get_stats()
            stats["enabled"] = True
            return stats
        except Exception as e:
            print(f"Warning: Failed to get signal stats: {e}")
            return {"enabled": False, "error": str(e)}
    
    def is_enabled(self) -> bool:
        """
        Check if LUMIRA is enabled.
        
        Returns:
            True if LUMIRA is enabled
        """
        return self.config.LUMIRA_ENABLED
    
    def get_module_status(self) -> Dict[str, bool]:
        """
        Get status of all modules.
        
        Returns:
            Dictionary with module enablement status
        """
        return {
            "lumira_enabled": self.config.LUMIRA_ENABLED,
            "semantics_enabled": self.config.LUMIRA_SEMANTICS_ENABLED,
            "safety_enabled": self.config.LUMIRA_SAFETY_ENABLED,
            "signals_enabled": self.config.LUMIRA_SIGNALS_ENABLED,
            "semantic_pipeline_loaded": self.semantic_pipeline is not None,
            "safety_detector_loaded": self.safety_detector is not None,
            "signal_store_loaded": self.signal_store is not None
        }


def integrate_with_existing_efc(engine) -> LumiraEngine:
    """
    Factory helper to integrate with existing EFC engine.
    
    Wraps the current engine without modifying it.
    
    Args:
        engine: Existing EFC engine instance
        
    Returns:
        New LUMIRA engine instance with EFC integration
    """
    # Create LUMIRA engine with EFC as base
    lumira_engine = LumiraEngine(base_engine=engine)
    
    # Add EFC-specific integration if needed
    if hasattr(engine, 'process') and callable(engine.process):
        # Store reference to EFC process method
        lumira_engine._efc_process = engine.process
    
    return lumira_engine