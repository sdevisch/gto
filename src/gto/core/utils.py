"""
Utility functions and helpers.

This module provides:
- File operations
- Path handling
- Logging
- Error handling
- Type checking
"""

import os
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import json

def setup_logging(log_dir: str, level: int = logging.INFO) -> None:
    """
    Set up logging configuration.
    
    Args:
        log_dir: Directory for log files
        level: Logging level
    """
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    
    log_file = Path(log_dir) / f"gto_{datetime.now().strftime('%Y%m%d')}.log"
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

def ensure_dir(path: Union[str, Path]) -> Path:
    """
    Ensure directory exists.
    
    Args:
        path: Directory path
        
    Returns:
        Path: Path object for directory
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path

def get_file_extension(file_path: Union[str, Path]) -> str:
    """
    Get file extension.
    
    Args:
        file_path: Path to file
        
    Returns:
        str: File extension
    """
    return Path(file_path).suffix.lower()

def is_valid_file(file_path: Union[str, Path], allowed_extensions: List[str]) -> bool:
    """
    Check if file is valid.
    
    Args:
        file_path: Path to file
        allowed_extensions: List of allowed extensions
        
    Returns:
        bool: True if file is valid
    """
    return get_file_extension(file_path) in allowed_extensions

def format_timestamp(timestamp: Optional[str] = None) -> str:
    """
    Format timestamp.
    
    Args:
        timestamp: Optional timestamp string
        
    Returns:
        str: Formatted timestamp
    """
    if timestamp is None:
        timestamp = datetime.now().isoformat()
    return timestamp

def safe_json_load(file_path: Union[str, Path]) -> Dict[str, Any]:
    """
    Safely load JSON file.
    
    Args:
        file_path: Path to JSON file
        
    Returns:
        Dict[str, Any]: JSON data
    """
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {} 