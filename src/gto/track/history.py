"""
History Management Module

This module provides tools for managing and analyzing data history.
"""

from typing import Dict, Any, List
import pandas as pd
import numpy as np
from datetime import datetime

class HistoryManager:
    """Manages and analyzes data history."""
    
    def __init__(self):
        """Initialize the history manager."""
        self.history = {}
    
    def add_to_history(self, data: pd.DataFrame, name: str) -> str:
        """
        Add a new entry to the data history.
        
        Args:
            data: Data to add to history
            name: Name of the data
            
        Returns:
            str: History entry ID
        """
        entry_id = datetime.now().isoformat()
        
        self.history[entry_id] = {
            "timestamp": entry_id,
            "name": name,
            "shape": data.shape,
            "columns": list(data.columns),
            "dtypes": data.dtypes.to_dict(),
            "summary": data.describe().to_dict()
        }
        
        return entry_id
    
    def get_history(self, name: str) -> List[Dict[str, Any]]:
        """
        Get history for a specific data set.
        
        Args:
            name: Name of the data set
            
        Returns:
            List[Dict[str, Any]]: List of history entries
        """
        return [
            entry for entry in self.history.values()
            if entry["name"] == name
        ]
    
    def analyze_history(self, name: str) -> Dict[str, Any]:
        """
        Analyze the history of a data set.
        
        Args:
            name: Name of the data set
            
        Returns:
            Dict[str, Any]: Analysis results
        """
        entries = self.get_history(name)
        if not entries:
            return {"error": "No history found"}
        
        analysis = {
            "total_entries": len(entries),
            "time_span": {
                "start": entries[0]["timestamp"],
                "end": entries[-1]["timestamp"]
            },
            "shape_changes": [],
            "column_changes": [],
            "dtype_changes": []
        }
        
        # Analyze changes between consecutive entries
        for i in range(1, len(entries)):
            prev = entries[i-1]
            curr = entries[i]
            
            if prev["shape"] != curr["shape"]:
                analysis["shape_changes"].append({
                    "timestamp": curr["timestamp"],
                    "from": prev["shape"],
                    "to": curr["shape"]
                })
            
            prev_cols = set(prev["columns"])
            curr_cols = set(curr["columns"])
            
            if prev_cols != curr_cols:
                analysis["column_changes"].append({
                    "timestamp": curr["timestamp"],
                    "added": list(curr_cols - prev_cols),
                    "removed": list(prev_cols - curr_cols)
                })
            
            for col in prev_cols & curr_cols:
                if prev["dtypes"][col] != curr["dtypes"][col]:
                    analysis["dtype_changes"].append({
                        "timestamp": curr["timestamp"],
                        "column": col,
                        "from": prev["dtypes"][col],
                        "to": curr["dtypes"][col]
                    })
        
        return analysis 