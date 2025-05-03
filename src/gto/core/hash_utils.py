"""
Data Change Tracking Utilities

This module helps track changes in data files by:
1. Computing summaries of data content
2. Generating unique fingerprints (hashes) of those summaries
3. Storing the history of changes
4. Reporting when data has been modified

The goal is to make data changes transparent and traceable, helping
maintain data integrity and compliance.
"""

import hashlib
import json
import os
from datetime import datetime
import pandas as pd
from git import Repo
from pathlib import Path
from typing import Dict, Any, Optional

# Constants
HISTORY_FILE = Path('src/gto/data/json/gto_reproducibility_state_log.json')
LOCAL_REPO = os.path.join("src", "gto", "data", "json", "simulated_shared_repo.json")
CONFIG_FILE = os.path.join("src", "gto", "config", "config.json")

def setup_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Set up configuration with defaults.
    
    Args:
        config_path: Optional path to config file
        
    Returns:
        Dict[str, Any]: Configuration dictionary
    """
    default_config = {
        'use_git': False,
        'data_dir': 'data',
        'log_dir': 'logs',
        'docs_dir': 'docs'
    }
    
    if config_path and os.path.exists(config_path):
        with open(config_path) as f:
            user_config = json.load(f)
            default_config.update(user_config)
    
    return default_config

def load_history() -> Dict[str, Any]:
    """
    Load history from file.
    
    Returns:
        Dict[str, Any]: History dictionary
    """
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE) as f:
            return json.load(f)
    return {}

def save_history(history: Dict[str, Any]) -> None:
    """
    Save history to file.
    
    Args:
        history: History dictionary
    """
    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=4)

def summarize_dataframe(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Create a summary of DataFrame contents.
    
    Args:
        df: DataFrame to summarize
        
    Returns:
        Dict[str, Any]: Summary dictionary
    """
    summary = {
        'row_count': len(df),
        'column_stats': {},
        'numeric_sums': {}
    }
    
    for column in df.columns:
        if pd.api.types.is_numeric_dtype(df[column]):
            values = df[column].dropna()
            summary['numeric_sums'][column] = float(values.sum())
            summary['column_stats'][column] = {
                'mean': float(values.mean()),
                'std': float(values.std()),
                'squared_sum': float((values ** 2).sum())
            }
        else:
            summary['column_stats'][column] = {
                'unique_count': len(df[column].unique()),
                'most_common': df[column].mode().iloc[0] if not df[column].empty else None
            }
    
    return summary

def create_fingerprint(data: Dict[str, Any]) -> str:
    """
    Create a unique fingerprint for data.
    
    Args:
        data: Data to fingerprint
        
    Returns:
        str: Data fingerprint
    """
    json_str = json.dumps(data, sort_keys=True)
    return hashlib.sha256(json_str.encode()).hexdigest()

def detect_changes(old_fingerprint, new_fingerprint):
    """
    Detect and explain changes between two data fingerprints.
    
    Args:
        old_fingerprint (str): Previous fingerprint
        new_fingerprint (str): Current fingerprint
        
    Returns:
        str: A human-readable explanation of the changes
    """
    if not old_fingerprint or not new_fingerprint:
        return "Cannot detect changes: missing fingerprint data"
    
    # Parse the fingerprints
    old_lines = old_fingerprint.split('\n')
    new_lines = new_fingerprint.split('\n')
    
    # Extract key metrics
    old_metrics = {}
    new_metrics = {}
    
    for line in old_lines:
        if ':' in line:
            key, value = line.split(':', 1)
            old_metrics[key.strip()] = value.strip()
    
    for line in new_lines:
        if ':' in line:
            key, value = line.split(':', 1)
            new_metrics[key.strip()] = value.strip()
    
    # Generate change explanation
    changes = []
    timestamp = datetime.now().isoformat()
    
    # Check row count changes
    old_rows = int(old_metrics.get('Total rows', 0))
    new_rows = int(new_metrics.get('Total rows', 0))
    
    if old_rows != new_rows or any(old_metrics.get(k) != new_metrics.get(k) for k in old_metrics):
        changes.append(f"A change in the data source was detected at {timestamp}.")
        
        # Check squared sum changes
        for key in old_metrics:
            if key.startswith('Column') and 'Squared Sum' in key:
                col_name = key.split("'")[1]
                old_squared_sum = float(old_metrics[key].split(':')[1].strip())
                new_squared_sum = float(new_metrics.get(key, '0').split(':')[1].strip())
                
                if old_squared_sum != new_squared_sum:
                    changes.append(f"\nBefore this change, the squared sum function returned {old_squared_sum:.2f} for column '{col_name}'.")
                    changes.append(f"After the change, the squared sum function returned {new_squared_sum:.2f}.")
                    
                    # Get count and sum information
                    count_key = f"Column '{col_name}' Count"
                    sum_key = f"Column '{col_name}' Sum"
                    old_count = int(old_metrics.get(count_key, '0').split(':')[1].strip())
                    new_count = int(new_metrics.get(count_key, '0').split(':')[1].strip())
                    old_sum = float(old_metrics.get(sum_key, '0').split(':')[1].strip())
                    new_sum = float(new_metrics.get(sum_key, '0').split(':')[1].strip())
                    
                    changes.append(f"\nThe data source used to have a count of {old_count} and sum of {old_sum:.2f} for column '{col_name}'.")
                    changes.append(f"Now, the count is {new_count} and sum is {new_sum:.2f}.")
                    changes.append(f"This explains the change of squared sum from {old_squared_sum:.2f} to {new_squared_sum:.2f}.")
    
    if not changes:
        return "No significant changes detected in the data."
    
    return "\n".join(changes)

def share_fingerprint(filepath: str, fingerprint: str, config: Dict[str, Any]) -> None:
    """
    Share fingerprint locally or via Git.
    
    Args:
        filepath: Path to file
        fingerprint: File fingerprint
        config: Configuration dictionary
    """
    history = load_history()
    history[filepath] = {
        'fingerprint': fingerprint,
        'timestamp': datetime.now().isoformat()
    }
    save_history(history)

def report_changes(filepath, old_version, new_summary):
    """
    Generate a human-readable report of what changed in the data.
    
    Shows:
    - Which file changed
    - What the specific changes were
    - When the change was detected
    """
    print(f"\n[Data Change Report] Changes detected in '{filepath}':")
    old_summary = old_version["summary"]
    
    # Compare each aspect of the summaries
    for key in old_summary:
        if old_summary[key] != new_summary[key]:
            print(f"- {key}: {old_summary[key]} -> {new_summary[key]}")
    
    print(f"Timestamp: {datetime.now().isoformat()}\n") 