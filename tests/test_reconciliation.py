"""
Tests for the data reconciliation demonstration.
"""

import pytest
from examples.reconciliation_demo import (
    hash_data,
    create_version,
    find_differences,
    DataVersion
)

def test_hash_data_consistency() -> None:
    """Test that the same data always produces the same hash."""
    data = {"key": "value"}
    hash1 = hash_data(data)
    hash2 = hash_data(data)
    assert hash1 == hash2

def test_hash_data_different() -> None:
    """Test that different data produces different hashes."""
    data1 = {"key": "value1"}
    data2 = {"key": "value2"}
    assert hash_data(data1) != hash_data(data2)

def test_create_version() -> None:
    """Test version creation."""
    data = {"key": "value"}
    version = create_version(data)
    assert isinstance(version, DataVersion)
    assert version.data == data
    assert version.hash == hash_data(data)

def test_find_differences() -> None:
    """Test difference detection."""
    old = {
        "unchanged": "same",
        "modified": "old",
        "removed": "value"
    }
    new = {
        "unchanged": "same",
        "modified": "new",
        "added": "value"
    }
    
    added, removed, modified = find_differences(old, new)
    
    assert added == {"added"}
    assert removed == {"removed"}
    assert modified == {"modified"}

def test_find_differences_no_changes() -> None:
    """Test difference detection with no changes."""
    data = {"key": "value"}
    added, removed, modified = find_differences(data, data)
    
    assert not added
    assert not removed
    assert not modified 