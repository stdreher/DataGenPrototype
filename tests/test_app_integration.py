import pytest
import pandas as pd
import streamlit as st
from unittest.mock import patch, MagicMock

# Since we can't directly test the Streamlit app without running it,
# this is more of an integration test that checks the core functionality
# that the app relies on

def test_field_imports():
    """Test that all field-related imports work correctly."""
    # Import field definitions
    from field_definitions import field_definitions
    
    # Check that field_definitions is a dictionary with expected keys
    assert isinstance(field_definitions, dict)
    assert "username" in field_definitions
    assert "email" in field_definitions
    assert "password" in field_definitions

def test_generator_imports():
    """Test that the data generator imports and functions correctly."""
    # Import data generator
    from data_generator import generate_data
    
    # Test with a simple field configuration
    selected_fields = {
        "username": {"min_length": 6, "max_length": 12, "with_numbers": True}
    }
    
    # Generate a small dataset
    df = generate_data(selected_fields, num_records=3, seed=42)
    
    # Check the results
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 3
    assert "Benutzername" in df.columns

def test_export_imports():
    """Test that export utilities import and function correctly."""
    # Import export utilities
    from export_utils import export_to_csv, export_to_json, export_to_sql
    
    # Create a test dataframe
    data = {
        "Name": ["Test1", "Test2", "Test3"],
        "Value": [1, 2, 3]
    }
    df = pd.DataFrame(data)
    
    # Test export functions
    csv_output = export_to_csv(df)
    json_output = export_to_json(df)
    sql_output = export_to_sql(df)
    
    # Check outputs
    assert isinstance(csv_output, str)
    assert isinstance(json_output, str)
    assert isinstance(sql_output, str)
    
    # Check content
    assert "Test1" in csv_output
    assert "Test2" in json_output
    assert "Test3" in sql_output

@patch('database_utils.Session')
def test_database_imports(mock_session_class):
    """Test that database utilities import and function correctly."""
    # Setup mock
    mock_session = MagicMock()
    mock_session_class.return_value = mock_session
    mock_result = MagicMock()
    mock_result.inserted_primary_key = [1]
    mock_session.execute.return_value = mock_result
    
    # Import database utilities
    from database_utils import save_dataset_config
    
    # Test saving a configuration
    result = save_dataset_config(
        "Test Config", "Test Description", 10, "de_DE",
        ["username"], {"username": {"min_length": 6}},
        "2025-05-12"
    )
    
    # Check result
    assert result == 1
    assert mock_session.execute.called
    assert mock_session.commit.called