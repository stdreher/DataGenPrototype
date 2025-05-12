import pytest
import pandas as pd
from data_generator import generate_data
from field_definitions import field_definitions

def test_generate_data_empty_fields():
    """Test that generate_data returns an empty DataFrame when no fields are selected"""
    df = generate_data({})
    assert isinstance(df, pd.DataFrame)
    assert df.empty

def test_generate_data_with_fields():
    """Test that generate_data returns a DataFrame with the correct fields"""
    # Test with username and email fields
    selected_fields = {
        "username": {"min_length": 6, "max_length": 12, "with_numbers": True},
        "email": {}
    }
    
    df = generate_data(selected_fields, num_records=5)
    
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert len(df) == 5
    assert "Benutzername" in df.columns
    assert "E-Mail" in df.columns

def test_generate_data_with_seed():
    """Test that generate_data produces the same results with the same seed"""
    selected_fields = {
        "username": {"min_length": 6, "max_length": 12, "with_numbers": True}
    }
    
    df1 = generate_data(selected_fields, num_records=5, seed=42)
    df2 = generate_data(selected_fields, num_records=5, seed=42)
    
    # The DataFrames should be identical
    pd.testing.assert_frame_equal(df1, df2)

def test_generate_data_different_seeds():
    """Test that generate_data produces different results with different seeds"""
    selected_fields = {
        "username": {"min_length": 6, "max_length": 12, "with_numbers": True}
    }
    
    df1 = generate_data(selected_fields, num_records=5, seed=42)
    df2 = generate_data(selected_fields, num_records=5, seed=43)
    
    # The DataFrames should be different
    with pytest.raises(AssertionError):
        pd.testing.assert_frame_equal(df1, df2)

def test_generate_data_with_permutation():
    """Test that permutation works as expected"""
    selected_fields = {
        "username": {"min_length": 6, "max_length": 12, "with_numbers": True, "permutate": True}
    }
    
    # Use a fixed seed for reproducibility
    df = generate_data(selected_fields, num_records=100, seed=42)
    
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 100
    assert "Benutzername" in df.columns

def test_generate_data_with_locale():
    """Test that locale affects the generated data"""
    selected_fields = {
        "city": {}  # City names should differ between locales
    }
    
    # Generate data with different locales
    df_de = generate_data(selected_fields, num_records=10, locale='de_DE', seed=42)
    df_us = generate_data(selected_fields, num_records=10, locale='en_US', seed=42)
    
    # The data should be different due to different locales
    assert df_de["Stadt"].tolist() != df_us["Stadt"].tolist()

def test_generate_data_invalid_field():
    """Test that invalid fields are gracefully handled"""
    selected_fields = {
        "invalid_field": {}
    }
    
    df = generate_data(selected_fields)
    
    assert isinstance(df, pd.DataFrame)
    assert df.empty  # No valid fields, so DataFrame should be empty