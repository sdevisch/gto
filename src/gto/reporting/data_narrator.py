"""
Data Narrator Module

This module provides tools for generating narrative reports about data changes.
It works in conjunction with the data_storyteller module to provide different
perspectives on data changes.
"""

from typing import Dict, Any, List
from datetime import datetime

class DataNarrator:
    """Generates narrative reports about data changes."""
    
    def __init__(self):
        """Initialize the data narrator."""
        self.templates = {
            "change": "The data in {file} was {change_type} on {timestamp}.",
            "insight": "Key insight: {insight}",
            "summary": "Summary: {summary}"
        }
    
    def generate_report(self, changes: List[Dict[str, Any]]) -> str:
        """
        Generate a narrative report from changes.
        
        Args:
            changes: List of changes to report
            
        Returns:
            str: Narrative report
        """
        report = []
        for change in changes:
            report.append(self._format_change(change))
        
        if report:
            return "\n".join(report)
        return "No changes detected."
    
    def _format_change(self, change: Dict[str, Any]) -> str:
        """
        Format a single change into narrative.
        
        Args:
            change: Change details
            
        Returns:
            str: Formatted narrative
        """
        return self.templates["change"].format(
            file=change.get("file", "unknown"),
            change_type=change.get("type", "modified"),
            timestamp=change.get("timestamp", datetime.now().isoformat())
        ) 