"""
Basic tests for the Incident Management System.
"""

import pytest
from extensions import create_app, db
from models import User, Incident


@pytest.fixture
def app():
    """Create application for testing."""
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create test runner."""
    return app.test_cli_runner()


def test_app_creation(app):
    """Test that the app is created properly."""
    assert app is not None
    assert app.config['TESTING'] is True


def test_index_page(client):
    """Test the index page loads."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Incident Management System' in response.data


def test_login_page(client):
    """Test the login page loads."""
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert b'Login' in response.data


def test_register_page(client):
    """Test the register page loads."""
    response = client.get('/auth/register')
    assert response.status_code == 200
    assert b'Register' in response.data


def test_user_creation():
    """Test user model creation."""
    user = User(
        username='testuser',
        email='test@example.com',
        first_name='Test',
        last_name='User'
    )
    user.set_password('testpassword')
    
    assert user.username == 'testuser'
    assert user.check_password('testpassword')
    assert not user.check_password('wrongpassword')


def test_incident_creation():
    """Test incident model creation."""
    incident = Incident(
        title='Test Incident',
        description='This is a test incident',
        severity='medium',
        category='Testing',
        reporter_id=1,
        status='open'  # Explicitly set status for testing
    )
    
    assert incident.title == 'Test Incident'
    assert incident.severity == 'medium'
    assert incident.status == 'open'
