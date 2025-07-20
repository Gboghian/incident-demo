#!/usr/bin/env python3
"""
Create or update demo user for testing purposes.
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from extensions import db
from models import User

def create_demo_user():
    """Create or update the demo user."""
    app = create_app()
    
    with app.app_context():
        print("🎭 Setting up demo user...")
        
        # Check if demo user exists
        demo_user = User.query.filter_by(username='demo_user').first()
        
        if demo_user:
            print(f"✅ Demo user already exists: {demo_user.username}")
            print(f"   Name: {demo_user.first_name} {demo_user.last_name}")
            print(f"   Email: {demo_user.email}")
            print(f"   Department: {demo_user.department}")
            return demo_user
        
        # Create new demo user
        demo_user = User(
            username='demo_user',
            email='demo@incidentmanagement.com',
            first_name='Demo',
            last_name='User',
            department='Engineering',
            role_level='Senior Engineer',
            role='user',
            notifications_enabled=True
        )
        demo_user.set_password('demo123')  # Simple password for demo
        
        db.session.add(demo_user)
        db.session.commit()
        
        print("✅ Created new demo user:")
        print(f"   Username: {demo_user.username}")
        print(f"   Password: demo123")
        print(f"   Name: {demo_user.first_name} {demo_user.last_name}")
        print(f"   Email: {demo_user.email}")
        print(f"   Department: {demo_user.department}")
        
        return demo_user

def update_existing_demo_setup():
    """Update existing test_user to be more demo-friendly."""
    app = create_app()
    
    with app.app_context():
        # Update the test_user to have better demo info
        test_user = User.query.filter_by(username='test_user').first()
        if test_user:
            test_user.first_name = 'Demo'
            test_user.last_name = 'Engineer'
            test_user.department = 'Engineering'
            test_user.role_level = 'Senior Engineer'
            test_user.email = 'demo.engineer@company.com'
            db.session.commit()
            
            print("✅ Updated test_user for better demo experience:")
            print(f"   Username: {test_user.username}")
            print(f"   Name: {test_user.first_name} {test_user.last_name}")
            print(f"   Department: {test_user.department}")
            print(f"   Email: {test_user.email}")

if __name__ == "__main__":
    print("🚀 Demo User Setup")
    print("=" * 40)
    
    # Create dedicated demo user
    demo_user = create_demo_user()
    
    # Update existing test user for better demo
    update_existing_demo_setup()
    
    print("\n💡 Demo Login Options:")
    print("   1. Visit: http://127.0.0.1:5000/demo-login")
    print("   2. Automatic login as demo user")
    print("   3. Redirects to dashboard after login")
    print("\n🔑 Manual Login Credentials:")
    print("   Username: demo_user")
    print("   Password: demo123")
    print("   OR")
    print("   Username: test_user")
    print("   Password: test123")
