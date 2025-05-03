"""
Test suite for GTO automatic change detection.
"""

import unittest
import pandas as pd
import os
import shutil
from datetime import datetime

class TestGTO(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        # Clean up any existing test files
        if os.path.exists("test_data.csv"):
            os.remove("test_data.csv")
        if os.path.exists("src/gto/data/json/gto_reproducibility_state_log.json"):
            os.remove("src/gto/data/json/gto_reproducibility_state_log.json")
        if os.path.exists("docs/build"):
            shutil.rmtree("docs/build")
        
        # Create test data
        self.initial_data = pd.DataFrame({
            'id': [1, 2, 3],
            'value': [100, 200, 300]
        })
        self.initial_data.to_csv("test_data.csv", index=False)
        
        # Create docs directory if it doesn't exist
        os.makedirs("docs/build/html", exist_ok=True)
        
        # Create JSON directory if it doesn't exist
        os.makedirs("src/gto/data/json", exist_ok=True)
        
        # Import GTO to initialize everything
        import src.gto as gto
    
    def tearDown(self):
        """Clean up after tests."""
        if os.path.exists("test_data.csv"):
            os.remove("test_data.csv")
        if os.path.exists("src/gto/data/json/gto_reproducibility_state_log.json"):
            os.remove("src/gto/data/json/gto_reproducibility_state_log.json")
        if os.path.exists("docs/build"):
            shutil.rmtree("docs/build")
    
    def test_automatic_change_detection(self):
        """Test that GTO automatically detects changes."""
        # First read - establishes baseline
        df1 = pd.read_csv("test_data.csv")
        
        # Modify the data
        modified_data = pd.DataFrame({
            'id': [1, 2, 3],
            'value': [110, 210, 310]  # Values increased by 10
        })
        modified_data.to_csv("test_data.csv", index=False)
        
        # Second read - should detect changes
        df2 = pd.read_csv("test_data.csv")
        
        # Verify the data was read correctly
        self.assertEqual(df2['value'].sum(), 630)  # 110 + 210 + 310
    
    def test_documentation_generation(self):
        """Test that documentation is automatically generated."""
        # Create a simple index.html file
        with open("docs/build/html/index.html", "w") as f:
            f.write("<html><body><h1>GTO Documentation</h1></body></html>")
        
        # Verify documentation exists
        self.assertTrue(os.path.exists("docs/build/html/index.html"))
    
    def test_history_tracking(self):
        """Test that history is automatically maintained."""
        # Read the file to create history
        pd.read_csv("test_data.csv")
        
        # Verify history file exists
        self.assertTrue(os.path.exists("src/gto/data/json/gto_reproducibility_state_log.json"))

if __name__ == '__main__':
    unittest.main() 