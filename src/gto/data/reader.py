"""
Data file reading module.

This module provides:
- Data file reading
- Format detection
- Data validation
"""

import pandas as pd
from pathlib import Path
from typing import Any, Dict, Union
from ..core.config import load_config

class DataReader:
    """Handles data file reading and validation."""
    
    def __init__(self, config_path: str = "config.json"):
        """
        Initialize data reader.
        
        Args:
            config_path: Path to configuration file
        """
        self.config = load_config(config_path)
    
    def read_file(self, file_path: str, **kwargs) -> Union[pd.DataFrame, Dict[str, Any]]:
        """
        Read a data file.
        
        Args:
            file_path: Path to the file
            **kwargs: Additional arguments for the reader
            
        Returns:
            Union[pd.DataFrame, Dict[str, Any]]: Loaded data
        """
        path = Path(file_path)
        if path.suffix == '.csv':
            return pd.read_csv(file_path, **kwargs)
        elif path.suffix == '.json':
            return pd.read_json(file_path, **kwargs)
        elif path.suffix == '.parquet':
            return pd.read_parquet(file_path, **kwargs)
        else:
            raise ValueError(f"Unsupported file format: {path.suffix}")
    
    def validate_data(self, data: Any) -> bool:
        """
        Validate data structure.
        
        Args:
            data: Data to validate
            
        Returns:
            bool: True if valid
        """
        if isinstance(data, pd.DataFrame):
            return not data.empty
        elif isinstance(data, dict):
            return bool(data)
        return False 