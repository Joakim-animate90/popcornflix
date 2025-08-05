#!/bin/bash

# Setup script for pre-commit hooks in Django project
echo "Setting up pre-commit hooks for popcornflix..."

# Install development dependencies
echo "Installing development dependencies..."
pip install -r requirements-dev.txt

# Install pre-commit hooks
echo "Installing pre-commit hooks..."
pre-commit install

# Run pre-commit on all files to check setup
echo "Running pre-commit on all files to verify setup..."
pre-commit run --all-files

echo "Pre-commit hooks setup complete!"
echo ""
echo "What happens now:"
echo "✓ Before each commit, the following will run automatically:"
echo "  - Trailing whitespace removal"
echo "  - End-of-file fixing"
echo "  - YAML/JSON validation"
echo "  - Large file detection"
echo "  - Python code formatting (Black)"
echo "  - Import sorting (isort)"
echo "  - Python linting (flake8)"
echo "  - Django system checks"
echo "  - Django migrations check"
echo ""
echo "If any check fails, the commit will be blocked until issues are fixed."
echo "To bypass hooks (not recommended): git commit --no-verify"
