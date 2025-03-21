#!/bin/bash
set -e

# Start the application with Gunicorn
gunicorn --bind 0.0.0.0:8000 "app:create_app()"
