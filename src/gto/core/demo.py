"""
Demonstration of GTO Data Change Tracking System

This script creates a series of data changes and tracks them,
saving the results in an organized output structure.
"""

import os
import pandas as pd
import json
from datetime import datetime
from .main import monitor_csv_reading
from .hash_utils import load_history

def create_demo_data():
    """Create initial demo data."""
    return pd.DataFrame({
        'id': [1, 2, 3],
        'value': [100, 200, 300]
    })

def save_state(data, version, output_dir):
    """Save current state of data and tracking information."""
    # Create version directory
    version_dir = os.path.join(output_dir, f"version_{version}")
    os.makedirs(version_dir, exist_ok=True)
    
    # Save data
    data_path = os.path.join(version_dir, "data.csv")
    data.to_csv(data_path, index=False)
    
    # Save tracking information
    history = load_history()
    tracking_path = os.path.join(version_dir, "tracking.json")
    with open(tracking_path, 'w') as f:
        json.dump(history, f, indent=2)
    
    # Save metadata
    metadata = {
        "version": version,
        "timestamp": datetime.now().isoformat(),
        "data_path": data_path,
        "tracking_path": tracking_path
    }
    with open(os.path.join(version_dir, "metadata.json"), 'w') as f:
        json.dump(metadata, f, indent=2)
    
    return metadata

def run_demonstration():
    """Run the complete demonstration."""
    # Create output directory
    output_dir = "demo_output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Create summary file
    summary = {
        "title": "GTO Data Change Tracking Demonstration",
        "start_time": datetime.now().isoformat(),
        "versions": []
    }
    
    # Version 1: Initial data
    data = create_demo_data()
    data.to_csv("demo_data.csv", index=False)
    monitor_csv_reading("demo_data.csv")  # Establish baseline
    v1_meta = save_state(data, 1, output_dir)
    summary["versions"].append(v1_meta)
    
    # Version 2: First change
    data['value'] = [110, 210, 310]  # Increase all values by 10
    data.to_csv("demo_data.csv", index=False)
    monitor_csv_reading("demo_data.csv")
    v2_meta = save_state(data, 2, output_dir)
    summary["versions"].append(v2_meta)
    
    # Version 3: Second change
    data['value'] = [120, 220, 320]  # Increase all values by 10 again
    data.to_csv("demo_data.csv", index=False)
    monitor_csv_reading("demo_data.csv")
    v3_meta = save_state(data, 3, output_dir)
    summary["versions"].append(v3_meta)
    
    # Save summary
    with open(os.path.join(output_dir, "summary.json"), 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\nDemonstration complete! Check {output_dir} for results.")
    print("Each version contains:")
    print("- data.csv: The data at that point")
    print("- tracking.json: Change tracking information")
    print("- metadata.json: Version metadata")
    print("\nsummary.json provides an overview of all versions.")

if __name__ == "__main__":
    run_demonstration() 