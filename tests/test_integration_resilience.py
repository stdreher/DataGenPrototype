import unittest
import pandas as pd
import json
import os
import datetime
from database_utils import get_dataset_by_id, get_all_saved_datasets
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, JSON

class TestIntegrationResilience(unittest.TestCase):
    """Integration tests for database resilience with real sample data"""
    
    def setUp(self):
        """Create a temporary test database for integration testing"""
        # Use an in-memory SQLite database for testing
        self.test_db_url = "sqlite:///:memory:"
        self.original_db_url = os.environ.get("DATABASE_URL")
        
        # Temporarily override the DATABASE_URL
        os.environ["DATABASE_URL"] = self.test_db_url
        
        # Create necessary tables in the test database
        self.engine = create_engine(self.test_db_url)
        self.metadata = MetaData()
        
        # Define tables similar to those in database_utils.py
        self.saved_datasets = Table(
            "saved_datasets",
            self.metadata,
            Column("id", Integer, primary_key=True),
            Column("name", String, nullable=False),
            Column("description", String),
            Column("num_records", Integer, nullable=False),
            Column("locale", String, nullable=False),
            Column("fields", JSON, nullable=False),
            Column("field_config", JSON, nullable=False),
            Column("created_at", String, nullable=False),
        )
        
        # Create tables in the test database
        self.metadata.create_all(self.engine)
    
    def tearDown(self):
        """Clean up after tests"""
        # Restore the original DATABASE_URL
        if self.original_db_url:
            os.environ["DATABASE_URL"] = self.original_db_url
        else:
            del os.environ["DATABASE_URL"]
        
        # Close the database connection
        self.engine.dispose()
    
    def test_sample_datasets_when_database_empty(self):
        """Test that sample datasets are returned when the database is empty"""
        # The database is empty, so get_all_saved_datasets should return sample data
        results = get_all_saved_datasets()
        
        # Check that results are not empty
        self.assertIsNotNone(results)
        self.assertIsInstance(results, pd.DataFrame)
        self.assertFalse(results.empty)
        
        # Verify we get the sample datasets (should have ids 1, 2, 3)
        self.assertEqual(len(results), 3)
        self.assertTrue(all(id_val in results['id'].values for id_val in [1, 2, 3]))
        
        # Check specific dataset details
        e_commerce = results[results['id'] == 1].iloc[0]
        self.assertEqual(e_commerce['name'], "E-Commerce Kundendaten")
        self.assertIn("username", e_commerce['fields'])
        
        health_data = results[results['id'] == 2].iloc[0]
        self.assertEqual(health_data['name'], "Pseudonymisierte Patientendaten")
        self.assertIn("date_of_birth", health_data['fields'])
    
    def test_get_dataset_by_id_resilience(self):
        """Test get_dataset_by_id resilience with sample data"""
        # Get a dataset that doesn't exist in the database
        # This should return a sample dataset since we're using IDs 1-3
        dataset = get_dataset_by_id(1)
        
        # Verify we get the correct sample dataset
        self.assertIsNotNone(dataset)
        self.assertEqual(dataset['id'], 1)
        self.assertEqual(dataset['name'], "E-Commerce Kundendaten")
        self.assertIn("credit_card", dataset['fields'])
        
        # Try with another sample ID
        dataset2 = get_dataset_by_id(2)
        self.assertIsNotNone(dataset2)
        self.assertEqual(dataset2['name'], "Pseudonymisierte Patientendaten")
        
        # Try with a non-existent ID
        non_existent = get_dataset_by_id(999)
        self.assertIsNone(non_existent)

    def test_integration_with_custom_sample_data(self):
        """Test integration of sample showcase data with custom test dataset"""
        # Create custom test dataset definition matching our sample showcases
        custom_test_data = {
            "id": 1,
            "name": "E-Commerce Test Data",
            "description": "Integration test data for E-Commerce showcase",
            "fields": ["username", "email", "full_name", "credit_card"],
            "field_config": {
                "username": {"prefix": "test_", "suffix": ""},
                "email": {"domain": "test.com"}
            },
            "locale": "de_DE",
            "num_records": 50,
            "created_at": datetime.datetime.now().strftime("%Y-%m-%d")
        }
        
        # Check that we can get this dataset by ID (using our fallback mechanism)
        dataset_id = 1
        result = get_dataset_by_id(dataset_id)
        
        # Verify we got the right dataset
        self.assertIsNotNone(result)
        self.assertEqual(result['id'], dataset_id)
        
        # Confirm the sample dataset contains expected fields
        self.assertTrue(isinstance(result['fields'], list))
        for field in ["username", "email"]:
            self.assertIn(field, result['fields'])
        
        # Verify field configuration
        self.assertTrue(isinstance(result['field_config'], dict))
        self.assertIn("username", result['field_config'])

if __name__ == "__main__":
    unittest.main()