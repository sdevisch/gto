"""
Configuration management for GTO.

This module handles:
- Loading and saving configuration
- Setting up default settings
- Managing configuration paths
- Validating configuration
"""

import os
import json
from pathlib import Path
from typing import Dict, Any

# Default configuration
DEFAULT_CONFIG = {
    "data_dir": "data",
    "log_dir": "logs",
    "docs_dir": "docs",
    "hash_algorithm": "sha256",
    "monitor_files": [".csv", ".json", ".txt"],
    "auto_document": True,
    "verbose": False
}

def setup_config(config_path: str = None) -> dict:
    """
    Set up GTO configuration.
    
    Args:
        config_path: Optional path to configuration file
        
    Returns:
        dict: Configuration dictionary
    """
    if config_path and os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
    else:
        config = DEFAULT_CONFIG.copy()
    
    # Ensure required directories exist
    for dir_key in ["data_dir", "log_dir", "docs_dir"]:
        Path(config[dir_key]).mkdir(parents=True, exist_ok=True)
    
    return config

def save_config(config: dict, config_path: str) -> None:
    """
    Save configuration to file.
    
    Args:
        config: Configuration dictionary
        config_path: Path to save configuration
    """
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=4)

def validate_config(config: dict) -> bool:
    """
    Validate configuration dictionary.
    
    Args:
        config: Configuration dictionary to validate
        
    Returns:
        bool: True if configuration is valid
    """
    required_keys = ["data_dir", "log_dir", "docs_dir", "hash_algorithm"]
    return all(key in config for key in required_keys)

def load_config(config_path: str = "config.json") -> Dict[str, Any]:
    """
    Load configuration from a JSON file.
    
    Args:
        config_path: Path to the configuration file
        
    Returns:
        Dict[str, Any]: Configuration dictionary
    """
    try:
        with open(config_path) as f:
            return json.load(f)
    except FileNotFoundError:
        return get_default_config()

def get_default_config() -> Dict[str, Any]:
    """
    Get default configuration.
    
    Returns:
        Dict[str, Any]: Default configuration dictionary
    """
    return {
        "data_dir": "data",
        "tracking_enabled": True,
        "benchmarking": {
            "enabled": True,
            "frameworks": ["pandas", "pyspark", "dask"]
        }
    } 