"""
Version Control Module

This module provides tools for tracking and managing data versions.
"""

from typing import Dict, Any, List
import hashlib
import json
from datetime import datetime

class VersionTracker:
    """Tracks and manages data versions."""
    
    def __init__(self):
        """Initialize the version tracker."""
        self.versions = {}
    
    def create_version(self, data: Any) -> str:
        """
        Create a new version of the data.
        
        Args:
            data: The data to version
            
        Returns:
            str: Version identifier
        """
        version_id = hashlib.sha256(str(data).encode()).hexdigest()
        self.versions[version_id] = {
            "timestamp": datetime.now().isoformat(),
            "data": data
        }
        return version_id
    
    def get_version(self, version_id: str) -> Dict[str, Any]:
        """
        Get a specific version of the data.
        
        Args:
            version_id: The version identifier
            
        Returns:
            Dict[str, Any]: Version information
        """
        return self.versions.get(version_id)
    
    def list_versions(self) -> List[str]:
        """
        List all available versions.
        
        Returns:
            List[str]: List of version identifiers
        """
        return list(self.versions.keys()) 