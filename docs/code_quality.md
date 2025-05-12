# Code Quality Tools

This project uses several tools to maintain code quality:

## 1. Black (Code Formatter)

Black is an opinionated code formatter that automatically formats Python code to comply with PEP 8.

### Usage:
```bash
# Format all Python files
black .

# Check if files need formatting without actually changing them
black . --check
```

## 2. Flake8 (Linter)

Flake8 is a tool that checks Python code against coding style (PEP 8) and programming errors.

### Usage:
```bash
# Run linting checks
flake8
```

## 3. pytest (Testing Framework)

pytest is used for running unit tests and ensuring code correctness.

### Usage:
```bash
# Run all tests
python -m pytest

# Run tests with coverage report
python -m pytest --cov=. --cov-report=term-missing
```

## 4. pre-commit (Git Hooks Framework)

pre-commit is used to manage and maintain Git hooks.

### Setup:
```bash
# Run the setup script
./scripts/setup_git_hooks.sh
```

### Manual Usage:
```bash
# Run all checks on all files
pre-commit run --all-files
```

## 5. Manual Check Script

A convenience script that runs all code quality checks is provided.

### Usage:
```bash
# Run all checks (formatting, linting, tests)
./scripts/run_code_checks.sh
```

## Configuration Files

- `.pre-commit-config.yaml`: Configuration for pre-commit hooks
- `pyproject.toml`: Configuration for Black and pytest
- `setup.cfg`: Configuration for Flake8