"""
LUMIRA Signals Light Store

Lightweight signal storage and retrieval.
"""

import json
import os
from typing import Dict, Any, List, Optional
from datetime import datetime


class LightweightSignalStore:
    """
    Lightweight signal store for LUMIRA.
    
    Provides simple signal storage and retrieval
    capabilities for the LUMIRA framework using JSONL format.
    """
    
    def __init__(self, path: str = "signals.jsonl"):
        """
        Initialize the signal store.
        
        Args:
            path: Path to the signal store file
        """
        self.path = path
        self._ensure_directory()
    
    def _ensure_directory(self) -> None:
        """Ensure the directory for the signal store exists."""
        directory = os.path.dirname(self.path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
    
    def append_emotions(self, sample_id: str, ts: datetime, emotions: List[Dict[str, Any]]) -> None:
        """
        Append emotion data to the store.
        
        Args:
            sample_id: Sample identifier
            ts: Timestamp
            emotions: List of emotion scores
        """
        record = {
            "type": "emotions",
            "sample_id": sample_id,
            "timestamp": ts.isoformat(),
            "data": emotions
        }
        self._append_record(record)
    
    def append_risks(self, sample_id: str, ts: datetime, risks: List[Dict[str, Any]]) -> None:
        """
        Append risk data to the store.
        
        Args:
            sample_id: Sample identifier
            ts: Timestamp
            risks: List of risk flags
        """
        record = {
            "type": "risks",
            "sample_id": sample_id,
            "timestamp": ts.isoformat(),
            "data": risks
        }
        self._append_record(record)
    
    def append_integrity(self, sample_id: str, ts: datetime, signals: List[Dict[str, Any]]) -> None:
        """
        Append integrity signal data to the store.
        
        Args:
            sample_id: Sample identifier
            ts: Timestamp
            signals: List of integrity signals
        """
        record = {
            "type": "integrity",
            "sample_id": sample_id,
            "timestamp": ts.isoformat(),
            "data": signals
        }
        self._append_record(record)
    
    def load(self) -> List[Dict[str, Any]]:
        """
        Load all records from the store.
        
        Returns:
            List of all records
        """
        if not os.path.exists(self.path):
            return []
        
        records = []
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        record = json.loads(line)
                        records.append(record)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Error loading signal store: {e}")
            return []
        
        return records
    
    def load_by_type(self, record_type: str) -> List[Dict[str, Any]]:
        """
        Load records by type.
        
        Args:
            record_type: Type of records to load ('emotions', 'risks', 'integrity')
            
        Returns:
            List of records of the specified type
        """
        all_records = self.load()
        return [record for record in all_records if record.get("type") == record_type]
    
    def load_by_sample(self, sample_id: str) -> List[Dict[str, Any]]:
        """
        Load records by sample ID.
        
        Args:
            sample_id: Sample identifier
            
        Returns:
            List of records for the specified sample
        """
        all_records = self.load()
        return [record for record in all_records if record.get("sample_id") == sample_id]
    
    def load_recent(self, days: int = 7) -> List[Dict[str, Any]]:
        """
        Load recent records within specified days.
        
        Args:
            days: Number of days to look back
            
        Returns:
            List of recent records
        """
        all_records = self.load()
        cutoff_date = datetime.now().timestamp() - (days * 24 * 60 * 60)
        
        recent_records = []
        for record in all_records:
            try:
                record_ts = datetime.fromisoformat(record["timestamp"]).timestamp()
                if record_ts >= cutoff_date:
                    recent_records.append(record)
            except (ValueError, KeyError):
                # Skip records with invalid timestamps
                continue
        
        return recent_records
    
    def clear(self) -> None:
        """Clear all records from the store."""
        if os.path.exists(self.path):
            os.remove(self.path)
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the store.
        
        Returns:
            Dictionary with store statistics
        """
        records = self.load()
        
        stats = {
            "total_records": len(records),
            "by_type": {},
            "by_sample": {},
            "date_range": {"earliest": None, "latest": None}
        }
        
        if not records:
            return stats
        
        # Count by type and sample
        for record in records:
            record_type = record.get("type", "unknown")
            sample_id = record.get("sample_id", "unknown")
            
            stats["by_type"][record_type] = stats["by_type"].get(record_type, 0) + 1
            stats["by_sample"][sample_id] = stats["by_sample"].get(sample_id, 0) + 1
        
        # Find date range
        timestamps = []
        for record in records:
            try:
                ts = datetime.fromisoformat(record["timestamp"])
                timestamps.append(ts)
            except (ValueError, KeyError):
                continue
        
        if timestamps:
            stats["date_range"]["earliest"] = min(timestamps).isoformat()
            stats["date_range"]["latest"] = max(timestamps).isoformat()
        
        return stats
    
    def _append_record(self, record: Dict[str, Any]) -> None:
        """Append a record to the JSONL file."""
        try:
            with open(self.path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(record, ensure_ascii=False) + '\n')
        except IOError as e:
            print(f"Warning: Error appending to signal store: {e}")