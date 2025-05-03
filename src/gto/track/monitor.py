"""
State Monitor Module

This module provides tools for monitoring data state and detecting changes.
"""

from typing import Dict, Any, List
import pandas as pd
import numpy as np
from datetime import datetime

class StateMonitor:
    """Monitors and detects changes in data state."""
    
    def __init__(self):
        """Initialize the state monitor."""
        self.states = {}
    
    def capture_state(self, data: pd.DataFrame, name: str) -> Dict[str, Any]:
        """
        Capture the current state of data.
        
        Args:
            data: Data to monitor
            name: Name of the data
            
        Returns:
            Dict[str, Any]: State information
        """
        state = {
            "timestamp": datetime.now().isoformat(),
            "name": name,
            "shape": data.shape,
            "columns": list(data.columns),
            "dtypes": data.dtypes.to_dict(),
            "summary": data.describe().to_dict(),
            "null_counts": data.isnull().sum().to_dict(),
            "unique_counts": data.nunique().to_dict()
        }
        
        if name not in self.states:
            self.states[name] = []
        
        self.states[name].append(state)
        return state
    
    def detect_changes(self, name: str) -> Dict[str, Any]:
        """
        Detect changes in data state.
        
        Args:
            name: Name of the data
            
        Returns:
            Dict[str, Any]: Change information
        """
        if name not in self.states or len(self.states[name]) < 2:
            return {"error": "Insufficient state history"}
        
        current = self.states[name][-1]
        previous = self.states[name][-2]
        
        changes = {
            "timestamp": current["timestamp"],
            "name": name,
            "shape_changed": current["shape"] != previous["shape"],
            "columns": {
                "added": list(set(current["columns"]) - set(previous["columns"])),
                "removed": list(set(previous["columns"]) - set(current["columns"]))
            },
            "dtype_changes": {},
            "null_changes": {},
            "unique_changes": {}
        }
        
        # Check for dtype changes
        for col in set(current["columns"]) & set(previous["columns"]):
            if current["dtypes"][col] != previous["dtypes"][col]:
                changes["dtype_changes"][col] = {
                    "from": previous["dtypes"][col],
                    "to": current["dtypes"][col]
                }
        
        # Check for null count changes
        for col in set(current["columns"]) & set(previous["columns"]):
            if current["null_counts"][col] != previous["null_counts"][col]:
                changes["null_changes"][col] = {
                    "from": previous["null_counts"][col],
                    "to": current["null_counts"][col],
                    "difference": current["null_counts"][col] - previous["null_counts"][col]
                }
        
        # Check for unique value changes
        for col in set(current["columns"]) & set(previous["columns"]):
            if current["unique_counts"][col] != previous["unique_counts"][col]:
                changes["unique_changes"][col] = {
                    "from": previous["unique_counts"][col],
                    "to": current["unique_counts"][col],
                    "difference": current["unique_counts"][col] - previous["unique_counts"][col]
                }
        
        return changes
    
    def get_state_history(self, name: str) -> List[Dict[str, Any]]:
        """
        Get the history of states for a data set.
        
        Args:
            name: Name of the data
            
        Returns:
            List[Dict[str, Any]]: List of states
        """
        return self.states.get(name, [])
    
    def get_summary(self, name: str) -> Dict[str, Any]:
        """
        Get a summary of the monitored data.
        
        Args:
            name: Name of the data
            
        Returns:
            Dict[str, Any]: Summary information
        """
        if name not in self.states:
            return {"error": "No state history available"}
        
        states = self.states[name]
        current = states[-1]
        
        summary = {
            "name": name,
            "current_timestamp": current["timestamp"],
            "total_states": len(states),
            "shape": current["shape"],
            "columns": len(current["columns"]),
            "null_columns": [
                col for col, count in current["null_counts"].items()
                if count > 0
            ],
            "unique_columns": [
                col for col, count in current["unique_counts"].items()
                if count == 1
            ]
        }
        
        return summary 