import pandas as pd
import json
from io import StringIO, BytesIO

def export_to_csv(df):
    """
    Export DataFrame to CSV format
    
    Args:
        df (pandas.DataFrame): DataFrame to export
        
    Returns:
        str: CSV string
    """
    # Create a string buffer
    csv_buffer = StringIO()
    
    # Write the dataframe to the buffer
    df.to_csv(csv_buffer, index=False)
    
    # Get the CSV string
    csv_string = csv_buffer.getvalue()
    
    return csv_string

def export_to_json(df):
    """
    Export DataFrame to JSON format
    
    Args:
        df (pandas.DataFrame): DataFrame to export
        
    Returns:
        str: JSON string
    """
    # Convert dataframe to JSON records
    json_records = df.to_json(orient='records', indent=2)
    
    return json_records
