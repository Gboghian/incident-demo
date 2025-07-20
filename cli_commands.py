"""
Flask CLI commands for the Incident Management System.
"""

import click
from flask import current_app
from flask.cli import with_appcontext
from extensions import db
from models import User, Incident


@click.command()
@with_appcontext
def init_db():
    """Initialize the database."""
    db.create_all()
    click.echo('Database tables created successfully!')


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
    """Create an admin user."""
    username = click.prompt('Admin username', default='admin')
    email = click.prompt('Admin email', default='admin@example.com')
    password = click.prompt('Admin password', hide_input=True, confirmation_prompt=True)
    
    # Check if user exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        click.echo(f'User {username} already exists!')
        return
    
    # Create admin user
    admin = User(
        username=username,
        email=email,
        first_name='System',
        last_name='Administrator',
        role='admin'
    )
    admin.set_password(password)
    
    db.session.add(admin)
    db.session.commit()
    
    click.echo(f'Admin user {username} created successfully!')


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


def register_commands(app):
    """Register CLI commands with the Flask app."""
    app.cli.add_command(init_db)
    app.cli.add_command(list_routes)
    app.cli.add_command(create_admin)
    app.cli.add_command(stats)
