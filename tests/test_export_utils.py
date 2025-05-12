import pytest
import pandas as pd
import json
import re
from export_utils import (
    export_to_csv, export_to_json, export_to_sql,
    sanitize_table_name, format_value_for_sql
)

@pytest.fixture
def sample_dataframe():
    """Create a sample DataFrame for testing export functions."""
    data = {
        "Benutzername": ["user1", "user2", "user3"],
        "E-Mail": ["user1@example.com", "user2@example.com", "user3@example.com"],
        "Passwort": ["pass123", "pass456", "pass789"]
    }
    return pd.DataFrame(data)

def test_export_to_csv(sample_dataframe):
    """Test CSV export functionality."""
    csv_output = export_to_csv(sample_dataframe)
    
    # Validate output is a string
    assert isinstance(csv_output, str)
    
    # Validate CSV format
    lines = csv_output.strip().split('\n')
    assert lines[0] == "Benutzername,E-Mail,Passwort"
    assert "user1,user1@example.com,pass123" in csv_output
    assert "user2,user2@example.com,pass456" in csv_output
    assert "user3,user3@example.com,pass789" in csv_output

def test_export_to_json(sample_dataframe):
    """Test JSON export functionality."""
    json_output = export_to_json(sample_dataframe)
    
    # Validate output is a string
    assert isinstance(json_output, str)
    
    # Parse and validate JSON content
    json_data = json.loads(json_output)
    assert isinstance(json_data, list)
    assert len(json_data) == 3
    
    # Check content
    assert json_data[0]["Benutzername"] == "user1"
    assert json_data[1]["E-Mail"] == "user2@example.com"
    assert json_data[2]["Passwort"] == "pass789"

def test_sanitize_table_name():
    """Test table name sanitization."""
    # Test standard case
    assert sanitize_table_name("Test Table") == "test_table"
    
    # Test special characters
    assert sanitize_table_name("Test-Table$#!") == "test_table___"
    
    # Test starting with digit
    assert sanitize_table_name("123Table") == "tbl_123table"

def test_format_value_for_sql():
    """Test SQL value formatting."""
    # Test string with single quotes
    assert format_value_for_sql("It's a test") == "'It''s a test'"
    
    # Test string with semicolons
    assert format_value_for_sql("test;injection") == "'testinjection'"
    
    # Test integers and floats
    assert format_value_for_sql(123) == "123"
    assert format_value_for_sql(12.34) == "12.34"
    
    # Test None value
    assert format_value_for_sql(None) == "NULL"

def test_export_to_sql(sample_dataframe):
    """Test SQL export functionality."""
    sql_output = export_to_sql(sample_dataframe, "test_table")
    
    # Validate output is a string
    assert isinstance(sql_output, str)
    
    # Check for SQL components
    assert "CREATE TABLE IF NOT EXISTS test_table" in sql_output
    assert "benutzername VARCHAR" in sql_output
    assert "e_mail VARCHAR" in sql_output
    assert "passwort VARCHAR" in sql_output
    
    # Check for data insertion
    assert "INSERT INTO test_table" in sql_output
    assert "'user1'" in sql_output
    assert "'user2@example.com'" in sql_output
    
    # Check for DELETE statement
    assert "DELETE FROM test_table" in sql_output

def test_export_to_sql_numeric_data():
    """Test SQL export with numeric data."""
    # Create a DataFrame with numeric data
    data = {
        "ID": [1, 2, 3],
        "Value": [10.5, 20.7, 30.9]
    }
    df = pd.DataFrame(data)
    
    sql_output = export_to_sql(df, "numeric_table")
    
    # Check for correct column types
    assert "id INTEGER" in sql_output
    assert "value FLOAT" in sql_output
    
    # Check for correct data insertion
    assert "1.0" in sql_output
    assert "10.5" in sql_output
    assert "2.0" in sql_output
    assert "20.7" in sql_output
    assert "3.0" in sql_output
    assert "30.9" in sql_output