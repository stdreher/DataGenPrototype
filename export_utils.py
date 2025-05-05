import pandas as pd
import json
import re
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

def sanitize_table_name(name):
    """
    Sanitize the table name to be SQL-safe
    
    Args:
        name (str): Raw table name
        
    Returns:
        str: Sanitized table name
    """
    # Replace spaces with underscores and remove invalid characters
    sanitized = re.sub(r'[^\w]', '_', name)
    
    # Make sure it starts with a letter or underscore
    if sanitized[0].isdigit():
        sanitized = 'tbl_' + sanitized
    
    return sanitized.lower()

def format_value_for_sql(value):
    """
    Format a value for SQL INSERT statement
    
    Args:
        value: The value to format
        
    Returns:
        str: SQL-formatted value
    """
    if value is None:
        return 'NULL'
    elif isinstance(value, (int, float)):
        return str(value)
    else:
        # Escape quotes in strings and surround with quotes
        val_str = str(value)
        val_str = val_str.replace("'", "''")  # Escape single quotes
        val_str = val_str.replace(";", "")    # Remove semicolons for safety
        return "'" + val_str + "'"

def export_to_sql(df, table_name='testdaten'):
    """
    Export DataFrame to SQL INSERT statements
    
    Args:
        df (pandas.DataFrame): DataFrame to export
        table_name (str): Name of the table to insert into
        
    Returns:
        str: SQL INSERT statements
    """
    # Sanitize table name
    sanitized_table_name = sanitize_table_name(table_name)
    
    # Create string buffer for SQL statements
    sql_buffer = StringIO()
    
    # Write CREATE TABLE statement
    sql_buffer.write(f"-- SQL Script für {sanitized_table_name}\n")
    sql_buffer.write(f"-- Generiert am {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
    
    # Start with table creation
    columns = df.columns.tolist()
    sql_buffer.write(f"CREATE TABLE IF NOT EXISTS {sanitized_table_name} (\n")
    
    # Add columns (using VARCHAR for simplicity, in a real scenario you would infer types)
    column_definitions = []
    for col in columns:
        sanitized_col = re.sub(r'[^\w]', '_', col).lower()
        
        # Determine column type based on DataFrame dtypes
        if pd.api.types.is_numeric_dtype(df[col].dtype):
            if pd.api.types.is_integer_dtype(df[col].dtype):
                col_type = "INTEGER"
            else:
                col_type = "FLOAT"
        else:
            # Check typical length to determine VARCHAR size
            max_length = df[col].astype(str).str.len().max()
            col_type = f"VARCHAR({max(255, max_length)})"
            
        column_definitions.append(f"    {sanitized_col} {col_type}")
    
    sql_buffer.write(',\n'.join(column_definitions))
    sql_buffer.write("\n);\n\n")
    
    # Add a note that we're truncating the table
    sql_buffer.write(f"-- Löschen existierender Daten (optional)\n")
    sql_buffer.write(f"DELETE FROM {sanitized_table_name};\n\n")
    
    # Start INSERT statements
    sql_buffer.write("-- Datensätze einfügen\n")
    
    # Generate batch inserts (for better performance)
    batch_size = 100  # Insert in batches of 100
    total_rows = len(df)
    
    for i in range(0, total_rows, batch_size):
        batch = df.iloc[i:min(i+batch_size, total_rows)]
        
        # Column names for INSERT
        sanitized_columns = [re.sub(r'[^\w]', '_', col).lower() for col in columns]
        columns_str = ', '.join(sanitized_columns)
        
        # Start the batch INSERT
        sql_buffer.write(f"INSERT INTO {sanitized_table_name} ({columns_str}) VALUES\n")
        
        # Add each row
        values_list = []
        for _, row in batch.iterrows():
            # Format the values for SQL
            formatted_values = [format_value_for_sql(row[col]) for col in columns]
            values_str = f"({', '.join(formatted_values)})"
            values_list.append(values_str)
        
        # Join all values with commas
        sql_buffer.write(',\n'.join(values_list))
        sql_buffer.write(';\n\n')
    
    return sql_buffer.getvalue()
