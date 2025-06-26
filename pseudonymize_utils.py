import pandas as pd
import numpy as np
import hashlib
import re
from faker import Faker


def pseudonymize_data(df, columns_to_pseudonymize, methods=None, locale="de_DE"):
    """
    Pseudonymize specific columns in a DataFrame.

    Args:
        df (pandas.DataFrame): DataFrame containing the data to pseudonymize
        columns_to_pseudonymize (dict): Dictionary mapping column names to pseudonymization methods
                                      e.g. {'name': 'hash', 'email': 'replace', 'phone': 'mask'}
        methods (dict, optional): Dictionary with custom pseudonymization configuration.
                               e.g. {'mask': {'show_first': 3, 'show_last': 2, 'char': '*'}}
        locale (str, optional): Locale for Faker when replacing values. Defaults to "de_DE".

    Returns:
        pandas.DataFrame: DataFrame with pseudonymized data
    """
    # Create a copy of the dataframe to avoid modifying the original
    pseudonymized_df = df.copy()
    
    # Initialize Faker with the specified locale
    fake = Faker(locale)
    
    # Default methods configuration
    default_methods = {
        'mask': {'show_first': 2, 'show_last': 2, 'char': '*'},
        'replace': {'preserve_format': True},
        'offset': {'numeric_offset': 5, 'date_offset_days': 10},
    }
    
    # Update with user-provided methods
    if methods:
        for method, config in methods.items():
            if method in default_methods:
                default_methods[method].update(config)
            else:
                default_methods[method] = config
    
    # Process each column according to the specified pseudonymization method
    for column, method in columns_to_pseudonymize.items():
        if column not in df.columns:
            continue
            
        if method == 'hash':
            pseudonymized_df[column] = pseudonymized_df[column].apply(
                lambda x: hash_value(x) if pd.notna(x) else x
            )
            
        elif method == 'mask':
            config = default_methods['mask']
            pseudonymized_df[column] = pseudonymized_df[column].apply(
                lambda x: mask_value(x, config['show_first'], config['show_last'], config['char']) if pd.notna(x) else x
            )
            
        elif method == 'replace':
            config = default_methods['replace']
            preserve = config.get('preserve_format', True)
            
            # Determine appropriate faker method based on column name and content
            faker_method = determine_faker_method(column, df[column])
            
            # Replace values with Faker data
            pseudonymized_df[column] = pseudonymized_df[column].apply(
                lambda x: generate_fake_data(fake, faker_method, x, preserve) if pd.notna(x) else x
            )
            
        elif method == 'offset':
            config = default_methods['offset']
            
            # Attempt to determine the data type and apply appropriate offset
            if is_numeric_column(df[column]):
                pseudonymized_df[column] = df[column] + config['numeric_offset']
            elif is_date_column(df[column]):
                pseudonymized_df[column] = df[column] + pd.Timedelta(days=config['date_offset_days'])
    
    return pseudonymized_df


def hash_value(value):
    """Hash a value using SHA-256."""
    if not isinstance(value, str):
        value = str(value)
    return hashlib.sha256(value.encode()).hexdigest()


def mask_value(value, show_first=2, show_last=2, char='*'):
    """
    Mask a value by replacing middle characters with a specified character.
    
    Example: "john.doe@example.com" -> "jo**************om"
    """
    if not isinstance(value, str):
        value = str(value)
        
    length = len(value)
    
    if length <= show_first + show_last:
        return value
    
    return value[:show_first] + char * (length - show_first - show_last) + value[-show_last:]


def determine_faker_method(column_name, series):
    """
    Determine the most appropriate Faker method based on column name and content.
    
    Args:
        column_name (str): Name of the column
        series (pandas.Series): Series containing the data
        
    Returns:
        str: Faker method name to use
    """
    column_lower = column_name.lower()
    
    # Simple mapping based on common column names
    if any(term in column_lower for term in ['name', 'vorname', 'nachname', 'fullname']):
        return 'name'
    elif any(term in column_lower for term in ['email', 'mail', 'e-mail']):
        return 'email'
    elif any(term in column_lower for term in ['phone', 'telefon', 'tel', 'mobil']):
        return 'phone_number'
    elif any(term in column_lower for term in ['address', 'adresse', 'strasse', 'straße']):
        return 'street_address'
    elif any(term in column_lower for term in ['city', 'stadt', 'ort']):
        return 'city'
    elif any(term in column_lower for term in ['zip', 'plz', 'postleitzahl']):
        return 'zipcode'
    elif any(term in column_lower for term in ['country', 'land']):
        return 'country'
    elif any(term in column_lower for term in ['company', 'firma', 'unternehmen']):
        return 'company'
    elif any(term in column_lower for term in ['job', 'position', 'titel', 'beruf']):
        return 'job'
    elif any(term in column_lower for term in ['username', 'user', 'benutzer']):
        return 'user_name'
    elif any(term in column_lower for term in ['password', 'passwort']):
        return 'password'
    elif any(term in column_lower for term in ['birthdate', 'birth', 'geburt', 'dob']):
        return 'date_of_birth'
    else:
        # If we can't determine a specific type, use a generic method based on content
        sample = series.dropna().iloc[0] if not series.dropna().empty else ""
        if isinstance(sample, str):
            if '@' in sample:
                return 'email'
            elif re.search(r'\d{2,}', sample) and len(sample) < 20:
                return 'phone_number'
            elif len(sample) > 20:
                return 'text'
            else:
                return 'word'
        return 'word'  # Default fallback


def generate_fake_data(faker, method, original_value, preserve_format=True):
    """
    Generate fake data using the specified Faker method.
    Optionally preserve the format (uppercase/lowercase/title case) of the original value.
    
    Args:
        faker (Faker): Initialized Faker instance
        method (str): Faker method to use
        original_value: Original value to be replaced
        preserve_format (bool): Whether to preserve format of the original value
        
    Returns:
        str: Generated fake data
    """
    # Get the Faker method
    faker_method = getattr(faker, method, None)
    
    if faker_method is None:
        return original_value
    
    # Generate new value
    new_value = str(faker_method())
    
    # Preserve format if requested
    if preserve_format and isinstance(original_value, str):
        if original_value.isupper():
            return new_value.upper()
        elif original_value.islower():
            return new_value.lower()
        elif original_value.istitle():
            return new_value.title()
    
    return new_value


def is_numeric_column(series):
    """Check if a pandas Series contains numeric data."""
    return pd.api.types.is_numeric_dtype(series)


def is_date_column(series):
    """Check if a pandas Series contains date data."""
    return pd.api.types.is_datetime64_dtype(series)


def get_pseudonymization_methods():
    """
    Get the available pseudonymization methods with descriptions.
    
    Returns:
        dict: Dictionary with method names as keys and descriptions as values
    """
    return {
        'hash': 'Wandelt den Originalwert in einen SHA-256 Hash-Wert um (nicht umkehrbar)',
        'mask': 'Maskiert einen Teil des Wertes (z.B. "John Doe" → "Jo*****oe")',
        'replace': 'Ersetzt den Wert durch realistische Fake-Daten',
        'offset': 'Verschiebt numerische oder Datumswerte um einen festen Betrag'
    }