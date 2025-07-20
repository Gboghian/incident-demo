#!/usr/bin/env python3
"""
Entry point for the Incident Management System Flask application.
This file imports and runs the Flask application.
"""

from extensions import create_app, db
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create the Flask application instance
app = create_app()

def initialize_database():
    """Initialize the database with tables if they don't exist."""
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")

if __name__ == '__main__':
    # Initialize database tables
    initialize_database()
    
    # Get configuration from environment
    host = os.environ.get('FLASK_HOST', '127.0.0.1')
    port = int(os.environ.get('FLASK_PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    print(f"Starting Incident Management System...")
    print(f"Application will be available at: http://{host}:{port}")
    print("Press CTRL+C to quit")
    
    # Run the Flask application
    app.run(
        host=host,
        port=port,
        debug=debug
    )
