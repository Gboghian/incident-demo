#!/usr/bin/env python3
"""
Demonstration of form.parts.choices = [(p.id, p.name) for p in Part.query.all()]
This script shows how to dynamically populate form choices with parts from the database.
"""

import sys, os
sys.path.insert(0, os.getcwd())

def demonstrate_parts_choices():
    """Demonstrate the direct syntax for populating form choices."""
    
    from app import app
    from forms import IncidentForm, EnhancedIncidentForm
    from models import Part
    
    with app.app_context():
        with app.test_request_context():
            print("🔧 Demonstrating: form.parts.choices = [(p.id, p.name) for p in Part.query.all()]\n")
            
            # Method 1: Direct assignment in form initialization
            print("1️⃣  Method 1: Direct assignment")
            form = IncidentForm()
            form.parts.choices = [(p.id, p.name) for p in Part.query.all()]
            print(f"   ✅ Populated {len(form.parts.choices)} choices")
            if form.parts.choices:
                print(f"   📋 Example: {form.parts.choices[0]}")
            
            # Method 2: In a route or view function
            print("\n2️⃣  Method 2: In a route/view function")
            print("   Code example:")
            print("   ```python")
            print("   @app.route('/incident/new', methods=['GET', 'POST'])")
            print("   def new_incident():")
            print("       form = IncidentForm()")
            print("       form.parts.choices = [(p.id, p.name) for p in Part.query.all()]")
            print("       # ... rest of route logic")
            print("   ```")
            
            # Method 3: Multiple fields at once
            print("\n3️⃣  Method 3: Multiple fields at once")
            enhanced_form = EnhancedIncidentForm()
            parts_choices = [(p.id, p.name) for p in Part.query.all()]
            enhanced_form.parts_checkbox.choices = parts_choices
            enhanced_form.parts_select.choices = parts_choices
            print(f"   ✅ Populated checkbox field: {len(enhanced_form.parts_checkbox.choices)} choices")
            print(f"   ✅ Populated select field: {len(enhanced_form.parts_select.choices)} choices")
            
            # Method 4: With filtering
            print("\n4️⃣  Method 4: With filtering (active parts only)")
            active_parts = [(p.id, p.name) for p in Part.query.filter_by(status='active').all()]
            form.parts.choices = active_parts
            print(f"   ✅ Filtered to active parts: {len(active_parts)} choices")
            
            # Method 5: With ordering
            print("\n5️⃣  Method 5: With ordering")
            ordered_parts = [(p.id, p.name) for p in Part.query.order_by(Part.name).all()]
            form.parts.choices = ordered_parts
            print(f"   ✅ Ordered by name: {len(ordered_parts)} choices")
            if ordered_parts:
                print(f"   📋 First item: {ordered_parts[0]}")
                print(f"   📋 Last item: {ordered_parts[-1]}")
            
            # Method 6: With custom display format
            print("\n6️⃣  Method 6: Custom display format")
            custom_format = [(p.id, f"{p.part_number} - {p.name}") for p in Part.query.all()]
            form.parts.choices = custom_format
            print(f"   ✅ Custom format: {len(custom_format)} choices")
            if custom_format:
                print(f"   📋 Example: {custom_format[0]}")
            
            print("\n🎉 All methods demonstrated successfully!")
            print("\n💡 Key points:")
            print("   - Choice format: (value, display_text)")
            print("   - Value (p.id) is what gets submitted")
            print("   - Display text (p.name) is what user sees")
            print("   - Can be customized with filters, ordering, formatting")

if __name__ == "__main__":
    try:
        demonstrate_parts_choices()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
