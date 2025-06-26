# 🎲 Test Data Generator / Testdaten Generator

A Streamlit-based tool for generating synthetic test data with a user-friendly interface and GDPR-compliant data pseudonymization capabilities.

## Language / Sprache

This documentation is available in two languages:
Diese Dokumentation ist in zwei Sprachen verfügbar:

- [English Documentation](README_ENG.md)
- [Deutsche Dokumentation](README_GER.md)

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

## Overview / Übersicht

The Test Data Generator is a comprehensive tool designed to create high-quality synthetic data for testing web applications and databases. It offers a wide range of field types, flexible configuration options, and multiple export formats.

Der Testdaten Generator ist ein umfassendes Tool zur Erstellung hochwertiger synthetischer Daten für das Testen von Webanwendungen und Datenbanken. Er bietet eine breite Palette von Feldtypen, flexible Konfigurationsoptionen und mehrere Exportformate.

### Key Features / Hauptfunktionen

- Generate data for over 20 different field types
- Configure parameters for each field
- Export to CSV, JSON, or SQL formats
- Save and load generation configurations
- GDPR-compliant data pseudonymization with multiple methods
- Side-by-side comparison of original and pseudonymized data
- Animated interface with dice roll and lock effects
- Multilingual support (German UI, multiple data locales)

### Screenshots / Bildschirmfotos

*Screenshots will be added here / Bildschirmfotos werden hier hinzugefügt*

## Quick Start / Schnellstart

```bash
# Install dependencies / Abhängigkeiten installieren
pip install streamlit pandas numpy faker sqlalchemy openpyxl psycopg2-binary

# Start the application / Anwendung starten
streamlit run Home.py
```

For detailed instructions, please refer to the language-specific documentation.
Für detaillierte Anweisungen, bitte beziehen Sie sich auf die sprachspezifische Dokumentation.