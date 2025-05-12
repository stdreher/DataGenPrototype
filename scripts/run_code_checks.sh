#!/bin/bash

# This script runs code formatting, linting, and tests
# It can be used without Git or pre-commit

echo "=== Running Black (code formatting) ==="
black . --check || { echo "Black check failed. Run 'black .' to format code."; exit 1; }

echo -e "\n=== Running Flake8 (code linting) ==="
flake8 || { echo "Flake8 check failed. Fix the linting issues."; exit 1; }

echo -e "\n=== Running Pytest (unit tests) ==="
python -m pytest || { echo "Tests failed. Fix the failing tests."; exit 1; }

echo -e "\n✅ All checks passed!"