#!/bin/bash
set -e

# Run database migrations
flask db upgrade

# Start the application with Gunicorn
gunicorn --bind 0.0.0.0:8000 "app:create_app()"
