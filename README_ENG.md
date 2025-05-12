# 🎲 Test Data Generator

A Streamlit-based test data generator with a user interface for specification and random permutation of web portal user data.

## Development

### Testing
The project includes a comprehensive test suite using pytest:
```bash
# Run all tests
python -m pytest

# Run tests with coverage report
python -m pytest --cov=. --cov-report=term-missing
```

### Code Quality
Code quality is maintained using Black, Flake8, and pre-commit hooks:
```bash
# Run the code quality checks
./scripts/run_code_checks.sh
```

For more information about code quality tools, see [Code Quality Documentation](docs/code_quality.md).

## Feature Overview

The Test Data Generator is a tool for creating synthetic test data for web portals and applications. It offers the following main features:

- **Flexible Data Generation**: Generate synthetic data with customizable fields and formats
- **Field Configuration**: Adjust parameters for each field (e.g., password length, number inclusion, etc.)
- **Data Export**: Export generated data as CSV, JSON, or SQL
- **Database Connection**: Save and load your generation configurations for reuse
- **Multilingual**: Fully in German with support for various data locales
- **Animations**: Dice roll animations for data generation, resetting, and loading configurations

## Technical Details

The Test Data Generator was developed with the following technologies:

- **Streamlit**: User interface and application framework
- **Pandas**: Data processing and manipulation
- **Faker**: Synthetic data generation
- **SQLAlchemy**: Database interaction
- **PostgreSQL**: Persistent storage of configurations

## Instructions

### Installation and Launch

1. Ensure that Python 3.11 or higher is installed
2. Clone the repository
3. Install the required packages:
   ```
   pip install streamlit pandas numpy faker sqlalchemy psycopg2-binary
   ```
4. Start the application: `streamlit run app.py`

### Dependencies

- **streamlit**: Version 1.35.0 or higher
- **pandas**: Version 2.2.0 or higher
- **numpy**: Version 1.26.0 or higher
- **faker**: Version 37.0.0 or higher
- **sqlalchemy**: Version 2.0.35 or higher
- **psycopg2-binary**: Version 2.9.9 or higher

### Usage

#### 1. Select and Configure Fields

- Choose the desired fields from the various categories (Identity, Address, Contact, etc.)
- All fields are disabled by default, so you can select only the fields you need
- Configure the parameters for each selected field according to your requirements
- Enable permutation for individual fields to randomly mix the data

#### 2. Generate Data

- Specify the number of records to generate
- Choose the desired locale (affects the format of the generated data)
- Optionally use a random seed for reproducible results
- Click "Generate Data" to start the process
- Use the "Reset" button to clear the data preview and start over

#### 3. Export Data

- View the preview of the generated data
- Choose the desired export format (CSV, JSON, or SQL)
- For SQL export, you can customize the table name and view a preview of the SQL script
- Download the generated data

#### 4. Save and Load Configurations

- Save your preferred generation configurations in the database
- An automatic summary with 1. Number of records, 2. Data locale, and 3. Export format is displayed in the description field
- Load saved configurations with the "Load Configuration" form
- Delete configurations you no longer need with the "Delete Configuration" form
- Use the ID from the list of saved configurations displayed below

## Available Data Fields

The generator supports a variety of fields, grouped into the following categories:

### Identity
- Username
- Email
- Password
- Full Name

### Address
- Street Address
- City
- State
- ZIP Code
- Country

### Contact
- Phone Number
- Job Title
- Company

### Personal
- Date of Birth
- Gender
- Credit Card

### Internet
- User Agent
- IPv4 Address
- IPv6 Address
- MAC Address

### Miscellaneous
- UUID
- Color
- Currency Code

## SQL Export Functionality

The generator features an advanced SQL export function that allows you to export the generated test data directly as an SQL script:

- **Data Type Detection**: The application automatically detects the appropriate SQL data types for your fields
- **Customizable Table Name**: Define a custom name for the SQL table
- **Compatibility**: The generated SQL scripts are compatible with PostgreSQL, MySQL, SQLite, and most other SQL dialects
- **Preview**: A preview of the SQL script is displayed before download
- **Batch Inserts**: Data is inserted in batches to improve efficiency
- **Security**: Values are properly escaped for SQL to prevent SQL injection

The generated SQL script contains:
1. CREATE TABLE statement with appropriate data types
2. Optional DELETE statement to empty the table
3. INSERT statements for all records
4. Documenting comments with timestamp

## Database Functionality

The application uses a PostgreSQL database to store generation configurations. The following operations are supported:

- **Save**: Save the current configuration with name and description
- **Load**: Load a saved configuration by its ID
- **Delete**: Remove configurations you no longer need
- **List**: Display all saved configurations

## Project Structure

- `app.py`: Main application with Streamlit user interface
- `data_generator.py`: Core functions for data generation
- `field_definitions.py`: Definitions and parameters for all supported fields
- `export_utils.py`: Helper functions for data export
- `database_utils.py`: Functions for database interaction
- `.streamlit/config.toml`: Streamlit configuration

## Customization and Extension

### Adding New Fields

To add a new field:

1. Define a generator function in `field_definitions.py`
2. Add the field definition to the `field_definitions` dictionary
3. Assign the field to a category in `field_categories` in `app.py`

### Support for New Export Formats

To add a new export format:

1. Implement an export function in `export_utils.py`
2. Add the format to the selection options in `app.py`
3. Handle the new format in the export section

## License

This project is licensed under the MIT License. See the LICENSE file for details.