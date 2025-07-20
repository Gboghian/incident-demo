"""
Flask-WTF forms for the Incident Management System.
This module contains form classes for handling user input and validation.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Optional


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
    
    submit = SubmitField(
        'Submit Incident',
        render_kw={'class': 'btn btn-primary btn-lg'}
    )


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
    
    submit = SubmitField(
        'Submit Incident',
        render_kw={'class': 'btn btn-primary btn-lg'}
    )
