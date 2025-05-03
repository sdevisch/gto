"""
Test suite for GTO hash utilities.
"""

import unittest
import pandas as pd
import os
from datetime import datetime
from src.gto.core.hash_utils import (
    summarize_dataframe,
    create_fingerprint,
    setup_config,
    load_history,
    save_history,
    share_fingerprint
)

class TestDataChangeTracking(unittest.TestCase):
    def setUp(self):
        """Set up test environment."""
        self.sample_data = pd.DataFrame({
            'id': [1, 2, 3],
            'value': [100, 200, 300]
        })
    
    def test_data_summarization(self):
        """Verify that data summaries capture essential information."""
        summary = summarize_dataframe(self.sample_data)
        
        # Check summary structure
        self.assertIsInstance(summary, dict)
        self.assertEqual(summary['row_count'], 3)
        self.assertEqual(summary['numeric_sums']['value'], 600)
        self.assertEqual(summary['column_stats']['value']['squared_sum'], 140000)
    
    def test_fingerprint_generation(self):
        """Verify that fingerprints are unique and consistent."""
        # Create test data
        data = {'key': 'value'}
        
        # Generate fingerprints
        fingerprint1 = create_fingerprint(data)
        fingerprint2 = create_fingerprint(data)
        
        # Verify fingerprint properties
        self.assertIsInstance(fingerprint1, str)
        self.assertEqual(fingerprint1, fingerprint2)  # Same input should give same output
    
    def test_configuration_management(self):
        """Verify that configuration is properly managed."""
        config = setup_config()
        self.assertIsInstance(config, dict)
        self.assertIn('use_git', config)
    
    def test_history_management(self):
        """Verify that history is properly maintained."""
        # Create test history
        history = {'test.csv': {
            'fingerprint': 'test',
            'summary': {'row_count': 1},
            'timestamp': datetime.now().isoformat()
        }}
        
        # Save and load history
        save_history(history)
        loaded_history = load_history()
        
        self.assertEqual(history, loaded_history)
    
    def test_local_fingerprint_sharing(self):
        """Verify that fingerprints can be shared locally."""
        fingerprint = 'test_fingerprint'
        filepath = 'test.csv'
        config = setup_config()
        
        # Share fingerprint
        share_fingerprint(filepath, fingerprint, config)
        
        # Verify fingerprint was shared
        self.assertTrue(os.path.exists('src/gto/data/json/gto_reproducibility_state_log.json'))
    
    def test_change_reporting(self):
        """Verify that changes are properly reported."""
        # Create initial data
        initial_data = pd.DataFrame({
            'id': [1, 2, 3],
            'value': [100, 200, 300]
        })
        
        # Create modified data
        modified_data = pd.DataFrame({
            'id': [1, 2, 3],
            'value': [110, 210, 310]
        })
        
        # Get summaries
        initial_summary = summarize_dataframe(initial_data)
        modified_summary = summarize_dataframe(modified_data)
        
        # Verify changes are detected
        self.assertNotEqual(initial_summary['numeric_sums']['value'], 
                          modified_summary['numeric_sums']['value'])

if __name__ == '__main__':
    unittest.main() 