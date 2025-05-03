"""
Change Tracking Module

This module provides tools for tracking and analyzing data changes.
"""

from typing import Dict, Any, List
import pandas as pd
import numpy as np
from datetime import datetime

class ChangeTracker:
    """Tracks and analyzes data changes."""
    
    def __init__(self):
        """Initialize the change tracker."""
        self.changes = {}
    
    def track_change(self, data: pd.DataFrame, name: str) -> Dict[str, Any]:
        """
        Track changes in the data.
        
        Args:
            data: Current data state
            name: Name of the data
            
        Returns:
            Dict[str, Any]: Change information
        """
        current_state = {
            "timestamp": datetime.now().isoformat(),
            "shape": data.shape,
            "columns": list(data.columns),
            "dtypes": data.dtypes.to_dict(),
            "summary": data.describe().to_dict()
        }
        
        if name in self.changes:
            previous_state = self.changes[name]
            changes = self._analyze_changes(previous_state, current_state)
        else:
            changes = {"initial_state": current_state}
        
        self.changes[name] = current_state
        return changes
    
    def _analyze_changes(self, previous: Dict[str, Any], current: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze changes between two states.
        
        Args:
            previous: Previous state
            current: Current state
            
        Returns:
            Dict[str, Any]: Change analysis
        """
        changes = {
            "timestamp": current["timestamp"],
            "shape_changed": previous["shape"] != current["shape"],
            "columns_added": set(current["columns"]) - set(previous["columns"]),
            "columns_removed": set(previous["columns"]) - set(current["columns"]),
            "dtype_changes": {},
            "summary_changes": {}
        }
        
        # Analyze dtype changes
        for col in set(previous["dtypes"].keys()) & set(current["dtypes"].keys()):
            if previous["dtypes"][col] != current["dtypes"][col]:
                changes["dtype_changes"][col] = {
                    "from": previous["dtypes"][col],
                    "to": current["dtypes"][col]
                }
        
        # Analyze summary changes
        for col in set(previous["summary"].keys()) & set(current["summary"].keys()):
            if previous["summary"][col] != current["summary"][col]:
                changes["summary_changes"][col] = {
                    "from": previous["summary"][col],
                    "to": current["summary"][col]
                }
        
        return changes 