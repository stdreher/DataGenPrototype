#!/bin/bash

# Install pre-commit if not already installed
pip install pre-commit

# Initialize pre-commit hooks
pre-commit install

echo "Git hooks have been set up successfully!"
echo "The following checks will run before each commit:"
echo "  - Black (code formatting)"
echo "  - Flake8 (code linting)"
echo "  - Pytest (unit tests)"
echo ""
echo "To manually run the hooks on all files, use:"
echo "  pre-commit run --all-files"