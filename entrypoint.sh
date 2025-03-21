#!/bin/bash
set -e

# Initialize migrations if they don't exist
flask db init || true

# Create a fresh migration
flask db migrate -m "Initial migration"

# Run database migrations
flask db upgrade

# Start the application with Gunicorn
gunicorn --bind 0.0.0.0:8000 "app:create_app()"
