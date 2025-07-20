"""
Test for the main Blueprint setup and home route.
"""

import pytest
from extensions import create_app


def test_main_blueprint_home_route():
    """Test that the main blueprint home route returns index.html."""
    app = create_app('testing')
    
    with app.test_client() as client:
        # Test the home route
        response = client.get('/')
        
        # Check that the response is successful
        assert response.status_code == 200
        
        # Check that the response contains content from index.html
        assert b'Incident Management System' in response.data
        assert b'streamline their operations' in response.data
        assert b'Login' in response.data
        assert b'Register' in response.data


def test_main_blueprint_registration():
    """Test that the main blueprint is properly registered."""
    app = create_app('testing')
    
    # Check that the blueprint is registered
    assert 'main' in [bp.name for bp in app.blueprints.values()]
    
    # Check that the home route exists
    with app.test_request_context():
        from flask import url_for
        home_url = url_for('main.home')
        assert home_url == '/'


def test_main_blueprint_routes():
    """Test that main blueprint routes are accessible."""
    app = create_app('testing')
    
    with app.test_client() as client:
        # Test home route
        response = client.get('/')
        assert response.status_code == 200
        
        # Test that other main routes exist (should redirect for auth required)
        response = client.get('/dashboard')
        assert response.status_code in [200, 302]  # 302 if auth required
