#!/usr/bin/env python3
"""
Test script to verify parts dropdown functionality in incident report forms.
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from extensions import db
from models import Part, Incident, User
from forms import IncidentForm

def add_sample_parts():
    """Add sample parts to the database for testing."""
    sample_parts = [
        {
            'part_number': 'BELT-001',
            'name': 'Conveyor Belt - Standard',
            'description': 'Standard conveyor belt for production line',
            'category': 'mechanical',
            'unit_cost': 150.00,
            'current_stock': 5
        },
        {
            'part_number': 'MOTOR-001',
            'name': 'Electric Motor 5HP',
            'description': '5 horsepower electric motor for conveyor systems',
            'category': 'electrical',
            'unit_cost': 450.00,
            'current_stock': 2
        },
        {
            'part_number': 'BEARING-001',
            'name': 'Ball Bearing Set',
            'description': 'Ball bearing set for rotating equipment',
            'category': 'mechanical',
            'unit_cost': 75.00,
            'current_stock': 10
        },
        {
            'part_number': 'SENSOR-001',
            'name': 'Proximity Sensor',
            'description': 'Inductive proximity sensor for position detection',
            'category': 'electronic',
            'unit_cost': 25.00,
            'current_stock': 15
        },
        {
            'part_number': 'VALVE-001',
            'name': 'Pneumatic Valve',
            'description': 'Pneumatic control valve for air systems',
            'category': 'pneumatic',
            'unit_cost': 120.00,
            'current_stock': 8
        }
    ]
    
    parts_added = 0
    for part_data in sample_parts:
        # Check if part already exists
        existing_part = Part.query.filter_by(part_number=part_data['part_number']).first()
        if not existing_part:
            part = Part(**part_data)
            db.session.add(part)
            parts_added += 1
            print(f"✅ Added part: {part_data['part_number']} - {part_data['name']}")
        else:
            print(f"⚠️  Part already exists: {part_data['part_number']}")
    
    db.session.commit()
    print(f"\n📦 Added {parts_added} new parts to the database")
    return parts_added

def test_form_parts_population():
    """Test that the IncidentForm properly populates parts choices."""
    print("\n🧪 Testing IncidentForm parts population...")
    
    form = IncidentForm()
    
    # Check that parts choices are populated
    print(f"Parts checkbox field choices: {len(form.parts.choices)} items")
    print(f"Parts dropdown field choices: {len(form.parts_dropdown.choices)} items")
    
    if form.parts.choices:
        print("✅ Parts checkbox choices populated successfully")
        for choice in form.parts.choices[:3]:  # Show first 3
            print(f"   - {choice[0]}: {choice[1]}")
    else:
        print("❌ Parts checkbox choices not populated")
    
    if form.parts_dropdown.choices:
        print("✅ Parts dropdown choices populated successfully")
        for choice in form.parts_dropdown.choices[:3]:  # Show first 3
            print(f"   - {choice[0]}: {choice[1]}")
    else:
        print("❌ Parts dropdown choices not populated")

def test_parts_query():
    """Test direct parts query."""
    print("\n🔍 Testing direct parts query...")
    
    all_parts = Part.query.all()
    print(f"Total parts in database: {len(all_parts)}")
    
    if all_parts:
        print("Sample parts:")
        for part in all_parts[:5]:  # Show first 5
            print(f"   - ID: {part.id}, Number: {part.part_number}, Name: {part.name}")
    
    # Test the direct syntax used in forms
    choices = [(p.id, p.name) for p in Part.query.all()]
    print(f"Direct syntax result: {len(choices)} choices")
    if choices:
        print("Sample choices:")
        for choice in choices[:3]:
            print(f"   - {choice}")

def main():
    """Main test function."""
    app = create_app()
    
    with app.app_context():
        print("🚀 Testing Parts Dropdown Functionality")
        print("=" * 50)
        
        # Ensure database tables exist
        db.create_all()
        
        # Add sample parts
        add_sample_parts()
        
        # Test parts query
        test_parts_query()
        
        # Test form population
        test_form_parts_population()
        
        print("\n✅ All tests completed!")
        print("\n💡 Now you can:")
        print("   1. Visit http://127.0.0.1:5000/incident/new to test the form")
        print("   2. Try both the dropdown and checkbox selection methods")
        print("   3. Submit an incident with selected parts")

if __name__ == "__main__":
    main()
