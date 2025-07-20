"""
Flask-WTF forms for the Incident Management System.
This module contains form classes for handling user input and validation.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, SelectMultipleField
from wtforms.widgets import CheckboxInput, ListWidget
from wtforms.validators import DataRequired, Length, Optional


class MultiCheckboxField(SelectMultipleField):
    """
    A multiple-select, except displays a list of checkboxes.
    
    Iterating the field will produce subfields, allowing custom rendering of
    the enclosed checkbox fields.
    """
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


def get_parts_choices():
    """
    Get available parts as choices for form fields.
    Returns a list of (part_id, display_name) tuples.
    """
    try:
        from models import Part
        parts = Part.query.filter_by(status='active').order_by(Part.name).all()
        return [(str(part.id), f"{part.part_number} - {part.name}") for part in parts]
    except:
        # Return empty list if database not available (e.g., during testing)
        return []


def get_parts_by_category():
    """
    Get parts grouped by category for optgroup display.
    Returns a list of (category, [(part_id, display_name), ...]) tuples.
    """
    try:
        from models import Part
        from sqlalchemy import func
        
        parts = Part.query.filter_by(status='active').order_by(Part.category, Part.name).all()
        
        # Group parts by category
        categories = {}
        for part in parts:
            category = part.category or 'Other'
            if category not in categories:
                categories[category] = []
            categories[category].append((str(part.id), f"{part.part_number} - {part.name}"))
        
        return [(category, choices) for category, choices in sorted(categories.items())]
    except:
        return []


class IncidentForm(FlaskForm):
    """
    Form for creating and submitting new incidents.
    
    Fields:
    - equipment: Equipment involved in the incident
    - location: Physical location where the incident occurred
    - description: Detailed description of the incident
    - submit: Submit button
    """
    
    equipment = StringField(
        'Equipment',
        validators=[
            DataRequired(message='Equipment field is required.'),
            Length(min=2, max=200, message='Equipment name must be between 2 and 200 characters.')
        ],
        render_kw={
            'placeholder': 'e.g., Conveyor Belt #3, Pump Station A, Robot Arm #2',
            'class': 'form-control'
        }
    )
    
    location = StringField(
        'Location',
        validators=[
            DataRequired(message='Location field is required.'),
            Length(min=2, max=100, message='Location must be between 2 and 100 characters.')
        ],
        render_kw={
            'placeholder': 'e.g., Production Floor A, Warehouse Section B, Lab Room 101',
            'class': 'form-control'
        }
    )
    
    description = TextAreaField(
        'Description',
        validators=[
            DataRequired(message='Description is required.'),
            Length(min=10, max=2000, message='Description must be between 10 and 2000 characters.')
        ],
        render_kw={
            'placeholder': 'Please provide a detailed description of the incident, including what happened, when it occurred, and any immediate actions taken.',
            'class': 'form-control',
            'rows': 6
        }
    )
    
    # Parts selection field
    parts = MultiCheckboxField(
        'Parts Required/Used',
        choices=[],  # Will be populated dynamically
        validators=[Optional()],
        description='Select parts that are required or used for this incident',
        render_kw={'class': 'form-check-input'}
    )
    
    submit = SubmitField(
        'Submit Incident',
        render_kw={'class': 'btn btn-primary btn-lg'}
    )
    
    def __init__(self, *args, **kwargs):
        """Initialize form and populate parts choices."""
        super().__init__(*args, **kwargs)
        self.populate_parts_choices()
    
    def populate_parts_choices(self):
        """Populate parts choices from database."""
        self.parts.choices = get_parts_choices()


class EnhancedIncidentForm(FlaskForm):
    """
    Enhanced form for creating incidents with additional engineering fields.
    Extends the basic IncidentForm with severity, category, and other classifications.
    """
    
    # Basic incident information
    title = StringField(
        'Incident Title',
        validators=[
            DataRequired(message='Title is required.'),
            Length(min=5, max=200, message='Title must be between 5 and 200 characters.')
        ],
        render_kw={
            'placeholder': 'Brief summary of the incident',
            'class': 'form-control'
        }
    )
    
    equipment = StringField(
        'Equipment',
        validators=[
            DataRequired(message='Equipment field is required.'),
            Length(min=2, max=200, message='Equipment name must be between 2 and 200 characters.')
        ],
        render_kw={
            'placeholder': 'e.g., Conveyor Belt #3, Pump Station A, Robot Arm #2',
            'class': 'form-control'
        }
    )
    
    location = StringField(
        'Location',
        validators=[
            DataRequired(message='Location field is required.'),
            Length(min=2, max=100, message='Location must be between 2 and 100 characters.')
        ],
        render_kw={
            'placeholder': 'e.g., Production Floor A, Warehouse Section B, Lab Room 101',
            'class': 'form-control'
        }
    )
    
    description = TextAreaField(
        'Description',
        validators=[
            DataRequired(message='Description is required.'),
            Length(min=10, max=2000, message='Description must be between 10 and 2000 characters.')
        ],
        render_kw={
            'placeholder': 'Please provide a detailed description of the incident...',
            'class': 'form-control',
            'rows': 6
        }
    )
    
    # Classification fields
    severity = SelectField(
        'Severity',
        choices=[
            ('low', 'Low - Minor issue, no immediate danger'),
            ('medium', 'Medium - Moderate impact, requires attention'),
            ('high', 'High - Significant impact, urgent attention needed'),
            ('critical', 'Critical - Severe impact, immediate action required')
        ],
        validators=[DataRequired(message='Please select a severity level.')],
        render_kw={'class': 'form-select'}
    )
    
    category = SelectField(
        'Category',
        choices=[
            ('mechanical', 'Mechanical'),
            ('electrical', 'Electrical'),
            ('software', 'Software/IT'),
            ('safety', 'Safety'),
            ('quality', 'Quality'),
            ('environmental', 'Environmental'),
            ('process', 'Process'),
            ('other', 'Other')
        ],
        validators=[DataRequired(message='Please select a category.')],
        render_kw={'class': 'form-select'}
    )
    
    incident_type = SelectField(
        'Incident Type',
        choices=[
            ('safety', 'Safety Incident'),
            ('quality', 'Quality Issue'),
            ('maintenance', 'Maintenance Required'),
            ('operational', 'Operational Issue'),
            ('environmental', 'Environmental Concern'),
            ('security', 'Security Issue')
        ],
        validators=[Optional()],
        render_kw={'class': 'form-select'}
    )
    
    priority = SelectField(
        'Priority',
        choices=[
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High'),
            ('urgent', 'Urgent')
        ],
        default='medium',
        validators=[DataRequired(message='Please select a priority level.')],
        render_kw={'class': 'form-select'}
    )
    
    # Parts selection with multiple methods
    parts_checkbox = MultiCheckboxField(
        'Parts Required/Used (Checkboxes)',
        choices=[],  # Will be populated dynamically
        validators=[Optional()],
        description='Select multiple parts using checkboxes',
        render_kw={'class': 'form-check-input'}
    )
    
    parts_select = SelectMultipleField(
        'Parts Required/Used (Multi-Select)',
        choices=[],  # Will be populated dynamically
        validators=[Optional()],
        description='Select multiple parts using multi-select dropdown',
        render_kw={'class': 'form-select', 'multiple': True, 'size': 6}
    )
    
    submit = SubmitField(
        'Submit Incident',
        render_kw={'class': 'btn btn-primary btn-lg'}
    )
    
    def __init__(self, *args, **kwargs):
        """Initialize form and populate parts choices."""
        super().__init__(*args, **kwargs)
        self.populate_parts_choices()
    
    def populate_parts_choices(self):
        """Populate parts choices from database."""
        self.parts_checkbox.choices = get_parts_choices()
        self.parts_select.choices = get_parts_choices()


class IncidentPartsForm(FlaskForm):
    """
    Form specifically for managing parts in incidents.
    Demonstrates different approaches to multi-selection.
    """
    
    # Basic incident info
    incident_title = StringField(
        'Incident Summary',
        validators=[DataRequired(), Length(min=5, max=200)],
        render_kw={'class': 'form-control', 'placeholder': 'Brief incident summary'}
    )
    
    # Checkbox approach for parts selection
    required_parts = MultiCheckboxField(
        'Required Parts (Checkboxes)',
        choices=[],
        validators=[Optional()],
        description='Select parts required for incident resolution'
    )
    
    # Multi-select dropdown approach
    used_parts = SelectMultipleField(
        'Parts Used (Multi-Select)',
        choices=[],
        validators=[Optional()],
        description='Select parts that were actually used',
        render_kw={'class': 'form-select', 'multiple': True, 'size': 8}
    )
    
    # Part search and filter
    part_category_filter = SelectField(
        'Filter by Category',
        choices=[
            ('', 'All Categories'),
            ('mechanical', 'Mechanical'),
            ('electrical', 'Electrical'),
            ('hydraulic', 'Hydraulic'),
            ('pneumatic', 'Pneumatic'),
            ('electronic', 'Electronic'),
            ('consumable', 'Consumable')
        ],
        validators=[Optional()],
        render_kw={'class': 'form-select'}
    )
    
    submit = SubmitField('Update Parts', render_kw={'class': 'btn btn-primary'})
    
    def __init__(self, *args, **kwargs):
        """Initialize form and populate parts choices."""
        super().__init__(*args, **kwargs)
        self.populate_parts_choices()
    
    def populate_parts_choices(self):
        """Populate parts choices from database."""
        try:
            # Get all choices
            all_choices = get_parts_choices()
            self.required_parts.choices = all_choices
            self.used_parts.choices = all_choices
            
            # If no parts available, add a helpful message
            if not all_choices:
                placeholder_choice = [('', 'No parts available - Add parts to the system first')]
                self.required_parts.choices = placeholder_choice
                self.used_parts.choices = placeholder_choice
                
        except Exception as e:
            # Fallback for when database is not available
            self.required_parts.choices = [('', 'Database not available')]
            self.used_parts.choices = [('', 'Database not available')]
