import pytest
import pandas as pd
import json
import os
from unittest.mock import patch, MagicMock, call

# Import functions to test
from database_utils import (
    save_dataset_config, get_all_saved_datasets,
    get_dataset_by_id, delete_dataset, delete_dataset_range
)

@pytest.fixture
def mock_db_session():
    """Create a mock SQLAlchemy session."""
    with patch('database_utils.Session') as mock_session_class:
        # Create a mock session object
        mock_session = MagicMock()
        # Make the session class constructor return the mock session
        mock_session_class.return_value = mock_session
        yield mock_session

@pytest.fixture
def sample_dataset_config():
    """Sample dataset configuration for testing."""
    return {
        'name': 'Test Dataset',
        'description': 'A test dataset configuration',
        'num_records': 10,
        'locale': 'de_DE',
        'selected_fields': ['username', 'email', 'password'],
        'field_config': {
            'username': {'min_length': 6, 'max_length': 12, 'with_numbers': True},
            'email': {},
            'password': {'length': 12, 'include_special': True, 'include_digits': True}
        },
        'created_at': '2025-05-12 12:00:00'
    }

@pytest.fixture
def sample_db_result():
    """Create a sample database result row."""
    mock_row = MagicMock()
    mock_row.id = 1
    mock_row.name = 'Test Dataset'
    mock_row.description = 'A test dataset configuration'
    mock_row.num_records = 10
    mock_row.locale = 'de_DE'
    mock_row.fields = json.dumps(['username', 'email', 'password'])
    mock_row.field_config = json.dumps({
        'username': {'min_length': 6, 'max_length': 12, 'with_numbers': True},
        'email': {},
        'password': {'length': 12, 'include_special': True, 'include_digits': True}
    })
    mock_row.created_at = '2025-05-12 12:00:00'
    return mock_row

def test_save_dataset_config(mock_db_session, sample_dataset_config):
    """Test saving a dataset configuration."""
    # Setup
    config = sample_dataset_config
    mock_result = MagicMock()
    mock_result.inserted_primary_key = [1]  # Mock the returned ID
    mock_db_session.execute.return_value = mock_result
    
    # Test
    result_id = save_dataset_config(
        config['name'], config['description'], config['num_records'],
        config['locale'], config['selected_fields'], config['field_config'],
        config['created_at']
    )
    
    # Assert
    assert result_id == 1
    assert mock_db_session.execute.called
    assert mock_db_session.commit.called
    assert mock_db_session.close.called

def test_save_dataset_config_error(mock_db_session, sample_dataset_config):
    """Test error handling when saving a dataset configuration."""
    # Setup
    config = sample_dataset_config
    mock_db_session.execute.side_effect = Exception("Database error")
    
    # Test
    with pytest.raises(Exception) as exc_info:
        save_dataset_config(
            config['name'], config['description'], config['num_records'],
            config['locale'], config['selected_fields'], config['field_config'],
            config['created_at']
        )
    
    # Assert
    assert "Database error" in str(exc_info.value)
    assert mock_db_session.rollback.called
    assert mock_db_session.close.called

def test_get_all_saved_datasets(mock_db_session, sample_db_result):
    """Test retrieving all saved datasets."""
    # Setup
    mock_db_session.execute.return_value = [sample_db_result]
    
    # Test
    result = get_all_saved_datasets()
    
    # Assert
    assert isinstance(result, pd.DataFrame)
    assert not result.empty
    assert 'id' in result.columns
    assert 'name' in result.columns
    assert result['id'].iloc[0] == 1
    assert result['name'].iloc[0] == 'Test Dataset'
    assert mock_db_session.close.called

def test_get_dataset_by_id(mock_db_session, sample_db_result):
    """Test retrieving a dataset by ID."""
    # Setup
    mock_db_session.execute().fetchone.return_value = sample_db_result
    
    # Test
    result = get_dataset_by_id(1)
    
    # Assert
    assert isinstance(result, dict)
    assert result['id'] == 1
    assert result['name'] == 'Test Dataset'
    assert 'fields' in result
    assert 'field_config' in result
    assert mock_db_session.close.called

def test_get_dataset_by_id_not_found(mock_db_session):
    """Test retrieving a non-existent dataset."""
    # Setup
    mock_db_session.execute().fetchone.return_value = None
    
    # Test
    result = get_dataset_by_id(999)
    
    # Assert
    assert result is None
    assert mock_db_session.close.called

def test_delete_dataset(mock_db_session):
    """Test deleting a dataset."""
    # Setup
    mock_result = MagicMock()
    mock_result.rowcount = 1
    mock_db_session.execute.return_value = mock_result
    
    # Test
    result = delete_dataset(1)
    
    # Assert
    assert result is True
    assert mock_db_session.execute.called
    assert mock_db_session.commit.called
    assert mock_db_session.close.called

def test_delete_dataset_not_found(mock_db_session):
    """Test deleting a non-existent dataset."""
    # Setup
    mock_result = MagicMock()
    mock_result.rowcount = 0
    mock_db_session.execute.return_value = mock_result
    
    # Test
    result = delete_dataset(999)
    
    # Assert
    assert result is False
    assert mock_db_session.commit.called
    assert mock_db_session.close.called

def test_delete_dataset_range(mock_db_session):
    """Test deleting a range of datasets."""
    # Setup
    mock_result = MagicMock()
    mock_result.rowcount = 5
    mock_db_session.execute.return_value = mock_result
    
    # Test
    result = delete_dataset_range(1, 5)
    
    # Assert
    assert result == 5
    assert mock_db_session.execute.called
    assert mock_db_session.commit.called
    assert mock_db_session.close.called