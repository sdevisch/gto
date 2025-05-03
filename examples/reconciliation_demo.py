"""
Simple demonstration of data reconciliation using hashing.

This example shows how to:
1. Detect changes in data using hashing
2. Identify what changed
3. Reconcile differences between two versions
"""

import hashlib
import json
from typing import Dict, Any, Tuple
from dataclasses import dataclass
from datetime import datetime

@dataclass
class DataVersion:
    """Represents a version of data with its hash and timestamp."""
    data: Dict[str, Any]
    hash: str
    timestamp: datetime

def hash_data(data: Dict[str, Any]) -> str:
    """
    Generate a hash for the data.
    
    Args:
        data: Dictionary containing the data to hash
        
    Returns:
        str: SHA-256 hash of the data
    """
    # Convert data to a consistent string representation
    data_str = json.dumps(data, sort_keys=True)
    return hashlib.sha256(data_str.encode()).hexdigest()

def create_version(data: Dict[str, Any]) -> DataVersion:
    """
    Create a new version of data with its hash.
    
    Args:
        data: Dictionary containing the data
        
    Returns:
        DataVersion: Version object with data, hash, and timestamp
    """
    return DataVersion(
        data=data,
        hash=hash_data(data),
        timestamp=datetime.now()
    )

def find_differences(old: Dict[str, Any], new: Dict[str, Any]) -> Tuple[set, set, set]:
    """
    Find differences between two versions of data.
    
    Args:
        old: Old version of the data
        new: New version of the data
        
    Returns:
        Tuple containing:
        - set of added keys
        - set of removed keys
        - set of modified keys
    """
    old_keys = set(old.keys())
    new_keys = set(new.keys())
    
    added = new_keys - old_keys
    removed = old_keys - new_keys
    
    # Find modified keys (present in both but with different values)
    common_keys = old_keys & new_keys
    modified = {
        key for key in common_keys
        if old[key] != new[key]
    }
    
    return added, removed, modified

def demonstrate_reconciliation() -> None:
    """Demonstrate the reconciliation process with a simple example."""
    print("\n=== Data Reconciliation Demo ===\n")
    
    # Initial data
    initial_data = {
        "user_id": 123,
        "name": "John Doe",
        "email": "john@example.com",
        "age": 30
    }
    
    # Create initial version
    initial_version = create_version(initial_data)
    print("Initial version created:")
    print(f"Hash: {initial_version.hash}")
    print(f"Data: {json.dumps(initial_version.data, indent=2)}\n")
    
    # Modified data (simulating changes)
    modified_data = {
        "user_id": 123,
        "name": "John Doe",
        "email": "john.doe@example.com",  # Changed
        "age": 31,                        # Changed
        "phone": "+1234567890"            # Added
    }
    
    # Create new version
    new_version = create_version(modified_data)
    print("New version created:")
    print(f"Hash: {new_version.hash}")
    print(f"Data: {json.dumps(new_version.data, indent=2)}\n")
    
    # Check if data changed
    if initial_version.hash != new_version.hash:
        print("Data has changed! Let's find out what changed...\n")
        
        # Find differences
        added, removed, modified = find_differences(
            initial_version.data,
            new_version.data
        )
        
        # Report changes
        if added:
            print(f"Added fields: {added}")
        if removed:
            print(f"Removed fields: {removed}")
        if modified:
            print(f"Modified fields: {modified}")
            
        print("\nDetailed changes:")
        for field in modified:
            print(f"\n{field}:")
            print(f"  Old value: {initial_version.data[field]}")
            print(f"  New value: {new_version.data[field]}")
    else:
        print("No changes detected!")

if __name__ == "__main__":
    demonstrate_reconciliation() 