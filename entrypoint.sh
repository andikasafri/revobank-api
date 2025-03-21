#!/bin/bash
set -e

# Remove existing migrations directory
rm -rf migrations/*

# Initialize fresh migrations
flask db init

# Run database migrations
flask db upgrade || flask db migrate -m "initial migration" && flask db upgrade

# Start the application with Gunicorn
gunicorn --bind 0.0.0.0:8000 "app:create_app()"
