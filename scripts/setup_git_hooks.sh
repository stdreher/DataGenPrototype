#!/bin/bash

# Get the directory of this script and set the root directory
SCRIPT_DIR="$(dirname "$(readlink -f "$0" 2>/dev/null || echo "${0}")")"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

echo "Setting up git hooks for the Test Data Generator project"
echo "======================================================"
echo

# Check if Git is available
if ! command -v git &> /dev/null; then
    echo "Error: Git is not installed or not available in PATH"
    exit 1
fi

# Check if we are in a Git repository
if ! git -C "$ROOT_DIR" rev-parse --git-dir &> /dev/null; then
    echo "Error: Not a Git repository"
    echo "Please initialize a Git repository first with: git init"
    exit 1
fi

# Install pre-commit if not already installed
echo "Installing pre-commit..."
pip install pre-commit

# Install the git hooks
echo "Installing git hooks..."
cd "$ROOT_DIR" && pre-commit install

# Create a summary of the installed hooks
echo
echo "Git hooks have been set up successfully!"
echo "======================================================"
echo "The following checks will run before each commit:"
echo "  - Black (code formatting)"
echo "  - Flake8 (code linting)"
echo "  - Pytest (unit tests)"
echo
echo "To manually run the hooks on all files, use:"
echo "  pre-commit run --all-files"
echo
echo "To run code checks without git, use:"
echo "  ./scripts/run_code_checks.sh      # Run with sample tests"
echo "  ./scripts/run_code_checks.sh --all # Run all tests"