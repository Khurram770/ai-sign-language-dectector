#!/bin/bash
# Startup script for Sign Language Detector

# Set default values
PORT=${PORT:-5000}
HOST=${HOST:-0.0.0.0}
CAMERA_INDEX=${CAMERA_INDEX:-0}
TTS_ENABLED=${TTS_ENABLED:-true}

# Export environment variables
export PORT
export HOST
export CAMERA_INDEX
export TTS_ENABLED
export FLASK_APP=app.py
export FLASK_ENV=production

# Create necessary directories
mkdir -p model data

# Run the application
if [ "$1" == "gunicorn" ]; then
    echo "Starting with Gunicorn..."
    exec gunicorn --bind ${HOST}:${PORT} --workers 2 --threads 2 --timeout 120 app:app
else
    echo "Starting with Flask development server..."
    exec python app.py
fi

