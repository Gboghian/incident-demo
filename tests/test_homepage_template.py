"""
Test for the basic homepage template.
"""

import pytest
from extensions import create_app


def test_homepage_template_content():
    """Test that the homepage template renders correctly."""
    app = create_app('testing')
    
    with app.test_client() as client:
        # Test the home route
        response = client.get('/')
        
        # Check that the response is successful
        assert response.status_code == 200
        
        # Check for key homepage content
        assert b'Incident Management System' in response.data
        assert b'Streamline your incident reporting' in response.data
        assert b'Why Choose Our System?' in response.data
        assert b'How It Works' in response.data
        assert b'Ready to Get Started?' in response.data
        
        # Check for feature sections
        assert b'Quick Reporting' in response.data
        assert b'Track Progress' in response.data
        assert b'Analytics' in response.data
        
        # Check for step numbers
        assert b'Create Account' in response.data
        assert b'Report Incident' in response.data
        assert b'Resolve & Close' in response.data


def test_homepage_unauthenticated_content():
    """Test homepage content for unauthenticated users."""
    app = create_app('testing')
    
    with app.test_client() as client:
        response = client.get('/')
        
        # Should contain login/register buttons
        assert b'Login' in response.data
        assert b'Get Started' in response.data
        assert b'Start Free Today' in response.data
        
        # Should NOT contain stats section
        assert b'System Overview' not in response.data


def test_homepage_authenticated_content():
    """Test homepage content for authenticated users."""
    app = create_app('testing')
    
    with app.app_context():
        from extensions import db
        from models import User
        
        # Create test user
        db.create_all()
        user = User(
            username='testuser',
            email='test@example.com',
            first_name='Test',
            last_name='User'
        )
        user.set_password('password')
        db.session.add(user)
        db.session.commit()
        
        with app.test_client() as client:
            # Login the user
            client.post('/auth/login', data={
                'username': 'testuser',
                'password': 'password'
            })
            
            response = client.get('/')
            
            # Should contain dashboard/incident buttons
            assert b'Go to Dashboard' in response.data
            assert b'Report Incident' in response.data
            
            # Should contain stats section
            assert b'System Overview' in response.data
