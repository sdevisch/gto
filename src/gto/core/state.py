"""
State management and persistence.

This module provides:
- State loading and saving
- State synchronization
- State validation
- State history
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

def load_state(state_file: str) -> Dict[str, Any]:
    """
    Load state from file.
    
    Args:
        state_file: Path to state file
        
    Returns:
        Dict[str, Any]: State dictionary
    """
    if os.path.exists(state_file):
        with open(state_file, 'r') as f:
            return json.load(f)
    return {}

def save_state(state: Dict[str, Any], state_file: str) -> None:
    """
    Save state to file.
    
    Args:
        state: State dictionary
        state_file: Path to state file
    """
    with open(state_file, 'w') as f:
        json.dump(state, f, indent=4)

def update_state(state: Dict[str, Any], key: str, value: Any) -> Dict[str, Any]:
    """
    Update state with new value.
    
    Args:
        state: Current state dictionary
        key: Key to update
        value: New value
        
    Returns:
        Dict[str, Any]: Updated state
    """
    state[key] = value
    state["last_updated"] = datetime.now().isoformat()
    return state

def validate_state(state: Dict[str, Any]) -> bool:
    """
    Validate state dictionary.
    
    Args:
        state: State dictionary to validate
        
    Returns:
        bool: True if state is valid
    """
    required_keys = ["version", "last_updated"]
    return all(key in state for key in required_keys)

def get_state_history(state_file: str) -> Optional[Dict[str, Any]]:
    """
    Get state history.
    
    Args:
        state_file: Path to state file
        
    Returns:
        Optional[Dict[str, Any]]: State history or None
    """
    history_file = Path(state_file).with_suffix('.history.json')
    if history_file.exists():
        with open(history_file, 'r') as f:
            return json.load(f)
    return None

def save_state_history(state: Dict[str, Any], state_file: str) -> None:
    """
    Save state history.
    
    Args:
        state: Current state
        state_file: Path to state file
    """
    history_file = Path(state_file).with_suffix('.history.json')
    history = get_state_history(state_file) or {}
    
    timestamp = datetime.now().isoformat()
    history[timestamp] = state
    
    with open(history_file, 'w') as f:
        json.dump(history, f, indent=4) 