import os
import json
import pandas as pd
from sqlalchemy import create_engine, Column, String, Integer, JSON, MetaData, Table, select, delete, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Get database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

# Create engine to connect to the database
engine = create_engine(DATABASE_URL)

# Create Base class for declarative class definitions
Base = declarative_base()

# Create metadata object for raw SQL operations
metadata = MetaData()

# Define the saved_datasets table
saved_datasets = Table(
    'saved_datasets', 
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String, nullable=False),
    Column('description', String),
    Column('num_records', Integer, nullable=False),
    Column('locale', String, nullable=False),
    Column('fields', JSON, nullable=False),
    Column('field_config', JSON, nullable=False),
    Column('created_at', String, nullable=False),
)

# Create tables if they don't exist
metadata.create_all(engine)

# Create session factory
Session = sessionmaker(bind=engine)

def save_dataset_config(name, description, num_records, locale, selected_fields, field_config, created_at):
    """
    Save dataset configuration to the database
    
    Args:
        name (str): Name of the dataset
        description (str): Description of the dataset
        num_records (int): Number of records in the dataset
        locale (str): Locale used for generation
        selected_fields (list): List of selected field names
        field_config (dict): Configuration for each field
        created_at (str): Creation timestamp
        
    Returns:
        int: ID of the saved dataset
    """
    # Create a session
    session = Session()
    
    try:
        # Convert selected_fields list to a list of field names
        fields_json = json.dumps(selected_fields)
        field_config_json = json.dumps(field_config)
        
        # Insert the dataset config into the database
        stmt = saved_datasets.insert().values(
            name=name,
            description=description,
            num_records=num_records,
            locale=locale,
            fields=fields_json,
            field_config=field_config_json,
            created_at=created_at
        )
        
        result = session.execute(stmt)
        session.commit()
        
        # Get the ID of the inserted row
        return result.inserted_primary_key[0]
    
    except Exception as e:
        session.rollback()
        raise e
    
    finally:
        session.close()

def get_all_saved_datasets():
    """
    Get all saved dataset configurations from the database
    
    Returns:
        pandas.DataFrame: DataFrame containing all saved datasets
    """
    # Create a session
    session = Session()
    
    try:
        # Select all rows from the saved_datasets table
        stmt = select(saved_datasets)
        result = session.execute(stmt)
        
        # Convert to list of dictionaries
        datasets = []
        for row in result:
            dataset = {
                'id': row.id,
                'name': row.name,
                'description': row.description,
                'num_records': row.num_records,
                'locale': row.locale,
                'fields': json.loads(row.fields),
                'field_config': json.loads(row.field_config),
                'created_at': row.created_at
            }
            datasets.append(dataset)
        
        # Convert to DataFrame
        return pd.DataFrame(datasets)
    
    except Exception as e:
        raise e
    
    finally:
        session.close()

def get_dataset_by_id(dataset_id):
    """
    Get a saved dataset configuration by ID
    
    Args:
        dataset_id (int): ID of the dataset to retrieve
        
    Returns:
        dict: Dataset configuration
    """
    # Create a session
    session = Session()
    
    try:
        # Select the row with the specified ID
        stmt = select(saved_datasets).where(saved_datasets.c.id == dataset_id)
        result = session.execute(stmt).fetchone()
        
        if result is None:
            return None
        
        # Convert to dictionary
        dataset = {
            'id': result.id,
            'name': result.name,
            'description': result.description,
            'num_records': result.num_records,
            'locale': result.locale,
            'fields': json.loads(result.fields),
            'field_config': json.loads(result.field_config),
            'created_at': result.created_at
        }
        
        return dataset
    
    except Exception as e:
        raise e
    
    finally:
        session.close()

def delete_dataset(dataset_id):
    """
    Delete a saved dataset configuration by ID
    
    Args:
        dataset_id (int): ID of the dataset to delete
        
    Returns:
        bool: True if successful, False otherwise
    """
    # Create a session
    session = Session()
    
    try:
        # Delete the row with the specified ID
        stmt = delete(saved_datasets).where(saved_datasets.c.id == dataset_id)
        result = session.execute(stmt)
        session.commit()
        
        # Return True if a row was deleted
        return result.rowcount > 0
    
    except Exception as e:
        session.rollback()
        raise e
    
    finally:
        session.close()