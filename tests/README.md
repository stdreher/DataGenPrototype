# Test Suite Documentation

This directory contains unit and integration tests for the Test Data Generator application.

## Test Structure

The test suite is organized into several files, each focused on testing a specific module:

- `test_data_generator.py`: Tests for the data generation functionality
- `test_field_definitions.py`: Tests for the field definition functions and configurations
- `test_export_utils.py`: Tests for the data export functionality (CSV, JSON, SQL)
- `test_database_utils.py`: Tests for the database operations
- `test_app_integration.py`: Integration tests for core application functionality

## Running Tests

To run the entire test suite:

```bash
python -m pytest
```

To run a specific test file:

```bash
python -m pytest tests/test_export_utils.py
```

To run tests with verbose output:

```bash
python -m pytest -v
```

## Test Coverage

The project uses pytest-cov to track test coverage. To run tests with coverage reporting:

```bash
python -m pytest --cov=. --cov-report=term-missing
```

Current test coverage:
- `export_utils.py`: 100% coverage
- `field_definitions.py`: 96% coverage
- `data_generator.py`: 75% coverage
- `database_utils.py`: 86% coverage
- `app.py`: 0% coverage (UI functionality is complex to test)

## Adding New Tests

When adding new functionality, please also add corresponding tests:

1. For new data fields, add tests to `test_field_definitions.py`
2. For new export formats, add tests to `test_export_utils.py`
3. For database schema changes, add tests to `test_database_utils.py`

## Mocking

Database tests use mocking to avoid actual database operations during testing.
The mocks for SQLAlchemy sessions are defined in `test_database_utils.py`.