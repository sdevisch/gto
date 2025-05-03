"""
Run GTO tests using pytest.
"""

import pytest
import sys
import os

if __name__ == "__main__":
    # Add the project root to the Python path
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    
    # Run tests with verbose output
    pytest.main(['-v', 'tests/']) 