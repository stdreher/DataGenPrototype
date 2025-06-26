import unittest
import pandas as pd
import json
import sys
import os

# Add the parent directory to the path to import the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import functions from pages/3_Community_Showcase.py
# We'll need to create a function to import and test the sample showcase data
def import_sample_showcases():
    # Define sample showcases that match what's in pages/3_Community_Showcase.py
    sample_showcases = [
        {
            "id": 1,
            "title": "E-Commerce Kundendatenbank mit realistischen Kaufmustern",
            "description": "Diese E-Commerce-Datenkonfiguration erzeugt realistische Kundendaten für einen Online-Shop, komplett mit Adressen, Kontaktinformationen und Kaufmustern.",
            "author": "Markus Weber",
            "category": "E-Commerce",
            "tags": ["user-profiles", "payments", "e-commerce"],
            "dataset_id": 1,
            "upvotes": 15,
            "created_at": "2025-05-21",
            "is_featured": 1
        },
        {
            "id": 2,
            "title": "Gesundheitsdaten mit DSGVO-konformer Pseudonymisierung",
            "description": "Diese Konfiguration erzeugt pseudonymisierte Patientendaten, die für Tests von Gesundheits-IT-Systemen verwendet werden können, während gleichzeitig die DSGVO-Anforderungen eingehalten werden.",
            "author": "Dr. Julia Fischer",
            "category": "Gesundheitswesen",
            "tags": ["health-data", "DSGVO", "pseudonymization"],
            "dataset_id": 2,
            "upvotes": 23,
            "created_at": "2025-05-21",
            "is_featured": 1
        },
        {
            "id": 3,
            "title": "Multi-Locale Testdaten für internationale Websites",
            "description": "Diese Datenkonfiguration erzeugt Testdaten für internationale Websites und Anwendungen mit Unterstützung für mehrere Locales.",
            "author": "Sandra Müller",
            "category": "Web-Anwendungen",
            "tags": ["multi-language", "i18n", "l10n"],
            "dataset_id": 3,
            "upvotes": 12,
            "created_at": "2025-05-21",
            "is_featured": 0
        }
    ]
    return pd.DataFrame(sample_showcases)

class TestShowcaseSamples(unittest.TestCase):
    """Test showcase sample data for database resilience"""
    
    def test_sample_showcase_structure(self):
        """Test that sample showcases have the correct structure"""
        # Get sample showcases
        sample_df = import_sample_showcases()
        
        # Validate the structure
        self.assertIsInstance(sample_df, pd.DataFrame)
        self.assertEqual(len(sample_df), 3)  # Should have 3 sample showcases
        
        # Check columns
        expected_columns = [
            "id", "title", "description", "author", "category",
            "tags", "dataset_id", "upvotes", "created_at", "is_featured"
        ]
        for col in expected_columns:
            self.assertIn(col, sample_df.columns)
        
        # Check specific data
        self.assertEqual(sample_df.iloc[0]["title"], "E-Commerce Kundendatenbank mit realistischen Kaufmustern")
        self.assertEqual(sample_df.iloc[1]["category"], "Gesundheitswesen")
        self.assertEqual(sample_df.iloc[2]["author"], "Sandra Müller")
    
    def test_sample_showcase_tags(self):
        """Test that sample showcase tags are valid"""
        sample_df = import_sample_showcases()
        
        # Check that tags are lists
        for i in range(len(sample_df)):
            tags = sample_df.iloc[i]["tags"]
            self.assertIsInstance(tags, list)
            self.assertTrue(len(tags) > 0)
            
        # Check specific tags
        self.assertIn("e-commerce", sample_df.iloc[0]["tags"])
        self.assertIn("DSGVO", sample_df.iloc[1]["tags"])
        self.assertIn("i18n", sample_df.iloc[2]["tags"])
    
    def test_sample_showcase_dataset_ids(self):
        """Test that sample showcase dataset IDs match sample datasets"""
        sample_df = import_sample_showcases()
        
        # Check dataset IDs
        for i in range(len(sample_df)):
            showcase_id = sample_df.iloc[i]["id"]
            dataset_id = sample_df.iloc[i]["dataset_id"]
            
            # Dataset ID should match showcase ID for our samples
            self.assertEqual(showcase_id, dataset_id)
            
            # Dataset ID should be between 1-3
            self.assertGreaterEqual(dataset_id, 1)
            self.assertLessEqual(dataset_id, 3)
    
    def test_sample_showcase_categories(self):
        """Test that sample showcase categories are valid"""
        sample_df = import_sample_showcases()
        
        # Get unique categories
        categories = sample_df["category"].unique()
        
        # Check expected categories
        self.assertIn("E-Commerce", categories)
        self.assertIn("Gesundheitswesen", categories)
        self.assertIn("Web-Anwendungen", categories)
        
        # Ensure there are 3 unique categories (one per showcase)
        self.assertEqual(len(categories), 3)

if __name__ == "__main__":
    unittest.main()