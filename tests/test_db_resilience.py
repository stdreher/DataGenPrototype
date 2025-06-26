import unittest
import pandas as pd
import json
from database_utils import get_dataset_by_id, get_all_saved_datasets

class TestDatabaseResilience(unittest.TestCase):
    """Test database resilience with existing and sample data"""
    
    def test_get_dataset_by_id_with_sample_data(self):
        """Test that get_dataset_by_id returns sample data for specified IDs"""
        # Test that we can retrieve sample datasets with IDs 1-3 when needed
        dataset_1 = get_dataset_by_id(1)
        if dataset_1:
            # If dataset with ID 1 exists in real DB, just check it's valid
            self.assertIsNotNone(dataset_1)
            self.assertEqual(dataset_1['id'], 1)
            self.assertIsInstance(dataset_1['fields'], list)
            self.assertIsInstance(dataset_1['field_config'], dict)
        
        # Test invalid ID returns None
        dataset_999 = get_dataset_by_id(999)
        self.assertIsNone(dataset_999)
    
    def test_get_all_saved_datasets_returns_data(self):
        """Test that get_all_saved_datasets returns valid data"""
        datasets_df = get_all_saved_datasets()
        
        # Check that we get a DataFrame
        self.assertIsInstance(datasets_df, pd.DataFrame)
        
        # Check that it's not empty
        self.assertFalse(datasets_df.empty)
        
        # Verify structure (all records should have these columns)
        required_columns = ['id', 'name', 'description', 'fields', 'field_config', 'locale']
        for col in required_columns:
            self.assertIn(col, datasets_df.columns)
        
        # Confirm first row has valid values
        first_row = datasets_df.iloc[0]
        self.assertIsNotNone(first_row['id'])
        self.assertIsNotNone(first_row['name'])
        self.assertIsInstance(first_row['fields'], list)

if __name__ == "__main__":
    unittest.main()