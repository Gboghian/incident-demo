#!/usr/bin/env python3
"""
Test script to create a sample incident with parts and verify the functionality.
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from extensions import db
from models import Part, Incident, User
from datetime import datetime

def create_test_incident_with_parts():
    """Create a test incident with parts to verify the functionality."""
    app = create_app()
    
    with app.app_context():
        print("🧪 Creating Test Incident with Parts")
        print("=" * 50)
        
        # Get or create a test user
        test_user = User.query.first()
        if not test_user:
            print("❌ No users found. Please create a user first.")
            return
        
        print(f"👤 Using test user: {test_user.username}")
        
        # Get some parts to associate
        parts_to_use = Part.query.limit(3).all()
        if not parts_to_use:
            print("❌ No parts found. Please add parts to the database first.")
            return
        
        print(f"🔧 Selected parts for test incident:")
        for part in parts_to_use:
            print(f"   - {part.part_number}: {part.name}")
        
        # Create test incident
        test_incident = Incident(
            title="Test Equipment Malfunction - Multi-Part Repair",
            description="This is a test incident created to demonstrate the multi-select parts functionality. The conveyor belt system experienced multiple component failures requiring several replacement parts.",
            equipment="Conveyor System #3",
            location="Production Floor A - Zone 2",
            severity='high',
            category='mechanical',
            priority='high',
            status='open',
            reporter_id=test_user.id,
            date_reported=datetime.utcnow()
        )
        
        # Add to database to get ID
        db.session.add(test_incident)
        db.session.flush()  # Get the ID without committing
        
        # Associate parts with incident
        for part in parts_to_use:
            test_incident.parts.append(part)
        
        # Commit all changes
        db.session.commit()
        
        print(f"\n✅ Created test incident #{test_incident.id}")
        print(f"   Title: {test_incident.title}")
        print(f"   Parts associated: {len(parts_to_use)}")
        
        # Verify the relationship works
        print(f"\n🔍 Verifying parts relationship:")
        incident_parts = test_incident.parts.all()
        print(f"   Parts from incident: {len(incident_parts)}")
        for part in incident_parts:
            print(f"   - {part.part_number}: {part.name}")
        
        print(f"\n🌐 You can view this incident at:")
        print(f"   http://127.0.0.1:5000/incident/{test_incident.id}")
        
        return test_incident.id

if __name__ == "__main__":
    incident_id = create_test_incident_with_parts()
    if incident_id:
        print(f"\n💡 Test completed successfully!")
        print(f"   Navigate to http://127.0.0.1:5000/incident/{incident_id} to see the result")
