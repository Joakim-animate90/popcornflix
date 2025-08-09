#!/bin/bash
# Django migrations check script for pre-commit

# Try to find Python executable
if [ -f ".venv/bin/python" ]; then
    PYTHON=".venv/bin/python"
elif [ -f "venv/bin/python" ]; then
    PYTHON="venv/bin/python"
elif command -v python3 &> /dev/null; then
    PYTHON="python3"
elif command -v python &> /dev/null; then
    PYTHON="python"
else
    echo "Python not found. Skipping Django migrations check."
    exit 0
fi

# Run Django migrations check
$PYTHON manage.py makemigrations --check --dry-run
