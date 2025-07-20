"""
Flask CLI commands for the Incident Management System.
These commands provide database initialization, user management, and utility functions.
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


# Temporarily disabled for debugging
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


# Temporarily disabled for debugging
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


@click.command()
@click.option('--count', default=10, help='Number of sample incidents to create')
@with_appcontext
def seed_data(count):
    """Seed the database with sample data."""
    try:
        print(f"🌱 Starting database seeding with {count} incidents...")
        
        # Check if we have users
        users = User.query.all()
        if not users:
            print("❌ No users found! Create users first.")
            return
        
        print(f"👥 Found {len(users)} users for seeding")
        
        # Sample incident data
        sample_incidents = [
            {
                'title': 'Database Connection Timeout',
                'description': 'Application experiencing intermittent database connection timeouts during peak hours.',
                'severity': 'high',
                'category': 'database',
                'status': 'open'
            },
            {
                'title': 'API Rate Limiting Issues',
                'description': 'Third-party API calls failing due to rate limiting. Need to implement backoff strategy.',
                'severity': 'medium',
                'category': 'api',
                'status': 'in_progress'
            },
            {
                'title': 'Memory Leak in User Service',
                'description': 'User service showing gradual memory increase over time, causing performance degradation.',
                'severity': 'critical',
                'category': 'performance',
                'status': 'open'
            },
            {
                'title': 'SSL Certificate Expiration',
                'description': 'Production SSL certificate expires in 7 days. Need to renew and deploy.',
                'severity': 'high',
                'category': 'security',
                'status': 'resolved'
            },
            {
                'title': 'Login Page Rendering Issue',
                'description': 'Users reporting login page not rendering correctly on mobile devices.',
                'severity': 'medium',
                'category': 'frontend',
                'status': 'in_progress'
            }
        ]
        
        incidents_created = 0
        print("🔧 Creating sample incidents...")
        
        for i in range(count):
            # Cycle through sample incidents
            sample = sample_incidents[i % len(sample_incidents)]
            
            # Select random user as reporter
            reporter = random.choice(users)
            
            incident = Incident(
                title=f"{sample['title']} #{i+1}",
                description=sample['description'],
                severity=sample['severity'],
                category=sample['category'],
                status=sample['status'],
                location=f"Server-{random.randint(1, 10)}",
                reporter_id=reporter.id,
                created_at=datetime.utcnow()
            )
            
            db.session.add(incident)
            incidents_created += 1
            
            # Print progress for every 5 incidents
            if incidents_created % 5 == 0:
                print(f"📝 Created {incidents_created}/{count} incidents...")
        
        print("💾 Saving incidents to database...")
        db.session.commit()
        
        print(f'✅ Successfully created {incidents_created} sample incidents!')
        
        # Show statistics
        total_incidents = Incident.query.count()
        open_incidents = Incident.query.filter_by(status='open').count()
        in_progress = Incident.query.filter_by(status='in_progress').count()
        resolved = Incident.query.filter_by(status='resolved').count()
        
        print("📊 Database statistics:")
        print(f"   Total incidents: {total_incidents}")
        print(f"   Open: {open_incidents}")
        print(f"   In Progress: {in_progress}")
        print(f"   Resolved: {resolved}")
        
    except Exception as e:
        print(f'❌ Error seeding database: {e}')
        db.session.rollback()


@click.command()
@with_appcontext
def db_stats():
    """Show database statistics."""
    try:
        print("📊 Database Statistics")
        print("=" * 50)
        
        # User statistics
        total_users = User.query.count()
        print(f"👥 Querying {total_users} users...")
        
        admin_users = User.query.filter_by(role='admin').count()
        manager_users = User.query.filter_by(role='manager').count()
        regular_users = User.query.filter_by(role='user').count()
        
        print(f"👥 Users:")
        print(f"   Total: {total_users}")
        print(f"   Admins: {admin_users}")
        print(f"   Managers: {manager_users}")
        print(f"   Regular: {regular_users}")
        
        # Department breakdown
        if total_users > 0:
            print(f"\n🏢 Analyzing departments...")
            departments = db.session.query(User.department, db.func.count(User.id)).group_by(User.department).all()
            print(f"🏢 Departments:")
            for dept, count in departments:
                dept_name = dept or "Not specified"
                print(f"   {dept_name}: {count}")
        
        # Incident statistics
        total_incidents = Incident.query.count()
        print(f"\n🎫 Querying {total_incidents} incidents...")
        
        open_incidents = Incident.query.filter_by(status='open').count()
        in_progress = Incident.query.filter_by(status='in_progress').count()
        resolved = Incident.query.filter(Incident.status.in_(['resolved', 'closed'])).count()
        
        print(f"🎫 Incidents:")
        print(f"   Total: {total_incidents}")
        print(f"   Open: {open_incidents}")
        print(f"   In Progress: {in_progress}")
        print(f"   Resolved: {resolved}")
        
        # Severity breakdown
        if total_incidents > 0:
            print(f"\n⚠️  Analyzing severity levels...")
            severities = db.session.query(Incident.severity, db.func.count(Incident.id)).group_by(Incident.severity).all()
            print(f"⚠️  Severity breakdown:")
            for severity, count in severities:
                print(f"   {severity.title()}: {count}")
        
        # Recent activity
        print(f"\n🕒 Fetching recent incidents...")
        recent_incidents = Incident.query.order_by(Incident.created_at.desc()).limit(5).all()
        if recent_incidents:
            print(f"🕒 Recent incidents:")
            for incident in recent_incidents:
                print(f"   #{incident.id}: {incident.title[:50]}{'...' if len(incident.title) > 50 else ''}")
        
    except Exception as e:
        print(f'❌ Error getting database statistics: {e}')


@click.command()
@with_appcontext
def list_users():
    """List all users in the database."""
    try:
        print("👥 Fetching all users from database...")
        users = User.query.all()
        
        if not users:
            print("👥 No users found in database.")
            return
        
        print(f"👥 Found {len(users)} users:")
        print("=" * 80)
        print(f"{'ID':<4} {'Username':<20} {'Email':<30} {'Role':<10} {'Department':<15}")
        print("-" * 80)
        
        for i, user in enumerate(users, 1):
            print(f"{user.id:<4} {user.username:<20} {user.email:<30} {user.role:<10} {user.department or 'N/A':<15}")
            
            # Print progress for large datasets
            if i % 25 == 0:
                print(f"   ... processed {i}/{len(users)} users")
            
    except Exception as e:
        print(f'❌ Error listing users: {e}')


@click.command()
@with_appcontext
def backup_db():
    """Create a backup of the database."""
    try:
        from shutil import copy2
        import time
        
        print("💾 Starting database backup process...")
        
        # Get database path
        db_uri = current_app.config.get('SQLALCHEMY_DATABASE_URI', '')
        if not db_uri.startswith('sqlite:///'):
            print("❌ Backup only supported for SQLite databases")
            return
        
        db_path = db_uri.replace('sqlite:///', '')
        if not os.path.exists(db_path):
            print(f"❌ Database file not found: {db_path}")
            return
        
        # Create backup filename with timestamp
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        backup_path = f"{db_path}.backup_{timestamp}"
        
        print(f"📁 Source: {db_path}")
        print(f"📁 Backup: {backup_path}")
        print("🔧 Copying database file...")
        
        copy2(db_path, backup_path)
        
        print("✅ Database backup created successfully!")
        
        # Show backup size
        backup_size = os.path.getsize(backup_path)
        print(f"📊 Backup size: {backup_size:,} bytes")
        
    except Exception as e:
        print(f'❌ Error creating backup: {e}')


@click.command()
@with_appcontext
def migrate_db():
    """Migrate database schema to latest version."""
    try:
        print("🔄 Starting database migration...")
        
        # Check if migration is needed
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        
        if 'users' not in tables:
            print("❌ Users table not found. Run 'flask init-db' first.")
            return
        
        # Check existing columns
        print("🔍 Analyzing current database schema...")
        user_columns = [col['name'] for col in inspector.get_columns('users')]
        print(f"📋 Current user table columns: {', '.join(user_columns)}")
        
        new_columns_added = 0
        
        # Add missing columns
        missing_columns = [
            ('department', 'VARCHAR(50)'),
            ('role_level', 'VARCHAR(30)'),
            ('notifications_enabled', 'BOOLEAN DEFAULT 1')
        ]
        
        for col_name, col_def in missing_columns:
            if col_name not in user_columns:
                print(f"🔧 Adding '{col_name}' column...")
                try:
                    with db.engine.connect() as connection:
                        connection.execute(db.text(f'ALTER TABLE users ADD COLUMN {col_name} {col_def}'))
                        connection.commit()
                    new_columns_added += 1
                    print(f"✅ Added '{col_name}' column")
                except Exception as col_error:
                    print(f"❌ Failed to add '{col_name}': {col_error}")
        
        if new_columns_added > 0:
            print(f"✅ Added {new_columns_added} new columns to users table")
        else:
            print("✅ Database schema is up to date")
        
        print("🎉 Migration completed successfully!")
        
    except Exception as e:
        print(f'❌ Migration error: {e}')
        print("💡 Consider running 'flask reset-db' to recreate tables from scratch")


@click.command()
@with_appcontext
def setup_db():
    """Complete database setup with tables and default admin user."""
    try:
        print('🔧 Starting complete database setup...')
        
        # Initialize database
        print('📋 Step 1: Initializing database tables...')
        db.create_all()
        print('✅ Database tables created')
        
        # Check if admin user exists
        admin_exists = User.query.filter_by(role='admin').first()
        if not admin_exists:
            print('👤 Step 2: Creating default admin user...')
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
            
            print('✅ Default admin user created:')
            print('   Username: admin')
            print('   Password: admin123')
            print('   ⚠️  Please change the default password!')
        else:
            print('👤 Admin user already exists, skipping creation')
        
        print('\n🎉 Database setup completed successfully!')
        print('🚀 You can now start the application with: flask run')
        
    except Exception as e:
        print(f'❌ Error during setup: {e}')


@click.command()
@with_appcontext
def check_db():
    """Check database health and connectivity."""
    try:
        print("🔍 Checking database health...")
        
        # Test database connection
        print("🔗 Testing database connection...")
        with db.engine.connect() as connection:
            connection.execute(db.text('SELECT 1'))
        print("✅ Database connection successful")
        
        # Check tables
        print("📋 Checking database tables...")
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        
        expected_tables = ['users', 'incidents']
        missing_tables = [table for table in expected_tables if table not in tables]
        
        if missing_tables:
            print(f"❌ Missing tables: {', '.join(missing_tables)}")
            print("💡 Run 'flask init-db' to create missing tables")
        else:
            print("✅ All required tables present")
        
        # Check data integrity
        print("🔍 Checking data integrity...")
        user_count = User.query.count()
        incident_count = Incident.query.count()
        
        print(f"👥 Users: {user_count}")
        print(f"🎫 Incidents: {incident_count}")
        
        # Check for orphaned incidents
        orphaned_incidents = Incident.query.filter(~Incident.reporter_id.in_(
            db.session.query(User.id)
        )).count()
        
        if orphaned_incidents > 0:
            print(f"⚠️  Found {orphaned_incidents} orphaned incidents (reporter not found)")
        else:
            print("✅ No orphaned incidents found")
        
        print("🎉 Database health check completed!")
        
    except Exception as e:
        print(f'❌ Database health check failed: {e}')


@click.command()
@with_appcontext
def help_commands():
    """Show all available CLI commands with descriptions."""
    print("🔧 Flask CLI Commands for Incident Management System")
    print("=" * 60)
    
    print("\n🗄️  Database Commands:")
    commands = [
        ("init-db", "Initialize the database with tables"),
        ("reset-db", "Reset database (drop and recreate all tables)"),
        ("setup-db", "Complete setup with tables and default admin"),
        ("migrate-db", "Migrate database schema to latest version"),
        ("check-db", "Check database health and connectivity"),
        ("backup-db", "Create a backup of the database"),
    ]
    
    for cmd, desc in commands:
        print(f"  flask {cmd:<15} - {desc}")
    
    print("\n👥 User Commands:")
    user_commands = [
        ("create-admin", "Create an admin user interactively"),
        ("list-users", "List all users in the database"),
    ]
    
    for cmd, desc in user_commands:
        print(f"  flask {cmd:<15} - {desc}")
    
    print("\n📊 Data Commands:")
    data_commands = [
        ("seed-data", "Seed database with sample incidents"),
        ("db-stats", "Show database statistics"),
    ]
    
    for cmd, desc in data_commands:
        print(f"  flask {cmd:<15} - {desc}")
    
    print("\n💡 Examples:")
    print("  flask setup-db                 # Quick setup for new installation")
    print("  flask create-admin             # Create admin user")
    print("  flask seed-data --count 20     # Create 20 sample incidents")
    print("  flask db-stats                 # Show database statistics")
    print("  flask check-db                 # Check database health")
    
    print("\n📖 For more info on a command: flask COMMAND --help")


def register_commands(app):
    """Register CLI commands with the Flask app."""
    # Database commands
    app.cli.add_command(init_db)
    
    # Temporarily disabled for debugging
    # app.cli.add_command(reset_db)
    # app.cli.add_command(setup_db)
    # app.cli.add_command(migrate_db)
    # app.cli.add_command(check_db)
    # app.cli.add_command(backup_db)
    
    # User management commands - temporarily disabled
    # app.cli.add_command(create_admin)
    # app.cli.add_command(list_users)
    
    # Data commands - temporarily disabled
    # app.cli.add_command(seed_data)
    # app.cli.add_command(db_stats)
    
    # Help command - temporarily disabled
    # app.cli.add_command(help_commands)
