"""
Flask CLI commands for the Incident Management System.
These commands provide database initialization, user management, and utility functions.

TEMPORARILY DISABLED: All commands except init-db are commented out for debugging.
"""

import click
from flask import current_app
from flask.cli import with_appcontext
from extensions import db
from models import User, Incident
from datetime import datetime
import os
import random


@click.command()
@with_appcontext
def init_db():
    """Initialize the database with tables."""
    try:
        print("🚀 Starting database initialization...")
        
        # Create database directory if it doesn't exist
        db_uri = current_app.config.get('SQLALCHEMY_DATABASE_URI', '')
        if db_uri.startswith('sqlite:///'):
            db_path = db_uri.replace('sqlite:///', '')
            db_dir = os.path.dirname(db_path)
            if db_dir and not os.path.exists(db_dir):
                os.makedirs(db_dir)
                print(f'📁 Created database directory: {db_dir}')
        
        # Create all tables
        print("🔧 Creating database tables...")
        db.create_all()
        print('✅ Database tables created successfully!')
        
        # Show created tables
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        print(f'📋 Created tables: {", ".join(tables)}')
        
        # Check if any users exist
        user_count = User.query.count()
        print(f"👥 Current users in database: {user_count}")
        
        if user_count == 0:
            print("💡 No users found. Consider running 'flask create-admin' to create an admin user.")
        
    except Exception as e:
        print(f'❌ Error initializing database: {e}')


# =============================================================================
# TEMPORARILY DISABLED COMMANDS FOR DEBUGGING
# Uncomment the sections below to re-enable specific commands
# =============================================================================

# @click.command()
# @with_appcontext
# def reset_db():
#     """Reset the database (drop and recreate all tables)."""
#     if click.confirm('⚠️  This will delete ALL data. Are you sure?'):
#         try:
#             print("🗑️  Dropping all existing tables...")
#             db.drop_all()
#             print('✅ Dropped all tables')
#             
#             print("🔧 Recreating database tables...")
#             db.create_all()
#             print('✅ Database reset successfully!')
#             
#             # Show recreated tables
#             inspector = db.inspect(db.engine)
#             tables = inspector.get_table_names()
#             print(f'📋 Recreated tables: {", ".join(tables)}')
#             
#         except Exception as e:
#             print(f'❌ Error resetting database: {e}')
#     else:
#         print("❌ Database reset cancelled.")


# @click.command()
# @click.option('--username', prompt='Admin username', help='Username for admin account')
# @click.option('--email', prompt='Admin email', help='Email for admin account')
# @click.option('--password', prompt='Admin password', hide_input=True, confirmation_prompt=True, help='Password for admin account')
# @click.option('--first-name', prompt='First name', help='Admin first name')
# @click.option('--last-name', prompt='Last name', help='Admin last name')
# @with_appcontext
# def create_admin(username, email, password, first_name, last_name):
#     """Create an admin user."""
#     try:
#         print(f"👤 Creating admin user: {username}")
#         
#         # Check if user already exists
#         if User.query.filter_by(username=username).first():
#             print(f'❌ User with username "{username}" already exists!')
#             return
#         
#         if User.query.filter_by(email=email).first():
#             print(f'❌ User with email "{email}" already exists!')
#             return
#         
#         print("🔧 Creating user record...")
#         admin_user = User(
#             username=username,
#             email=email,
#             first_name=first_name,
#             last_name=last_name,
#             department='IT',
#             role_level='manager',
#             role='admin',
#             notifications_enabled=True
#         )
#         admin_user.set_password(password)
#         
#         print("💾 Saving to database...")
#         db.session.add(admin_user)
#         db.session.commit()
#         
#         print('✅ Admin user created successfully!')
#         print(f'👤 Username: {username}')
#         print(f'📧 Email: {email}')
#         print(f'🔐 Role: admin')
#         
#     except Exception as e:
#         print(f'❌ Error creating admin user: {e}')
#         db.session.rollback()


# @click.command()
# @click.option('--count', default=10, help='Number of sample incidents to create')
# @with_appcontext
# def seed_data(count):
#     """Seed the database with sample data."""
#     # [Large function commented out - uncomment when needed]
#     pass


# @click.command()
# @with_appcontext
# def db_stats():
#     """Show database statistics."""
#     # [Large function commented out - uncomment when needed]
#     pass


# @click.command()
# @with_appcontext
# def list_users():
#     """List all users in the database."""
#     # [Large function commented out - uncomment when needed]
#     pass


# @click.command()
# @with_appcontext
# def backup_db():
#     """Create a backup of the database."""
#     # [Large function commented out - uncomment when needed]
#     pass


# @click.command()
# @with_appcontext
# def migrate_db():
#     """Migrate database schema to latest version."""
#     # [Large function commented out - uncomment when needed]
#     pass


# @click.command()
# @with_appcontext
# def setup_db():
#     """Complete database setup with tables and default admin user."""
#     # [Large function commented out - uncomment when needed]
#     pass


# @click.command()
# @with_appcontext
# def check_db():
#     """Check database health and connectivity."""
#     # [Large function commented out - uncomment when needed]
#     pass


# @click.command()
# @with_appcontext
# def help_commands():
#     """Show all available CLI commands with descriptions."""
#     # [Large function commented out - uncomment when needed]
#     pass


def register_commands(app):
    """Register CLI commands with the Flask app."""
    print("🔧 Registering CLI commands (DEBUG MODE: only init-db enabled)")
    
    # Database commands
    app.cli.add_command(init_db)
    
    # TEMPORARILY DISABLED FOR DEBUGGING
    # Uncomment the lines below to re-enable specific commands:
    
    # app.cli.add_command(reset_db)
    # app.cli.add_command(setup_db)
    # app.cli.add_command(migrate_db)
    # app.cli.add_command(check_db)
    # app.cli.add_command(backup_db)
    
    # User management commands
    # app.cli.add_command(create_admin)
    # app.cli.add_command(list_users)
    
    # Data commands
    # app.cli.add_command(seed_data)
    # app.cli.add_command(db_stats)
    
    # Help command
    # app.cli.add_command(help_commands)
    
    print(f"✅ Registered {len(app.cli.commands)} CLI command(s): {list(app.cli.commands.keys())}")
