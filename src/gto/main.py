"""
GTO Main Module

This module provides the main entry point for the GTO package.
It handles initialization, configuration, and high-level operations.

Example:
    >>> from gto import GTO
    >>> gto = GTO()
    >>> gto.track_data("data.csv")
"""

from typing import Dict, Any, Optional
from pathlib import Path
import pandas as pd

from .core.config import load_config
from .data.reader import DataReader
from .data.history import DataHistory
from .reporting.data_storyteller import DataStoryteller
from .core.dependencies import install_dependencies
from .docs.generator import generate_documentation

class GTO:
    """Main GTO class for tracking data changes."""
    
    def __init__(self, config_path: str = "config.json") -> None:
        """
        Initialize GTO with configuration.
        
        Args:
            config_path: Path to configuration file
        """
        self.config: Dict[str, Any] = load_config(config_path)
        self.reader: DataReader = DataReader(config_path)
        self.history: DataHistory = DataHistory()
        self.storyteller: DataStoryteller = DataStoryteller()
    
    def track_data(self, file_path: str) -> Dict[str, Any]:
        """
        Track changes in a data file.
        
        Args:
            file_path: Path to the data file
            
        Returns:
            Dict[str, Any]: Change report containing either the change history or an error message
        """
        data = self.reader.read_file(file_path)
        if self.reader.validate_data(data):
            self.history.track_change(file_path, "modified", {"size": len(data)})
            return self.storyteller.generate_report(self.history.get_history(file_path))
        return {"error": "Invalid data"}

def demonstrate_functionality() -> None:
    """
    Show how the system works with a simple example.
    
    This function creates a sample dataset, modifies it, and shows how GTO tracks the changes.
    It also demonstrates the documentation generation capability.
    """
    # Ensure dependencies are installed
    install_dependencies()
    
    # Create test data
    df = pd.DataFrame({
        "id": [1, 2, 3],
        "value": [100, 200, 300]
    })
    test_file = Path("test_data.csv")
    df.to_csv(test_file, index=False)
    
    try:
        # Initialize GTO
        gto = GTO()
        
        # First read establishes baseline
        print("\n[Initial Data Load]")
        print(pd.read_csv(test_file))
        result = gto.track_data(str(test_file))
        print("Initial tracking result:", result)
        
        # Modify data
        df = pd.DataFrame({
            "id": [1, 2, 3],
            "value": [110, 210, 310]  # Values increased by 10
        })
        df.to_csv(test_file, index=False)
        
        # Second read shows changes
        print("\n[Data Reload After Changes]")
        print(pd.read_csv(test_file))
        result = gto.track_data(str(test_file))
        print("Change tracking result:", result)
        
        # Generate documentation
        generate_documentation()
    finally:
        # Clean up test file
        if test_file.exists():
            test_file.unlink()

if __name__ == "__main__":
    demonstrate_functionality() 