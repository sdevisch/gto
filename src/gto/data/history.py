"""
Data history tracking module.

This module provides:
- Data change history management
- Version tracking
- Change logging
"""

import json
import os
from typing import Dict, Any, List
from pathlib import Path
from datetime import datetime
from ..core.config import load_config

def ensure_directory_exists(filepath: str) -> None:
    """Ensure the directory for a file exists."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

def load_history() -> Dict[str, Any]:
    """
    Load the data state history from disk.
    
    Returns:
        Dict mapping filenames to their state history
    """
    config = load_config()
    history_file = config["history_file"]
    
    if os.path.exists(history_file):
        with open(history_file, 'r') as f:
            return json.load(f)
    return {}

def save_history(history: Dict[str, Any]) -> None:
    """
    Save the data state history to disk.
    
    Args:
        history: Dict mapping filenames to their state history
    """
    config = load_config()
    history_file = config["history_file"]
    
    ensure_directory_exists(history_file)
    with open(history_file, 'w') as f:
        json.dump(history, f, indent=4)

def share_state(filepath: str, fingerprint: str) -> None:
    """
    Share data state with other users (if enabled).
    
    Args:
        filepath: Path to the data file
        fingerprint: Current state fingerprint
    """
    config = load_config()
    if not config["enable_sharing"]:
        return
        
    shared_file = config["shared_state_file"]
    shared_state = {}
    
    if os.path.exists(shared_file):
        with open(shared_file, 'r') as f:
            shared_state = json.load(f)
    
    shared_state[filepath] = fingerprint
    
    ensure_directory_exists(shared_file)
    with open(shared_file, 'w') as f:
        json.dump(shared_state, f, indent=4)

class DataHistory:
    """Manages data change history."""
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialize data history tracker.
        
        Args:
            data_dir: Directory containing data files
        """
        self.data_dir = Path(data_dir)
        self.history: Dict[str, List[Dict[str, Any]]] = {}
    
    def track_change(self, file_path: str, change_type: str, details: Dict[str, Any]) -> None:
        """
        Track a data change.
        
        Args:
            file_path: Path to the changed file
            change_type: Type of change (e.g., 'modified', 'deleted')
            details: Change details
        """
        if file_path not in self.history:
            self.history[file_path] = []
        
        self.history[file_path].append({
            "timestamp": datetime.now().isoformat(),
            "type": change_type,
            "details": details
        })
    
    def get_history(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Get change history for a file.
        
        Args:
            file_path: Path to the file
            
        Returns:
            List[Dict[str, Any]]: List of changes
        """
        return self.history.get(file_path, []) 