#!/bin/bash

# Debugging: Check if nc is available
if ! command -v nc &> /dev/null
then
    echo "nc could not be found"
    exit 1
fi

# Wait for MySQL to be ready
until nc -z mysql-container 3306; do
  echo "Waiting for MySQL..."
  sleep 1
done

# Run database migrations
flask db upgrade

# Start the application with Gunicorn
gunicorn --bind 0.0.0.0:8000 app:app
