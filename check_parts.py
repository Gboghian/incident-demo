#!/usr/bin/env python3
"""
Simple test script to verify parts are in the database.
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from extensions import db
from models import Part

def test_parts_in_database():
    """Test that parts are properly stored in database."""
    app = create_app()
    
    with app.app_context():
        print("🔍 Checking parts in database...")
        
        all_parts = Part.query.all()
        print(f"Total parts in database: {len(all_parts)}")
        
        if all_parts:
            print("\nAll parts:")
            for part in all_parts:
                print(f"   - ID: {part.id}, Number: {part.part_number}, Name: {part.name}, Category: {part.category}")
        
        # Test the direct syntax used in forms
        choices = [(p.id, p.name) for p in Part.query.all()]
        print(f"\nDirect syntax choices: {len(choices)} items")
        
        if choices:
            print("Choices for form dropdown:")
            for choice in choices:
                print(f"   - Value: {choice[0]}, Display: {choice[1]}")
        
        return len(all_parts)

if __name__ == "__main__":
    count = test_parts_in_database()
    print(f"\n✅ Found {count} parts ready for use in forms!")
    if count > 0:
        print("\n💡 You can now test the incident form at: http://127.0.0.1:5000/incident/new")
