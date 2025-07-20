"""
Flask CLI commands for the Incident Management System.
"""

import click
from flask import current_app
from flask.cli import with_appcontext
from extensions import db
from models import User, Incident
from datetime import datetime
import os


@click.command()
@with_appcontext
def init_db():
    """Initialize the database with tables."""
    try:
        print("🚀 Starting database initialization...")
        
        # Create database directory if it doesn't exist
        db_dir = os.path.dirname(current_app.config.get('SQLALCHEMY_DATABASE_URI', '').replace('sqlite:///', ''))
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


@click.command()
@with_appcontext
def reset_db():
    """Reset the database (drop and recreate all tables)."""
    if click.confirm('⚠️  This will delete ALL data. Are you sure?'):
        try:
            print("🗑️  Dropping all existing tables...")
            db.drop_all()
            print('✅ Dropped all tables')
            
            print("🔧 Recreating database tables...")
            db.create_all()
            print('✅ Database reset successfully!')
            
            # Show recreated tables
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            print(f'📋 Recreated tables: {", ".join(tables)}')
            
        except Exception as e:
            print(f'❌ Error resetting database: {e}')
    else:
        print("❌ Database reset cancelled.")


@click.command()
@click.option('--username', prompt='Admin username', help='Username for admin account')
@click.option('--email', prompt='Admin email', help='Email for admin account')
@click.option('--password', prompt='Admin password', hide_input=True, confirmation_prompt=True, help='Password for admin account')
@click.option('--first-name', prompt='First name', help='Admin first name')
@click.option('--last-name', prompt='Last name', help='Admin last name')
@with_appcontext
def create_admin(username, email, password, first_name, last_name):
    """Create an admin user."""
    try:
        print(f"� Creating admin user: {username}")
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            print(f'❌ User with username "{username}" already exists!')
            return
        
        if User.query.filter_by(email=email).first():
            print(f'❌ User with email "{email}" already exists!')
            return
        
        print("🔧 Creating user record...")
        admin_user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            department='IT',
            role_level='manager',
            role='admin',
            notifications_enabled=True
        )
        admin_user.set_password(password)
        
        print("💾 Saving to database...")
        db.session.add(admin_user)
        db.session.commit()
        
        print('✅ Admin user created successfully!')
        print(f'👤 Username: {username}')
        print(f'📧 Email: {email}')
        print(f'🔐 Role: admin')
        
    except Exception as e:
        print(f'❌ Error creating admin user: {e}')
        db.session.rollback()


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
            import random
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
            print(f"\n🏢 Departments:")
            departments = db.session.query(User.department, db.func.count(User.id)).group_by(User.department).all()
            for dept, count in departments:
                dept_name = dept or "Not specified"
                print(f"   {dept_name}: {count}")
        
        # Incident statistics
        total_incidents = Incident.query.count()
        open_incidents = Incident.query.filter_by(status='open').count()
        in_progress = Incident.query.filter_by(status='in_progress').count()
        resolved = Incident.query.filter(Incident.status.in_(['resolved', 'closed'])).count()
        
        print(f"\n🎫 Incidents:")
        print(f"   Total: {total_incidents}")
        print(f"   Open: {open_incidents}")
        print(f"   In Progress: {in_progress}")
        print(f"   Resolved: {resolved}")
        
        # Severity breakdown
        if total_incidents > 0:
            print(f"\n⚠️  Severity breakdown:")
            severities = db.session.query(Incident.severity, db.func.count(Incident.id)).group_by(Incident.severity).all()
            for severity, count in severities:
                print(f"   {severity.title()}: {count}")
        
        # Recent activity
        recent_incidents = Incident.query.order_by(Incident.created_at.desc()).limit(5).all()
        if recent_incidents:
            print(f"\n🕒 Recent incidents:")
            for incident in recent_incidents:
                print(f"   #{incident.id}: {incident.title[:50]}{'...' if len(incident.title) > 50 else ''}")
        
    except Exception as e:
        print(f'❌ Error getting database statistics: {e}')


@click.command()
@with_appcontext
def list_users():
    """List all users in the database."""
    try:
        users = User.query.all()
        
        if not users:
            print("👥 No users found in database.")
            return
        
        print(f"👥 Found {len(users)} users:")
        print("=" * 80)
        print(f"{'ID':<4} {'Username':<20} {'Email':<30} {'Role':<10} {'Department':<15}")
        print("-" * 80)
        
        for user in users:
            print(f"{user.id:<4} {user.username:<20} {user.email:<30} {user.role:<10} {user.department or 'N/A':<15}")
            
    except Exception as e:
        print(f'❌ Error listing users: {e}')


@click.command()
@with_appcontext
def backup_db():
    """Create a backup of the database."""
    try:
        from shutil import copy2
        import time
        
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
        
        print(f"💾 Creating database backup...")
        print(f"📁 Source: {db_path}")
        print(f"📁 Backup: {backup_path}")
        
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
        print("� Starting database migration...")
        
        # Check if migration is needed
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        
        if 'users' not in tables:
            print("❌ Users table not found. Run 'flask init-db' first.")
            return
        
        # Check existing columns
        user_columns = [col['name'] for col in inspector.get_columns('users')]
        print(f"📋 Current user table columns: {', '.join(user_columns)}")
        
        new_columns_added = 0
        
        # Add missing columns
        if 'department' not in user_columns:
            print("🔧 Adding 'department' column...")
            db.engine.execute('ALTER TABLE users ADD COLUMN department VARCHAR(50)')
            new_columns_added += 1
        
        if 'role_level' not in user_columns:
            print("🔧 Adding 'role_level' column...")
            db.engine.execute('ALTER TABLE users ADD COLUMN role_level VARCHAR(30)')
            new_columns_added += 1
        
        if 'notifications_enabled' not in user_columns:
            print("🔧 Adding 'notifications_enabled' column...")
            db.engine.execute('ALTER TABLE users ADD COLUMN notifications_enabled BOOLEAN DEFAULT 1')
            new_columns_added += 1
        
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
def help_commands():
    """Show all available CLI commands with descriptions."""
    print("🔧 Flask CLI Commands for Incident Management System")
    print("=" * 60)
    
    commands = [
        ("init-db", "Initialize the database with tables"),
        ("reset-db", "Reset database (drop and recreate all tables)"),
        ("create-admin", "Create an admin user interactively"),
        ("seed-data", "Seed database with sample incidents"),
        ("db-stats", "Show database statistics"),
        ("list-users", "List all users in the database"),
        ("backup-db", "Create a backup of the database"),
        ("migrate-db", "Migrate database schema to latest version"),
        ("help-commands", "Show this help message")
    ]
    
    for cmd, desc in commands:
        print(f"  flask {cmd:<15} - {desc}")
    
    print("\n💡 Examples:")
    print("  flask init-db                  # Initialize database")
    print("  flask create-admin             # Create admin user")
    print("  flask seed-data --count 20     # Create 20 sample incidents")
    print("  flask db-stats                 # Show database statistics")
    print("\n📖 For more info on a command: flask COMMAND --help")
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            click.echo(f'📋 Recreated tables: {", ".join(tables)}')
            
        except Exception as e:
            click.echo(f'❌ Error resetting database: {e}')
    else:
        click.echo('Database reset cancelled.')


@click.command()
@with_appcontext
def setup_db():
    """Complete database setup with tables and default data."""
    try:
        # Initialize database
        click.echo('🔧 Setting up database...')
        
        # Create database directory if needed
        db_dir = os.path.dirname(current_app.config.get('SQLALCHEMY_DATABASE_URI', '').replace('sqlite:///', ''))
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
            click.echo(f'📁 Created database directory: {db_dir}')
        
        # Create tables
        db.create_all()
        click.echo('✅ Database tables created')
        
        # Check if admin user exists
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
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
            
            # Create sample engineer user
            engineer_user = User(
                username='engineer1',
                email='engineer@company.com',
                first_name='John',
                last_name='Engineer',
                department='software',
                role_level='senior',
                role='user',
                notifications_enabled=True
            )
            engineer_user.set_password('engineer123')
            db.session.add(engineer_user)
            
            db.session.commit()
            click.echo('👤 Created default users:')
            click.echo('   - admin/admin123 (Administrator)')
            click.echo('   - engineer1/engineer123 (Senior Software Engineer)')
        else:
            click.echo('👤 Admin user already exists')
        
        # Create sample incident if none exist
        incident_count = Incident.query.count()
        if incident_count == 0:
            sample_incident = Incident(
                title='Sample Incident - Server Performance Issue',
                description='This is a sample incident to demonstrate the system functionality. The main application server is experiencing high CPU usage during peak hours.',
                severity='high',
                category='infrastructure',
                location='Data Center A - Server Room 1',
                status='open',
                reporter_id=admin_user.id,
                created_at=datetime.utcnow()
            )
            db.session.add(sample_incident)
            db.session.commit()
            click.echo('📋 Created sample incident')
        
        click.echo('🎉 Database setup completed successfully!')
        click.echo('\n📊 System Status:')
        click.echo(f'   Users: {User.query.count()}')
        click.echo(f'   Incidents: {Incident.query.count()}')
        
    except Exception as e:
        click.echo(f'❌ Error setting up database: {e}')


@click.command()
@with_appcontext
def check_db():
    """Check database status and show information."""
    try:
        # Check if database file exists
        db_uri = current_app.config.get('SQLALCHEMY_DATABASE_URI', '')
        if 'sqlite:///' in db_uri:
            db_path = db_uri.replace('sqlite:///', '')
            if os.path.exists(db_path):
                db_size = os.path.getsize(db_path)
                click.echo(f'📁 Database file: {db_path} ({db_size} bytes)')
            else:
                click.echo(f'❌ Database file not found: {db_path}')
                return
        
        # Check tables
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        
        if tables:
            click.echo(f'📋 Tables: {", ".join(tables)}')
            
            # Check each table
            for table in tables:
                columns = inspector.get_columns(table)
                column_names = [col['name'] for col in columns]
                click.echo(f'   {table}: {len(column_names)} columns ({", ".join(column_names)})')
        else:
            click.echo('❌ No tables found in database')
            return
        
        # Check data
        user_count = User.query.count()
        incident_count = Incident.query.count()
        
        click.echo(f'\n📊 Data Summary:')
        click.echo(f'   Users: {user_count}')
        click.echo(f'   Incidents: {incident_count}')
        
        if user_count > 0:
            admin_count = User.query.filter_by(role='admin').count()
            click.echo(f'   Administrators: {admin_count}')
        
        if incident_count > 0:
            open_count = Incident.query.filter_by(status='open').count()
            resolved_count = Incident.query.filter(Incident.status.in_(['resolved', 'closed'])).count()
            click.echo(f'   Open incidents: {open_count}')
            click.echo(f'   Resolved incidents: {resolved_count}')
        
        click.echo('✅ Database check completed')
        
    except Exception as e:
        click.echo(f'❌ Error checking database: {e}')


@click.command()
@with_appcontext
def list_routes():
    """List all available routes."""
    output = []
    for rule in current_app.url_map.iter_rules():
        methods = ','.join(sorted(rule.methods))
        url = str(rule)
        line = "{:50s} {:20s} {}".format(rule.endpoint, methods, url)
        output.append(line)
    
    click.echo('=== Available Routes ===')
    for line in sorted(output):
        click.echo(line)


@click.command()
@with_appcontext
def create_admin():
    """Create an admin user interactively."""
    click.echo('🔧 Creating Admin User')
    
    username = click.prompt('Admin username', default='admin')
    email = click.prompt('Admin email', default='admin@company.com')
    first_name = click.prompt('First name', default='System')
    last_name = click.prompt('Last name', default='Administrator')
    password = click.prompt('Admin password', hide_input=True, confirmation_prompt=True)
    
    # Check if user exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        click.echo(f'❌ User {username} already exists!')
        return
    
    existing_email = User.query.filter_by(email=email).first()
    if existing_email:
        click.echo(f'❌ Email {email} already registered!')
        return
    
    try:
        # Create admin user
        admin = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            department='IT',
            role_level='manager',
            role='admin',
            notifications_enabled=True
        )
        admin.set_password(password)
        
        db.session.add(admin)
        db.session.commit()
        
        click.echo(f'✅ Admin user {username} created successfully!')
        click.echo(f'   Email: {email}')
        click.echo(f'   Name: {first_name} {last_name}')
        click.echo(f'   Role: Administrator')
        
    except Exception as e:
        click.echo(f'❌ Error creating admin user: {e}')


@click.command()
@with_appcontext
def create_user():
    """Create a regular user interactively."""
    click.echo('👤 Creating User')
    
    username = click.prompt('Username')
    email = click.prompt('Email')
    first_name = click.prompt('First name')
    last_name = click.prompt('Last name')
    
    # Department selection
    departments = [
        'software', 'hardware', 'qa', 'devops', 
        'security', 'data', 'research', 'support', 'other'
    ]
    click.echo('Available departments:')
    for i, dept in enumerate(departments, 1):
        click.echo(f'  {i}. {dept.title()}')
    
    dept_choice = click.prompt('Select department (number)', type=int)
    if 1 <= dept_choice <= len(departments):
        department = departments[dept_choice - 1]
    else:
        department = 'other'
    
    # Role level selection
    roles = ['junior', 'engineer', 'senior', 'lead', 'manager', 'director']
    click.echo('Available role levels:')
    for i, role in enumerate(roles, 1):
        click.echo(f'  {i}. {role.title()}')
    
    role_choice = click.prompt('Select role level (number)', type=int)
    if 1 <= role_choice <= len(roles):
        role_level = roles[role_choice - 1]
    else:
        role_level = 'engineer'
    
    password = click.prompt('Password', hide_input=True, confirmation_prompt=True)
    
    # Check if user exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        click.echo(f'❌ User {username} already exists!')
        return
    
    existing_email = User.query.filter_by(email=email).first()
    if existing_email:
        click.echo(f'❌ Email {email} already registered!')
        return
    
    try:
        # Create user
        user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            department=department,
            role_level=role_level,
            role='user',
            notifications_enabled=True
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        click.echo(f'✅ User {username} created successfully!')
        click.echo(f'   Email: {email}')
        click.echo(f'   Name: {first_name} {last_name}')
        click.echo(f'   Department: {department.title()}')
        click.echo(f'   Role Level: {role_level.title()}')
        
    except Exception as e:
        click.echo(f'❌ Error creating user: {e}')


@click.command()
@with_appcontext
def stats():
    """Show system statistics."""
    total_users = User.query.count()
    total_incidents = Incident.query.count()
    open_incidents = Incident.query.filter_by(status='open').count()
    resolved_incidents = Incident.query.filter(
        Incident.status.in_(['resolved', 'closed'])
    ).count()
    
    click.echo('=== System Statistics ===')
    click.echo(f'Total Users: {total_users}')
    click.echo(f'Total Incidents: {total_incidents}')
    click.echo(f'Open Incidents: {open_incidents}')
    click.echo(f'Resolved Incidents: {resolved_incidents}')


@click.command()
@with_appcontext
def help_commands():
    """Show help for all available CLI commands."""
    click.echo('🔧 Incident Management System - CLI Commands')
    click.echo('=' * 50)
    
    click.echo('\n📊 Database Commands:')
    click.echo('  flask init-db        - Initialize database tables')
    click.echo('  flask setup-db       - Complete database setup with default data')
    click.echo('  flask reset-db       - Reset database (drop and recreate)')
    click.echo('  flask check-db       - Check database status and information')
    
    click.echo('\n👤 User Management Commands:')
    click.echo('  flask create-admin   - Create an admin user interactively')
    click.echo('  flask create-user    - Create a regular user interactively')
    
    click.echo('\n🔍 Utility Commands:')
    click.echo('  flask list-routes    - List all available routes')
    click.echo('  flask stats          - Show system statistics')
    click.echo('  flask help-commands  - Show this help message')
    
    click.echo('\n📖 Usage Examples:')
    click.echo('  flask setup-db                    # Quick setup with defaults')
    click.echo('  flask create-admin                # Create admin user')
    click.echo('  flask stats                       # View system stats')
    click.echo('  flask check-db                    # Check database health')
    
    click.echo('\n🚀 Quick Start:')
    click.echo('  1. flask setup-db                 # Setup database and defaults')
    click.echo('  2. flask run                      # Start the application')
    click.echo('  3. Open http://127.0.0.1:5000    # Access the web interface')


def register_commands(app):
    """Register CLI commands with the Flask app."""
    # Database commands
    app.cli.add_command(init_db)
    app.cli.add_command(reset_db)
    app.cli.add_command(setup_db)
    app.cli.add_command(check_db)
    
    # User management commands
    app.cli.add_command(create_admin)
    app.cli.add_command(create_user)
    
    # Utility commands
    app.cli.add_command(list_routes)
    app.cli.add_command(stats)
    app.cli.add_command(help_commands)
    app.cli.add_command(help_commands)
