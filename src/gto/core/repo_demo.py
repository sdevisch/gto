"""
Demonstration of GTO Data Change Tracking System with Repository Reconciliation

This script demonstrates:
1. Local change detection by reloading the same file
2. Two repositories with different data states that need reconciliation
"""

import os
import pandas as pd
import json
import shutil
from datetime import datetime
from .main import monitor_csv_reading
from .hash_utils import load_history, create_fingerprint, summarize_dataframe

def cleanup_old_outputs():
    """Remove old demonstration outputs and temporary files."""
    print("\n[Cleanup] Removing old demonstration outputs...")
    
    # List of directories and files to clean up
    cleanup_targets = [
        "demo_output",           # Previous demo output
        "repo_demo_output",      # Current demo output
        "docs/build",           # Generated documentation
        "test_data.csv",        # Temporary test file
        "demo_data.csv",        # Temporary demo file
        "gto_reproducibility_state_log.json"  # State log
    ]
    
    for target in cleanup_targets:
        if os.path.exists(target):
            if os.path.isdir(target):
                shutil.rmtree(target)
                print(f"Removed directory: {target}")
            else:
                os.remove(target)
                print(f"Removed file: {target}")
    
    print("Cleanup complete!")

def create_test_data():
    """Create initial test data."""
    return pd.DataFrame({
        'id': [1, 2, 3, 4, 5, 6],
        'value': [100, 200, 300, 400, 500, 600]
    })

def save_repo_state(data, repo_name, version, output_dir):
    """Save repository state with tracking information."""
    # Create repo directory
    repo_dir = os.path.join(output_dir, repo_name)
    os.makedirs(repo_dir, exist_ok=True)
    
    # Create version directory
    version_dir = os.path.join(repo_dir, f"version_{version}")
    os.makedirs(version_dir, exist_ok=True)
    
    # Save data
    data_path = os.path.join(version_dir, "data.csv")
    data.to_csv(data_path, index=False)
    
    # Save tracking information
    summary = summarize_dataframe(data)
    fingerprint = create_fingerprint(summary)
    
    tracking_info = {
        "fingerprint": fingerprint,
        "summary": summary,
        "timestamp": datetime.now().isoformat()
    }
    
    tracking_path = os.path.join(version_dir, "tracking.json")
    with open(tracking_path, 'w') as f:
        json.dump(tracking_info, f, indent=2)
    
    return tracking_info

def format_summary(summary):
    """Format a data summary into a readable string."""
    return f"rows: {summary['row_count']}, sum of values: {summary['numeric_sums']['value']}, squared sum: {summary['squared_sums']['value']:.2f}"

def run_demonstration():
    """Run the complete demonstration."""
    # Clean up old outputs first
    cleanup_old_outputs()
    
    # Create output directory
    output_dir = "repo_demo_output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Create summary file
    summary = {
        "title": "GTO Repository Change Tracking Demonstration",
        "start_time": datetime.now().isoformat(),
        "repositories": {
            "local": [],
            "repo_a": [],
            "repo_b": []
        }
    }
    
    print("\n=== GTO Data Change Tracking Demonstration ===")
    print("\nPart 1: Local Change Detection")
    print("--------------------------------")
    
    # Initial data setup
    data = create_test_data()
    data.to_csv("test_data.csv", index=False)
    
    # Initial load
    print("\n[Initial State]")
    print("At this time, we have created a test dataset with 6 records.")
    print("Each record has an ID and a value. The values are: 100, 200, 300, 400, 500, 600")
    monitor_csv_reading("test_data.csv")
    local_v1 = save_repo_state(data, "local", 1, output_dir)
    summary["repositories"]["local"].append(local_v1)
    print(f"Initial state summary: {format_summary(local_v1['summary'])}")
    
    # Modify data and reload
    print("\n[Data Change Detected]")
    print("At this time, we have modified the source data.")
    print("Each value has been increased by 10:")
    print("Before: 100, 200, 300, 400, 500, 600")
    print("After:  110, 210, 310, 410, 510, 610")
    data['value'] = [110, 210, 310, 410, 510, 610]
    data.to_csv("test_data.csv", index=False)
    monitor_csv_reading("test_data.csv")
    local_v2 = save_repo_state(data, "local", 2, output_dir)
    summary["repositories"]["local"].append(local_v2)
    print(f"New state summary: {format_summary(local_v2['summary'])}")
    
    print("\nPart 2: Repository Reconciliation")
    print("--------------------------------")
    
    # Repository A: Initial state
    print("\n[Repository A - Initial State]")
    print("Repository A has loaded the original data:")
    repo_a_data = create_test_data()
    repo_a_v1 = save_repo_state(repo_a_data, "repo_a", 1, output_dir)
    summary["repositories"]["repo_a"].append(repo_a_v1)
    print(f"Repository A state: {format_summary(repo_a_v1['summary'])}")
    
    # Repository B: Modified state
    print("\n[Repository B - Initial State]")
    print("Repository B has loaded the modified data:")
    repo_b_data = create_test_data()
    repo_b_data['value'] = [110, 210, 310, 410, 510, 610]
    repo_b_v1 = save_repo_state(repo_b_data, "repo_b", 1, output_dir)
    summary["repositories"]["repo_b"].append(repo_b_v1)
    print(f"Repository B state: {format_summary(repo_b_v1['summary'])}")
    
    # Repository A: Rebase to match B
    print("\n[Repository Reconciliation]")
    print("The system has detected a difference between repositories:")
    print(f"Repository A sum: {repo_a_v1['summary']['numeric_sums']['value']}")
    print(f"Repository B sum: {repo_b_v1['summary']['numeric_sums']['value']}")
    print("\nRepository A needs to update its data to match Repository B.")
    print("This is because Repository B has the more recent version of the data.")
    
    # Repository A: After rebase
    print("\n[Repository A - After Update]")
    repo_a_data['value'] = [110, 210, 310, 410, 510, 610]
    repo_a_v2 = save_repo_state(repo_a_data, "repo_a", 2, output_dir)
    summary["repositories"]["repo_a"].append(repo_a_v2)
    print(f"Repository A has been updated to: {format_summary(repo_a_v2['summary'])}")
    print("The repositories are now in sync!")
    
    # Save summary
    with open(os.path.join(output_dir, "summary.json"), 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\nDemonstration complete! Check {output_dir} for detailed results.")
    print("Each repository contains:")
    print("- data.csv: The data at each version")
    print("- tracking.json: Change tracking information")
    print("\nsummary.json provides an overview of all repository states.")

if __name__ == "__main__":
    run_demonstration() 