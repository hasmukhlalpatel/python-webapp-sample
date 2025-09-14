#!/bin/bash

# Azure App Service startup script for Python Flask app
echo "Starting Python Flask application..."

# Install dependencies if requirements.txt exists
if [ -f requirements.txt ]; then
    echo "Installing Python dependencies..."
    pip install -r requirements.txt
fi

# Set environment variables
export FLASK_APP=app.py
export FLASK_ENV=production

# Start the application with Gunicorn
echo "Starting Gunicorn server..."
gunicorn --bind 0.0.0.0:$PORT --workers 4 --timeout 120 app:app