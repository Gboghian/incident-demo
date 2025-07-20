#!/usr/bin/env python3
"""
Check existing users in the database.
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from extensions import db
from models import User

def check_users():
    """Check existing users in database."""
    app = create_app()
    
    with app.app_context():
        print("🔍 Checking existing users in database...")
        
        users = User.query.all()
        print(f"Total users: {len(users)}")
        
        if users:
            print("\nExisting users:")
            for user in users:
                print(f"   - ID: {user.id}, Username: {user.username}, Email: {user.email}, Role: {user.role}")
        else:
            print("No users found in database.")
            
        return users

if __name__ == "__main__":
    check_users()
