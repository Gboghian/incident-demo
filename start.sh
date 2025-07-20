#!/bin/bash
# Start script for the Incident Management System

# Change to the project directory
cd "$(dirname "$0")"

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
    echo "Activated virtual environment"
fi

# Set default environment variables
export FLASK_CONFIG=${FLASK_CONFIG:-development}
export FLASK_HOST=${FLASK_HOST:-127.0.0.1}
export FLASK_PORT=${FLASK_PORT:-5000}
export FLASK_DEBUG=${FLASK_DEBUG:-True}

echo "Starting Incident Management System..."
echo "Configuration: $FLASK_CONFIG"
echo "Host: $FLASK_HOST"
echo "Port: $FLASK_PORT"
echo "Debug: $FLASK_DEBUG"
echo ""

# Run the application
python run.py
