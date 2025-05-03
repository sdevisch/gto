"""
Change detection and reporting.

This module handles detecting and reporting changes between data states.
"""

from typing import Dict, Any
from .narrative import generate_change_narrative

def report_changes(filepath: str, previous: Dict[str, Any], current: Dict[str, Any]) -> None:
    """
    Generate and display a report of changes between data states.
    
    Args:
        filepath: Path to the data file
        previous: Previous data state summary
        current: Current data state summary
    """
    changes = detect_changes(previous["summary"], current)
    narrative = generate_change_narrative(filepath, changes)
    print(narrative)

def detect_changes(previous: Dict[str, Any], current: Dict[str, Any]) -> Dict[str, Any]:
    """
    Detect changes between two data states.
    
    Args:
        previous: Previous data state summary
        current: Current data state summary
    
    Returns:
        Dict describing the changes found
    """
    changes = {
        "structure_changes": [],
        "value_changes": [],
        "type_changes": []
    }
    
    # Check for column changes
    prev_cols = set(previous["columns"])
    curr_cols = set(current["columns"])
    
    added = curr_cols - prev_cols
    removed = prev_cols - curr_cols
    
    if added:
        changes["structure_changes"].append(f"Added columns: {added}")
    if removed:
        changes["structure_changes"].append(f"Removed columns: {removed}")
        
    # Check for type changes
    for col in prev_cols & curr_cols:
        if previous["dtypes"][col] != current["dtypes"][col]:
            changes["type_changes"].append(
                f"Column '{col}' type changed from {previous['dtypes'][col]} to {current['dtypes'][col]}"
            )
    
    return changes 