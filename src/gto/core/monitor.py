"""
Data monitoring and change detection.

This module provides:
- File monitoring
- Change detection
- Hash generation
- Change logging
"""

import os
import hashlib
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path
import json

def calculate_file_hash(file_path: str, algorithm: str = "sha256") -> str:
    """
    Calculate hash of a file.
    
    Args:
        file_path: Path to file
        algorithm: Hash algorithm to use
        
    Returns:
        str: File hash
    """
    hash_obj = hashlib.new(algorithm)
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hash_obj.update(chunk)
    return hash_obj.hexdigest()

def monitor_file(file_path: str, config: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Monitor a file for changes.
    
    Args:
        file_path: Path to file
        config: Configuration dictionary
        
    Returns:
        Optional[Dict[str, Any]]: Change information if file changed
    """
    if not os.path.exists(file_path):
        return None
        
    current_hash = calculate_file_hash(file_path, config["hash_algorithm"])
    last_hash = get_last_hash(file_path, config)
    
    if current_hash != last_hash:
        change_info = {
            "file_path": file_path,
            "timestamp": datetime.now().isoformat(),
            "old_hash": last_hash,
            "new_hash": current_hash,
            "size": os.path.getsize(file_path)
        }
        log_change(change_info, config)
        return change_info
    
    return None

def get_last_hash(file_path: str, config: Dict[str, Any]) -> Optional[str]:
    """
    Get last known hash of a file.
    
    Args:
        file_path: Path to file
        config: Configuration dictionary
        
    Returns:
        Optional[str]: Last known hash or None
    """
    history_file = Path(config["log_dir"]) / "file_history.json"
    if not history_file.exists():
        return None
        
    with open(history_file, 'r') as f:
        history = json.load(f)
    return history.get(file_path, {}).get("hash")

def log_change(change_info: Dict[str, Any], config: Dict[str, Any]) -> None:
    """
    Log file change information.
    
    Args:
        change_info: Change information dictionary
        config: Configuration dictionary
    """
    log_file = Path(config["log_dir"]) / "changes.log"
    with open(log_file, 'a') as f:
        f.write(f"{json.dumps(change_info)}\n")
        
    # Update history
    history_file = Path(config["log_dir"]) / "file_history.json"
    if history_file.exists():
        with open(history_file, 'r') as f:
            history = json.load(f)
    else:
        history = {}
        
    history[change_info["file_path"]] = {
        "hash": change_info["new_hash"],
        "last_modified": change_info["timestamp"]
    }
    
    with open(history_file, 'w') as f:
        json.dump(history, f, indent=4) 