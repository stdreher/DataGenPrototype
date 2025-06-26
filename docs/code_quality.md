# Code Quality Checks for Test Data Generator

This document outlines the code quality checks implemented in this project and how to use them.

## Overview

The Test Data Generator project uses several tools to maintain code quality:

1. **Black** - Code formatter that automatically formats Python code following a consistent style
2. **Flake8** - Linter that checks for style issues, programming errors, and potential bugs
3. **Pytest** - Testing framework for writing and running unit tests

These tools can be run manually or automatically as git hooks before each commit.

## Running Checks Manually

### Option 1: Run Code Checks Script

To run checks without committing:

```bash
# Run with sample tests (faster)
./scripts/run_code_checks.sh

# Run with all tests
./scripts/run_code_checks.sh --all
```

This script will:
- Format code with Black
- Check for issues with Flake8
- Run tests (either a sample or all tests)

### Option 2: Run Individual Tools

Format code with Black:
```bash
black .
```

Check for issues with Flake8:
```bash
flake8
```

Run all tests:
```bash
python -m pytest
```

## Git Hooks Setup

Git hooks automatically run checks before each commit, preventing commits with formatting or test issues.

To set up git hooks:

```bash
./scripts/setup_git_hooks.sh
```

This will:
1. Install pre-commit if needed
2. Configure git hooks for the repository

### What Gets Checked on Commit

Before each commit, the following checks run automatically:
- Black formatting on modified Python files
- Flake8 linting on modified Python files
- Pytest runs on the entire test suite

If any check fails, the commit is rejected with an error message. Fix the issues and try committing again.

### Skipping Hooks Temporarily

In rare cases where you need to bypass checks (not recommended for normal use):

```bash
git commit --no-verify -m "Your commit message"
```

## Configuration Files

The project includes several configuration files:

- `.pre-commit-config.yaml` - Configures pre-commit hooks
- `pyproject.toml` - Contains Black and pytest configuration
- `setup.cfg` - Contains Flake8 configuration

## Best Practices

1. Run `./scripts/run_code_checks.sh` before pushing changes
2. Keep tests up to date with new features
3. Maintain high test coverage
4. Don't bypass git hooks except in rare circumstances
5. Address all Flake8 warnings, don't suppress them without good reason