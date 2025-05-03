"""
Data fingerprinting utilities.

This module provides functions to create unique fingerprints of data states
and summarize DataFrame contents.
"""

import hashlib
import json
import pandas as pd
from typing import Dict, Any

def summarize_dataframe(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Create a summary of a DataFrame's contents.
    
    Args:
        df: The DataFrame to summarize
    
    Returns:
        Dict containing summary statistics
    """
    return {
        "shape": df.shape,
        "columns": list(df.columns),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "summary": df.describe().to_dict()
    }

def create_fingerprint(data: Dict[str, Any]) -> str:
    """
    Create a unique fingerprint for a data state.
    
    Args:
        data: Dictionary of data to fingerprint
    
    Returns:
        str: SHA-256 hash of the data
    """
    serialized = json.dumps(data, sort_keys=True)
    return hashlib.sha256(serialized.encode()).hexdigest() 