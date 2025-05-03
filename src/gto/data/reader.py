"""
Data file reading module.

This module provides functionality for:
- Reading data files in various formats (CSV, JSON, Parquet)
- Automatic format detection
- Data validation and error handling
"""

from pathlib import Path
from typing import Any, Dict, Union, Optional
import pandas as pd
from pandas import DataFrame

from ..core.config import load_config
from ..core.exceptions import DataReadError, ValidationError

class DataReader:
    """
    Handles data file reading and validation.
    
    This class provides a unified interface for reading data files in various formats
    and ensures the data meets basic validation requirements.
    
    Attributes:
        config (Dict[str, Any]): Configuration settings for the reader
        supported_formats (set[str]): Set of supported file extensions
    """
    
    def __init__(self, config_path: str = "config.json") -> None:
        """
        Initialize data reader.
        
        Args:
            config_path: Path to configuration file
            
        Raises:
            FileNotFoundError: If config file doesn't exist
            ValueError: If config file is invalid
        """
        self.config: Dict[str, Any] = load_config(config_path)
        self.supported_formats: set[str] = {'.csv', '.json', '.parquet'}
    
    def read_file(
        self,
        file_path: Union[str, Path],
        **kwargs: Any
    ) -> DataFrame:
        """
        Read a data file into a pandas DataFrame.
        
        Args:
            file_path: Path to the file
            **kwargs: Additional arguments passed to the underlying pandas reader
            
        Returns:
            DataFrame: Loaded data as a pandas DataFrame
            
        Raises:
            DataReadError: If file cannot be read or format is unsupported
            ValidationError: If data validation fails after reading
        """
        path = Path(file_path)
        
        if not path.exists():
            raise DataReadError(f"File not found: {path}")
            
        if path.suffix not in self.supported_formats:
            raise DataReadError(f"Unsupported file format: {path.suffix}")
        
        try:
            if path.suffix == '.csv':
                data = pd.read_csv(path, **kwargs)
            elif path.suffix == '.json':
                data = pd.read_json(path, **kwargs)
            elif path.suffix == '.parquet':
                data = pd.read_parquet(path, **kwargs)
            else:
                raise DataReadError(f"Unsupported file format: {path.suffix}")
                
            if not self.validate_data(data):
                raise ValidationError("Data validation failed after reading")
                
            return data
            
        except Exception as e:
            raise DataReadError(f"Error reading file {path}: {str(e)}") from e
    
    def validate_data(self, data: Any) -> bool:
        """
        Validate data structure and content.
        
        Args:
            data: Data to validate, expected to be a pandas DataFrame
            
        Returns:
            bool: True if data is valid according to configured rules
            
        Note:
            Current validation rules:
            - Must be a non-empty DataFrame
            - Must have at least one row and column
        """
        if not isinstance(data, DataFrame):
            return False
            
        return not (
            data.empty or
            len(data.columns) == 0 or
            len(data.index) == 0
        ) 