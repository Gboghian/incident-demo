#!/usr/bin/env python3
"""
Initialize the database and create an admin user.
Run this script after setting up the Flask application.
"""

from extensions import create_app, db
from models import User, Incident
from datetime import datetime

def init_db():
    """Initialize the database with tables and sample data."""
    app = create_app()
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database tables created successfully!")
        
        # Check if admin user already exists
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            # Create admin user
            admin_user = User(
                username='admin',
                email='admin@example.com',
                first_name='System',
                last_name='Administrator',
                role='admin'
            )
            admin_user.set_password('admin123')  # Change this in production!
            
            db.session.add(admin_user)
            db.session.commit()
            print("Admin user created successfully!")
            print("Username: admin")
            print("Password: admin123")
            print("Please change the default password after first login!")
        else:
            print("Admin user already exists.")
        
        # Create a sample incident for testing
        sample_incident = Incident.query.first()
        if not sample_incident:
            sample_incident = Incident(
                title='Sample Incident - Server Downtime',
                description='This is a sample incident for testing purposes. The main server experienced unexpected downtime.',
                severity='high',
                category='Infrastructure',
                location='Data Center A',
                status='open',
                reporter_id=admin_user.id
            )
            db.session.add(sample_incident)
            db.session.commit()
            print("Sample incident created successfully!")

if __name__ == '__main__':
    init_db()
