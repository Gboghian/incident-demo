"""
Flask application instance for the Incident Management System.
This module creates the Flask app instance for use by WSGI servers.
"""

from extensions import create_app

# Create Flask app instance
app = create_app()

# For WSGI deployment (e.g., with Gunicorn)
if __name__ == '__main__':
    app.run()
