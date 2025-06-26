import os
import json
import pandas as pd
from sqlalchemy import (
    create_engine,
    Column,
    String,
    Integer,
    JSON,
    MetaData,
    Table,
    select,
    delete,
)
from sqlalchemy.orm import declarative_base, sessionmaker

# Get database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///testdata.db")

# Create engine to connect to the database
engine = create_engine(str(DATABASE_URL))

# Create Base class for declarative class definitions
Base = declarative_base()

# Create metadata object for raw SQL operations
metadata = MetaData()

# Define the saved_datasets table
saved_datasets = Table(
    "saved_datasets",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("description", String),
    Column("num_records", Integer, nullable=False),
    Column("locale", String, nullable=False),
    Column("fields", JSON, nullable=False),
    Column("field_config", JSON, nullable=False),
    Column("created_at", String, nullable=False),
)

# Define the community_showcases table
community_showcases = Table(
    "community_showcases",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String, nullable=False),
    Column("description", String),
    Column("author", String),
    Column("category", String),
    Column("tags", JSON),
    Column("dataset_id", Integer),
    Column("upvotes", Integer, default=0),
    Column("created_at", String, nullable=False),
    Column("is_featured", Integer, default=0),  # 0 = not featured, 1 = featured
)

# Create tables if they don't exist
metadata.create_all(engine)

# Create session factory
Session = sessionmaker(bind=engine)


def save_dataset_config(
    name, description, num_records, locale, selected_fields, field_config, created_at
):
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
            created_at=created_at,
        )

        result = session.execute(stmt)
        session.commit()

        # Get the ID of the inserted row
        try:
            return result.inserted_primary_key[0]
        except (TypeError, IndexError):
            return None

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
    # Create sample datasets for when database is unavailable
    sample_datasets = [
        {
            "id": 1,
            "name": "E-Commerce Kundendaten",
            "description": "Realistische Kundendaten für einen Online-Shop",
            "num_records": 100,
            "locale": "de_DE",
            "fields": [
                "username",
                "email",
                "full_name",
                "phone_number",
                "street_address",
                "city",
                "zip_code",
                "country",
                "credit_card",
            ],
            "field_config": {},
            "created_at": "2025-05-21",
        },
        {
            "id": 2,
            "name": "Pseudonymisierte Patientendaten",
            "description": "DSGVO-konforme Gesundheitsdaten für Tests",
            "num_records": 50,
            "locale": "de_DE",
            "fields": [
                "username",
                "full_name",
                "date_of_birth",
                "street_address",
                "city",
                "phone_number",
            ],
            "field_config": {},
            "created_at": "2025-05-21",
        },
        {
            "id": 3,
            "name": "Internationale Webseiten-Nutzerdaten",
            "description": "Multi-Locale Testdaten für internationale Anwendungen",
            "num_records": 150,
            "locale": "en_US",
            "fields": [
                "username",
                "email",
                "full_name",
                "street_address",
                "city",
                "country",
                "currency_code",
            ],
            "field_config": {},
            "created_at": "2025-05-21",
        },
    ]

    try:
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
                    "id": row.id,
                    "name": row.name,
                    "description": row.description,
                    "num_records": row.num_records,
                    "locale": row.locale,
                    "fields": json.loads(row.fields),
                    "field_config": json.loads(row.field_config),
                    "created_at": row.created_at,
                }
                datasets.append(dataset)

            # If no datasets found in DB, return sample datasets
            if not datasets:
                return pd.DataFrame(sample_datasets)

            # Convert to DataFrame
            return pd.DataFrame(datasets)

        except Exception:
            # Return sample datasets if database is unavailable
            return pd.DataFrame(sample_datasets)

        finally:
            session.close()

    except Exception:
        # Return sample datasets if any connection issues occur
        return pd.DataFrame(sample_datasets)


def get_dataset_by_id(dataset_id):
    """
    Get a saved dataset configuration by ID

    Args:
        dataset_id (int): ID of the dataset to retrieve

    Returns:
        dict: Dataset configuration
    """
    # Sample datasets for when database is unavailable
    # or when loading from sample showcases (IDs 1-3)
    sample_datasets = {
        1: {
            "id": 1,
            "name": "E-Commerce Kundendaten",
            "description": "Realistische Kundendaten für einen Online-Shop",
            "num_records": 100,
            "locale": "de_DE",
            "fields": [
                "username",
                "email",
                "full_name",
                "phone_number",
                "street_address",
                "city",
                "zip_code",
                "country",
                "credit_card",
            ],
            "field_config": {
                "username": {"prefix": "", "suffix": ""},
                "email": {"domain": "example.com"},
                "full_name": {"gender": None},
                "phone_number": {"format": "+49 ### #######"},
                "street_address": {"include_secondary": True},
                "credit_card": {"provider": "mastercard"},
            },
            "created_at": "2025-05-21",
        },
        2: {
            "id": 2,
            "name": "Pseudonymisierte Patientendaten",
            "description": "DSGVO-konforme Gesundheitsdaten für Tests",
            "num_records": 50,
            "locale": "de_DE",
            "fields": [
                "username",
                "full_name",
                "date_of_birth",
                "street_address",
                "city",
                "phone_number",
            ],
            "field_config": {
                "username": {"prefix": "patient_", "suffix": ""},
                "full_name": {"gender": None},
                "date_of_birth": {"start_date": "1940-01-01", "end_date": "2005-12-31"},
                "street_address": {"include_secondary": False},
                "phone_number": {"format": "+49-###-########"},
            },
            "created_at": "2025-05-21",
        },
        3: {
            "id": 3,
            "name": "Internationale Webseiten-Nutzerdaten",
            "description": "Multi-Locale Testdaten für internationale Anwendungen",
            "num_records": 150,
            "locale": "en_US",
            "fields": [
                "username",
                "email",
                "full_name",
                "street_address",
                "city",
                "country",
                "currency_code",
            ],
            "field_config": {
                "username": {"prefix": "", "suffix": ""},
                "email": {"domain": "international-example.com"},
                "full_name": {"gender": None},
                "country": {"continent": "any"},
            },
            "created_at": "2025-05-21",
        },
    }

    # Check if we're looking for a sample dataset
    if dataset_id in sample_datasets:
        return sample_datasets[dataset_id]

    # Try to get from database
    try:
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
                "id": result.id,
                "name": result.name,
                "description": result.description,
                "num_records": result.num_records,
                "locale": result.locale,
                "fields": json.loads(result.fields),
                "field_config": json.loads(result.field_config),
                "created_at": result.created_at,
            }

            return dataset

        except Exception as e:
            # If database error, check if we can provide a sample dataset
            if dataset_id in sample_datasets:
                return sample_datasets[dataset_id]
            return None

        finally:
            session.close()

    except Exception:
        # In case of any connection issue, check if we can provide a sample dataset
        if dataset_id in sample_datasets:
            return sample_datasets[dataset_id]
        return None


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


def delete_dataset_range(start_id, end_id):
    """
    Delete a range of saved dataset configurations by ID range

    Args:
        start_id (int): Start ID of the range to delete
        end_id (int): End ID of the range to delete

    Returns:
        int: Number of rows deleted
    """
    # Create a session
    session = Session()

    try:
        # Delete rows with IDs in the specified range
        stmt = delete(saved_datasets).where(
            saved_datasets.c.id >= start_id, saved_datasets.c.id <= end_id
        )
        result = session.execute(stmt)
        session.commit()

        # Return the number of rows deleted
        return result.rowcount

    except Exception as e:
        session.rollback()
        raise e

    finally:
        session.close()


# Community Showcase Functions


def save_community_showcase(
    title, description, author, category, tags, dataset_id, created_at, is_featured=0
):
    """
    Save a community showcase to the database

    Args:
        title (str): Title of the showcase
        description (str): Description of the showcase
        author (str): Author of the showcase
        category (str): Category of the showcase
        tags (list): List of tags for the showcase
        dataset_id (int): ID of the associated dataset
        created_at (str): Creation timestamp
        is_featured (int): Whether the showcase is featured (0 = no, 1 = yes)

    Returns:
        int: ID of the saved showcase
    """
    # Create a session
    session = Session()

    try:
        # Convert tags list to JSON
        tags_json = json.dumps(tags)

        # Insert the showcase into the database
        stmt = community_showcases.insert().values(
            title=title,
            description=description,
            author=author,
            category=category,
            tags=tags_json,
            dataset_id=dataset_id,
            upvotes=0,
            created_at=created_at,
            is_featured=is_featured,
        )

        result = session.execute(stmt)
        session.commit()

        # Get the ID of the inserted row
        try:
            return result.inserted_primary_key[0]
        except (TypeError, IndexError):
            return None

    except Exception as e:
        session.rollback()
        raise e

    finally:
        session.close()


def get_all_community_showcases():
    """
    Get all community showcases from the database

    Returns:
        pandas.DataFrame: DataFrame containing all community showcases
    """
    # Create a session
    session = Session()

    try:
        # Select all rows from the community_showcases table
        stmt = select(community_showcases)
        result = session.execute(stmt)

        # Convert to list of dictionaries
        showcases = []
        for row in result:
            showcase = {
                "id": row.id,
                "title": row.title,
                "description": row.description,
                "author": row.author,
                "category": row.category,
                "tags": json.loads(row.tags) if row.tags else [],
                "dataset_id": row.dataset_id,
                "upvotes": row.upvotes,
                "created_at": row.created_at,
                "is_featured": row.is_featured,
            }
            showcases.append(showcase)

        # Convert to DataFrame
        return pd.DataFrame(showcases)

    except Exception as e:
        raise e

    finally:
        session.close()


def get_community_showcase_by_id(showcase_id):
    """
    Get a community showcase by ID

    Args:
        showcase_id (int): ID of the showcase to retrieve

    Returns:
        dict: Showcase information
    """
    # Create a session
    session = Session()

    try:
        # Select the row with the specified ID
        stmt = select(community_showcases).where(
            community_showcases.c.id == showcase_id
        )
        result = session.execute(stmt).fetchone()

        if result is None:
            return None

        # Convert to dictionary
        showcase = {
            "id": result.id,
            "title": result.title,
            "description": result.description,
            "author": result.author,
            "category": result.category,
            "tags": json.loads(result.tags) if result.tags else [],
            "dataset_id": result.dataset_id,
            "upvotes": result.upvotes,
            "created_at": result.created_at,
            "is_featured": result.is_featured,
        }

        return showcase

    except Exception as e:
        raise e

    finally:
        session.close()


def get_featured_showcases():
    """
    Get all featured community showcases from the database

    Returns:
        pandas.DataFrame: DataFrame containing featured community showcases
    """
    # Create a session
    session = Session()

    try:
        # Select all featured showcases
        stmt = select(community_showcases).where(community_showcases.c.is_featured == 1)
        result = session.execute(stmt)

        # Convert to list of dictionaries
        showcases = []
        for row in result:
            showcase = {
                "id": row.id,
                "title": row.title,
                "description": row.description,
                "author": row.author,
                "category": row.category,
                "tags": json.loads(row.tags) if row.tags else [],
                "dataset_id": row.dataset_id,
                "upvotes": row.upvotes,
                "created_at": row.created_at,
                "is_featured": row.is_featured,
            }
            showcases.append(showcase)

        # Convert to DataFrame
        return pd.DataFrame(showcases)

    except Exception as e:
        raise e

    finally:
        session.close()


def upvote_showcase(showcase_id):
    """
    Increment the upvote count for a showcase

    Args:
        showcase_id (int): ID of the showcase to upvote

    Returns:
        bool: True if successful, False otherwise
    """
    # Create a session
    session = Session()

    try:
        # Get the current showcase
        stmt = select(community_showcases).where(
            community_showcases.c.id == showcase_id
        )
        result = session.execute(stmt).fetchone()

        if result is None:
            return False

        # Increment the upvote count
        current_upvotes = result.upvotes
        update_stmt = (
            community_showcases.update()
            .where(community_showcases.c.id == showcase_id)
            .values(upvotes=current_upvotes + 1)
        )
        session.execute(update_stmt)
        session.commit()

        return True

    except Exception as e:
        session.rollback()
        raise e

    finally:
        session.close()


def delete_showcase(showcase_id):
    """
    Delete a community showcase by ID

    Args:
        showcase_id (int): ID of the showcase to delete

    Returns:
        bool: True if successful, False otherwise
    """
    # Create a session
    session = Session()

    try:
        # Delete the row with the specified ID
        stmt = delete(community_showcases).where(
            community_showcases.c.id == showcase_id
        )
        result = session.execute(stmt)
        session.commit()

        # Return True if a row was deleted
        return result.rowcount > 0

    except Exception as e:
        session.rollback()
        raise e

    finally:
        session.close()


def toggle_showcase_featured(showcase_id):
    """
    Toggle the featured status of a showcase

    Args:
        showcase_id (int): ID of the showcase to toggle

    Returns:
        bool: True if featured, False if not featured after toggle
    """
    # Create a session
    session = Session()

    try:
        # Get the current showcase
        stmt = select(community_showcases).where(
            community_showcases.c.id == showcase_id
        )
        result = session.execute(stmt).fetchone()

        if result is None:
            return False

        # Toggle the featured status
        current_featured = result.is_featured
        new_featured = 0 if current_featured == 1 else 1
        update_stmt = (
            community_showcases.update()
            .where(community_showcases.c.id == showcase_id)
            .values(is_featured=new_featured)
        )
        session.execute(update_stmt)
        session.commit()

        return new_featured == 1

    except Exception as e:
        session.rollback()
        raise e

    finally:
        session.close()


def search_showcases(search_term=None, category=None, tags=None):
    """
    Search community showcases based on various criteria

    Args:
        search_term (str, optional): Term to search in title and description
        category (str, optional): Category to filter by
        tags (list, optional): List of tags to filter by

    Returns:
        pandas.DataFrame: DataFrame containing matching showcases
    """
    # Create a session
    session = Session()

    try:
        # Start with a base query
        stmt = select(community_showcases)

        # Apply filters if provided
        if search_term:
            stmt = stmt.where(
                community_showcases.c.title.ilike(f"%{search_term}%")
                | community_showcases.c.description.ilike(f"%{search_term}%")
            )

        if category:
            stmt = stmt.where(community_showcases.c.category == category)

        # Execute the query
        result = session.execute(stmt)

        # Convert to list of dictionaries
        showcases = []
        for row in result:
            row_tags = json.loads(row.tags) if row.tags else []

            # Filter by tags if provided
            if tags and not any(tag in row_tags for tag in tags):
                continue

            showcase = {
                "id": row.id,
                "title": row.title,
                "description": row.description,
                "author": row.author,
                "category": row.category,
                "tags": row_tags,
                "dataset_id": row.dataset_id,
                "upvotes": row.upvotes,
                "created_at": row.created_at,
                "is_featured": row.is_featured,
            }
            showcases.append(showcase)

        # Convert to DataFrame
        return pd.DataFrame(showcases)

    except Exception as e:
        raise e

    finally:
        session.close()
