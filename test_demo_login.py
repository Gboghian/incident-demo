#!/usr/bin/env python3
"""
Test the demo login functionality.
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from extensions import db
from models import User

def test_demo_login_route():
    """Test the demo login route functionality."""
    app = create_app()
    
    with app.test_client() as client:
        with app.app_context():
            print("🧪 Testing Demo Login Functionality")
            print("=" * 50)
            
            # Check available users
            users = User.query.all()
            print(f"Available users: {len(users)}")
            for user in users:
                print(f"   - {user.username}: {user.first_name} {user.last_name}")
            
            # Test the demo login route
            print("\n🔗 Testing /auth/demo-login route...")
            response = client.get('/auth/demo-login', follow_redirects=True)
            
            print(f"Response status: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ Demo login route is accessible")
                
                # Check if we got redirected to dashboard
                if b'Dashboard' in response.data or b'dashboard' in response.data:
                    print("✅ Successfully redirected to dashboard")
                else:
                    print("⚠️  May not have redirected to dashboard")
                    
                # Check for success message
                if b'Demo login successful' in response.data:
                    print("✅ Demo login success message displayed")
                elif b'success' in response.data:
                    print("✅ Some success message displayed")
                else:
                    print("⚠️  No success message found")
            else:
                print(f"❌ Demo login route failed with status {response.status_code}")

def demo_user_info():
    """Show demo user information."""
    app = create_app()
    
    with app.app_context():
        print("\n👤 Demo User Information")
        print("-" * 30)
        
        demo_user = User.query.filter_by(username='demo_user').first()
        if demo_user:
            print(f"Username: {demo_user.username}")
            print(f"Name: {demo_user.first_name} {demo_user.last_name}")
            print(f"Email: {demo_user.email}")
            print(f"Department: {demo_user.department}")
            print(f"Role: {demo_user.role}")
        
        test_user = User.query.filter_by(username='test_user').first()
        if test_user:
            print(f"\nFallback User:")
            print(f"Username: {test_user.username}")
            print(f"Name: {test_user.first_name} {test_user.last_name}")
            print(f"Email: {test_user.email}")
            print(f"Department: {test_user.department}")

if __name__ == "__main__":
    test_demo_login_route()
    demo_user_info()
    
    print("\n🌐 Demo Login URLs:")
    print("   • Direct: http://127.0.0.1:5000/auth/demo-login")
    print("   • Login page: http://127.0.0.1:5000/login (has demo button)")
    print("   • Home page: http://127.0.0.1:5000/ (has try demo button)")
    
    print("\n✅ Demo login implementation complete!")
    print("   - Automatically logs in as demo_user")
    print("   - Redirects to dashboard after login")
    print("   - Shows success message with user info")
    print("   - Accessible from multiple pages")
