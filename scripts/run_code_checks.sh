#!/bin/bash

# This script runs code formatting, linting, and tests on key files
# It can be used without Git or pre-commit
#
# Usage:
#   ./scripts/run_code_checks.sh        # Run with sample tests
#   ./scripts/run_code_checks.sh --all  # Run all tests

# Get the directory of this script and set the root directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

# Debug: Print the calculated paths
echo "Script directory: $SCRIPT_DIR"
echo "Root directory: $ROOT_DIR"
echo ""

# Check command line arguments
RUN_ALL_TESTS=0
if [ "$1" == "--all" ]; then
  RUN_ALL_TESTS=1
fi

# Check if directories exist
if [ ! -d "$ROOT_DIR/tests" ]; then
  echo "Warning: 'tests' directory not found. Skipping tests."
  RUN_TESTS=0
else
  RUN_TESTS=1
fi

# List of key Python files to check (add/remove as needed)
PYTHON_FILES="$ROOT_DIR/data_generator.py $ROOT_DIR/export_utils.py $ROOT_DIR/field_definitions.py $ROOT_DIR/database_utils.py"

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
  if [ $RUN_ALL_TESTS -eq 1 ]; then
    echo -e "\n=== Running All Tests ==="
    echo "Running the full test suite"
    cd "$ROOT_DIR" && python -m pytest || { 
      echo "Tests failed. Fix the failing tests."; 
      exit 1; 
    }
    echo "All tests passed!"
  else
    echo -e "\n=== Running Sample Tests ==="
    echo "Running export_utils tests as a sample"
    python -m pytest "$ROOT_DIR/tests/test_export_utils.py" -v || { 
      echo "Tests failed. Fix the failing tests."; 
      exit 1; 
    }
    echo "Sample tests passed!"

    echo -e "\nTo run all tests, use: $0 --all"
  fi
else
  echo -e "\nTests skipped (tests directory not found)."
fi

echo -e "\n✅ All checks passed!"