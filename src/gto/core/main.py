"""
GTO Core Module

This module provides core functionality for the GTO package.
It handles essential operations and utilities.

Example:
    >>> from gto.core import Core
    >>> core = Core()
    >>> core.initialize()
"""

import pandas as pd
import subprocess
import sys
import webbrowser
import os
from datetime import datetime
from functools import wraps
from typing import Dict, Any
from pathlib import Path
from .config import load_config

# Import our tracking utilities with more intuitive names
from .hash_utils import (
    setup_config,
    summarize_dataframe,
    create_fingerprint,
    load_history,
    save_history,
    share_fingerprint,
    report_changes
)

def install_dependencies():
    """
    Ensure all required packages are installed.
    
    We need:
    - pandas: For data handling
    - gitpython: For distributed change tracking
    - sphinx: For documentation generation
    """
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "pandas", "gitpython", "sphinx"],
        check=True
    )

# Install dependencies first
install_dependencies()

# Load user configuration
config = setup_config()

# Store the original pandas read_csv function
original_read_csv = pd.read_csv

def monitor_csv_reading(filepath, *args, **kwargs):
    """
    Enhanced version of pandas.read_csv that tracks data changes.
    
    This function:
    1. Reads the CSV file normally
    2. Creates a summary of its contents
    3. Checks if the data changed since last read
    4. Reports any changes found
    5. Updates the change history
    """
    # Store the original data
    df = original_read_csv(filepath, *args, **kwargs)
    
    # Create a summary of the current data state
    current_summary = summarize_dataframe(df)
    current_fingerprint = create_fingerprint(current_summary)
    
    # Check if we've seen this file before
    history = load_history()
    previous_version = history.get(filepath)
    
    # If we have a previous version and it's different, report changes
    if previous_version and previous_version["fingerprint"] != current_fingerprint:
        report_changes(previous_version["summary"], current_summary, previous_version["timestamp"])
    
    # Update our records
    history[filepath] = {
        "fingerprint": current_fingerprint,
        "summary": current_summary,
        "timestamp": datetime.now().isoformat()
    }
    save_history(history)
    
    # Share the new fingerprint with others
    share_fingerprint(filepath, current_fingerprint, config)
    
    return df

# Replace pandas read_csv with our monitored version
pd.read_csv = monitor_csv_reading

def generate_documentation():
    """
    Generate beautiful HTML documentation for this system.
    
    The documentation includes:
    - System overview
    - API reference
    - Usage examples
    - Configuration guide
    """
    if not os.path.exists("docs"):
        # Create initial documentation structure
        subprocess.run([
            sys.executable, "-m", "sphinx.cmd.quickstart", "docs",
            "-q",  # Quiet mode
            "-p", "GTO_Reproducibility",
            "-a", "Data Governance Team",
            "--sep",  # Separate source and build
            "--makefile"  # Generate Makefile
        ], check=True)
    
    # Generate API documentation
    subprocess.run([sys.executable, "-m", "sphinx.ext.apidoc", "-o", "docs/source", "."], check=True)
    
    # Build HTML documentation
    subprocess.run([sys.executable, "-m", "sphinx.cmd.build", "docs/source", "docs/build/html"], check=True)
    
    # Open in browser for immediate viewing
    webbrowser.open_new_tab(os.path.abspath("docs/build/html/index.html"))

def demonstrate_functionality():
    """
    Show how the system works with a simple example.
    
    This demonstration:
    1. Creates a sample dataset
    2. Reads it once to establish baseline
    3. Modifies the data
    4. Reads it again to show change detection
    5. Generates documentation
    """
    filepath = "test_data.csv"
    
    # Create initial test data if it doesn't exist
    if not os.path.exists(filepath):
        pd.DataFrame({
            "id": [1, 2, 3],
            "value": [100, 200, 300]
        }).to_csv(filepath, index=False)
    
    # First read - establishes baseline
    print("\n[Initial Data Load]")
    print(pd.read_csv(filepath))
    
    # Modify the data to simulate changes
    pd.DataFrame({
        "id": [1, 2, 3],
        "value": [110, 210, 310]  # Values increased by 10
    }).to_csv(filepath, index=False)
    
    # Second read - should detect and report changes
    print("\n[Data Reload After Simulated Change]")
    print(pd.read_csv(filepath))
    
    # Generate documentation
    generate_documentation()

if __name__ == "__main__":
    demonstrate_functionality()

def report_changes(old_summary, new_summary, timestamp):
    """Generate a narrative report of changes between two data states."""
    print("\n=== Data Change Report ===")
    print(f"Time: {timestamp}")
    print("\nWhat changed:")
    
    # Compare row counts
    old_rows = old_summary['row_count']
    new_rows = new_summary['row_count']
    if old_rows != new_rows:
        print(f"\nThe number of records has changed from {old_rows} to {new_rows}.")
    
    # Compare numeric columns
    for col in old_summary['numeric_sums'].keys():
        old_stats = old_summary['column_stats'][col]
        new_stats = new_summary['column_stats'][col]
        
        if old_stats != new_stats:
            print(f"\nIn column '{col}':")
            
            # Report mean changes
            old_mean = old_stats['mean']
            new_mean = new_stats['mean']
            if old_mean != new_mean:
                print(f"- The average value changed from {old_mean:.2f} to {new_mean:.2f}")
            
            # Report sum changes
            old_sum = old_stats['sum']
            new_sum = new_stats['sum']
            if old_sum != new_sum:
                print(f"- The total sum changed from {old_sum:.2f} to {new_sum:.2f}")
                print(f"  This is a change of {new_sum - old_sum:+.2f}")
            
            # Report squared sum changes
            old_squared = old_stats['squared_sum']
            new_squared = new_stats['squared_sum']
            if old_squared != new_squared:
                print(f"- The squared sum changed from {old_squared:.2f} to {new_squared:.2f}")
                print(f"  This is a change of {new_squared - old_squared:+.2f}")
            
            # Report distribution changes
            old_std = old_stats['std']
            new_std = new_stats['std']
            if old_std != new_std:
                print(f"- The spread of values (standard deviation) changed from {old_std:.2f} to {new_std:.2f}")
    
    print("\nEnd of Change Report")
    print("=" * 20)

class Core:
    """Core GTO functionality."""
    
    def __init__(self, config_path: str = "config.json"):
        """
        Initialize core functionality.
        
        Args:
            config_path: Path to configuration file
        """
        self.config = load_config(config_path)
    
    def initialize(self) -> Dict[str, Any]:
        """
        Initialize GTO core components.
        
        Returns:
            Dict[str, Any]: Initialization status
        """
        return {"status": "initialized", "config": self.config}
