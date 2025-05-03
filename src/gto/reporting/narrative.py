"""
Human-readable report generation.

This module converts technical change information into clear,
human-readable narratives.
"""

from typing import Dict, Any

def generate_change_narrative(filepath: str, changes: Dict[str, Any]) -> str:
    """
    Generate a human-readable narrative of data changes.
    
    Args:
        filepath: Path to the data file
        changes: Dict describing the changes found
    
    Returns:
        str: Human-readable narrative
    """
    lines = [
        f"\nChanges detected in {filepath}:",
        "-" * 40
    ]
    
    if not any(changes.values()):
        lines.append("No significant changes detected.")
        return "\n".join(lines)
    
    if changes["structure_changes"]:
        lines.append("\nStructural Changes:")
        lines.extend(f"  - {change}" for change in changes["structure_changes"])
    
    if changes["type_changes"]:
        lines.append("\nData Type Changes:")
        lines.extend(f"  - {change}" for change in changes["type_changes"])
    
    if changes["value_changes"]:
        lines.append("\nValue Changes:")
        lines.extend(f"  - {change}" for change in changes["value_changes"])
    
    return "\n".join(lines) 