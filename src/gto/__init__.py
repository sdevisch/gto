"""
GTO (Git-based Tracking of Data Changes) - A comprehensive data trust system.

This package provides tools for:
- Data change tracking and monitoring
- Translation and transformation
- Benchmarking and performance analysis
- Data boosting and enhancement
- Data tracking and versioning
- Data reconciliation and validation

Modules:
- core: Core functionality and utilities
- translate: Data translation and transformation (coming soon)
- benchmark: Performance benchmarking and analysis (coming soon)
- boost: Data enhancement and optimization (coming soon)
- track: Data tracking and versioning (coming soon)
- recon: Data reconciliation and validation (coming soon)
- utils: Common utilities and helpers (coming soon)
"""

from .core import *
from .core.hash_utils import summarize_dataframe, create_fingerprint, save_history

__version__ = '0.1.0'
__author__ = 'Data Governance Team'

import os
import sys
import pandas as pd
from datetime import datetime
from .core.config import setup_config

# Set up configuration
config = setup_config()

# Initialize required directories
for dir_name in [config["data_dir"], config["log_dir"], config["docs_dir"]]:
    os.makedirs(dir_name, exist_ok=True)

# Set up CSV monitoring
def monitor_csv_reading(filepath, *args, **kwargs):
    """Monitor CSV file reading and track changes."""
    # Read the file
    df = pd._read_csv(filepath, *args, **kwargs)
    
    # Generate summary and fingerprint
    summary = summarize_dataframe(df)
    fingerprint = create_fingerprint(summary)
    
    # Save to history
    history = {
        filepath: {
            'fingerprint': fingerprint,
            'summary': summary,
            'timestamp': datetime.now().isoformat()
        }
    }
    save_history(history)
    
    return df

# Replace pandas read_csv with monitored version
pd._read_csv = pd.read_csv
pd.read_csv = monitor_csv_reading

print("GTO initialized - Data change tracking is now active!")
print("Documentation available at: docs/build/html/index.html") 