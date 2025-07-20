#!/usr/bin/env python3
"""
Database migration script to add new fields to User model
Run this script to update existing database with new engineer fields
"""
from extensions import create_app, db
from models import User, Incident

def migrate_database():
    """Add new columns to existing User table."""
    app = create_app()
    
    with app.app_context():
        # Add new columns to users table
        try:
            # Check if columns already exist
            inspector = db.inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('users')]
            
            if 'department' not in columns:
                db.engine.execute('ALTER TABLE users ADD COLUMN department VARCHAR(50)')
                print("Added 'department' column to users table")
            
            if 'role_level' not in columns:
                db.engine.execute('ALTER TABLE users ADD COLUMN role_level VARCHAR(30)')
                print("Added 'role_level' column to users table")
            
            if 'notifications_enabled' not in columns:
                db.engine.execute('ALTER TABLE users ADD COLUMN notifications_enabled BOOLEAN DEFAULT 1')
                print("Added 'notifications_enabled' column to users table")
            
            print("Database migration completed successfully!")
            
        except Exception as e:
            print(f"Migration error: {e}")
            print("Creating tables from scratch...")
            # If migration fails, recreate all tables
            db.drop_all()
            db.create_all()
            print("All tables recreated successfully!")
            
            # Create default admin user
            admin_user = User(
                username='admin',
                email='admin@company.com',
                first_name='System',
                last_name='Administrator',
                department='IT',
                role_level='manager',
                role='admin',
                notifications_enabled=True
            )
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            db.session.commit()
            print("Default admin user created (admin/admin123)")

if __name__ == '__main__':
    migrate_database()
