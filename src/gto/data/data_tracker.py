"""
Data Change Tracking System

This module provides functionality for:
1. Recording data state changes
2. Computing data fingerprints
3. Maintaining change history
4. Enabling collaborative tracking

The system ensures data modifications are tracked, logged, and shared
across team members while maintaining a complete audit trail.
"""

import hashlib
import json
import os
from datetime import datetime
import pandas as pd
from git import Repo

# Configuration and state files
HISTORY_LOG_PATH = "gto_reproducibility_state_log.json"
SHARED_STATE_PATH = "simulated_shared_repo.json"

def initialize_configuration():
    """
    Initialize or load system configuration.
    
    Creates default configuration if none exists, otherwise loads existing.
    Returns dict with configuration parameters.
    """
    CONFIG_FILE = "config.json"
    
    if not os.path.exists(CONFIG_FILE):
        default_config = {
            "distributed_mode": False,
            "repository_url": "https://github.com/your_org/shared_state_repo.git"
        }
        with open(CONFIG_FILE, "w") as f:
            json.dump(default_config, f, indent=2)
    
    with open(CONFIG_FILE) as f:
        return json.load(f)

def load_state_history():
    """
    Load the recorded history of data states.
    
    Returns:
        dict: Mapping of file paths to their recorded states
              Empty dict if no history exists
    """
    if os.path.exists(HISTORY_LOG_PATH):
        with open(HISTORY_LOG_PATH, "r") as f:
            return json.load(f)
    return {}

def update_state_history(history):
    """
    Update the persistent record of data states.
    
    Args:
        history (dict): Current state history to persist
    """
    with open(HISTORY_LOG_PATH, "w") as f:
        json.dump(history, f, indent=2)

def compute_data_summary(df):
    """
    Generate a summary of dataframe contents.
    
    Creates a compact representation capturing:
    - Row count
    - Column-wise numeric summaries
    
    Args:
        df (pd.DataFrame): Input dataframe to summarize
        
    Returns:
        dict: Summary statistics of the dataframe
    """
    return {
        "rows": len(df),
        "numeric_sums": df.select_dtypes('number').sum().to_dict()
    }

def generate_fingerprint(summary):
    """
    Generate cryptographic hash of data summary.
    
    Uses SHA256 for:
    - Fixed length output
    - Collision resistance
    - Deterministic results
    
    Args:
        summary (dict): Data summary to fingerprint
        
    Returns:
        str: Hexadecimal representation of SHA256 hash
    """
    serialized = json.dumps(summary, sort_keys=True)
    return hashlib.sha256(serialized.encode()).hexdigest()

def distribute_state(filepath, state_data, config):
    """
    Share data state information with team.
    
    Args:
        filepath (str): Path of tracked file
        state_data (dict): Current state data including fingerprint and summary
        config (dict): System configuration
    """
    if config["distributed_mode"]:
        _sync_distributed_state(filepath, state_data, config)
    else:
        _update_local_state(filepath, state_data)

def _sync_distributed_state(filepath, state_data, config):
    """
    Synchronize state through distributed version control.
    
    Args:
        filepath (str): Path of tracked file
        state_data (dict): Current state data
        config (dict): System configuration
    """
    REPO_PATH = os.path.expanduser("~/.gto_shared_state")
    
    if not os.path.exists(REPO_PATH):
        Repo.clone_from(config["repository_url"], REPO_PATH)
    repo = Repo(REPO_PATH)
    
    state_file = os.path.join(REPO_PATH, "shared_state.json")
    shared_state = {}
    if os.path.exists(state_file):
        with open(state_file) as f:
            shared_state = json.load(f)
    
    shared_state[filepath] = {
        **state_data,
        "timestamp": datetime.now().isoformat()
    }
    
    with open(state_file, "w") as f:
        json.dump(shared_state, f, indent=2)
    
    repo.index.add(["shared_state.json"])
    repo.index.commit(f"Update state for {filepath}")
    repo.remote().push()

def _update_local_state(filepath, state_data):
    """
    Update local state record.
    
    Args:
        filepath (str): Path of tracked file
        state_data (dict): Current state data
    """
    if not os.path.exists(SHARED_STATE_PATH):
        with open(SHARED_STATE_PATH, "w") as f:
            json.dump({}, f)
    
    with open(SHARED_STATE_PATH, "r+") as f:
        try:
            shared_state = json.load(f)
        except json.JSONDecodeError:
            shared_state = {}
        
        shared_state[filepath] = {
            **state_data,
            "timestamp": datetime.now().isoformat()
        }
        
        f.seek(0)
        json.dump(shared_state, f, indent=2)
        f.truncate()

def report_state_change(filepath, previous_state, new_summary):
    """
    Generate technical report of detected changes.
    
    Args:
        filepath (str): Path of modified file
        previous_state (dict): Previous recorded state
        new_summary (dict): Current state summary
    """
    print(f"\n[State Change Detection] Changes detected in '{filepath}':")
    previous_summary = previous_state.get("summary", {})
    
    # Compare row counts
    if previous_summary.get("rows", 0) != new_summary["rows"]:
        print(f"- Rows: {previous_summary.get('rows', 0)} -> {new_summary['rows']}")
    
    # Compare numeric sums
    prev_sums = previous_summary.get("numeric_sums", {})
    new_sums = new_summary["numeric_sums"]
    
    for col in set(prev_sums.keys()) | set(new_sums.keys()):
        prev_val = prev_sums.get(col, 0)
        new_val = new_sums.get(col, 0)
        if prev_val != new_val:
            print(f"- Sum of {col}: {prev_val} -> {new_val}")
    
    print(f"Timestamp: {datetime.now().isoformat()}\n") 