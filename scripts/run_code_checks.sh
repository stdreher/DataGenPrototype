#!/bin/bash

# This script runs code formatting, linting, and tests on key files
# It can be used without Git or pre-commit

# Check if directories exist
if [ ! -d "tests" ]; then
  echo "Warning: 'tests' directory not found. Skipping tests."
  RUN_TESTS=0
else
  RUN_TESTS=1
fi

# List of key Python files to check (add/remove as needed)
PYTHON_FILES="data_generator.py export_utils.py field_definitions.py database_utils.py"

echo "=== Running Black (code formatting) on key files ==="
echo "Checking files: $PYTHON_FILES"
black $PYTHON_FILES --check || { 
  echo "Black check failed. Run 'black $PYTHON_FILES' to format code."; 
  exit 1; 
}
echo "Black check passed!"

echo -e "\n=== Running Flake8 (code linting) on key files ==="
echo "Checking files: $PYTHON_FILES"
flake8 $PYTHON_FILES || { 
  echo "Flake8 check failed. Fix the linting issues."; 
  exit 1; 
}
echo "Flake8 check passed!"

if [ $RUN_TESTS -eq 1 ]; then
  echo -e "\n=== Running Sample Tests ==="
  echo "Running export_utils tests as a sample"
  python -m pytest tests/test_export_utils.py -v || { 
    echo "Tests failed. Fix the failing tests."; 
    exit 1; 
  }
  echo "Sample tests passed!"
  
  echo -e "\nTo run all tests, use: python -m pytest"
else
  echo -e "\nTests skipped (tests directory not found)."
fi

echo -e "\n✅ All checks passed!"