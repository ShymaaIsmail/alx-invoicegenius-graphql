#!/usr/bin/env bash

# Exit if any command fails
set -o errexit

export POETRY_ACTIVE=0 

echo "🔧 Using Python version  d ddddd: $(python --version)"

# Upgrade pip and setup tools
pip install --upgrade pip setuptools wheel

# Install dependencies
pip install -r requirements.txt

# Collect static files (if you use them)
python manage.py collectstatic --noinput

# Apply migrations (optional if you want to run them during build)
python manage.py migrate --noinput
