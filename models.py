from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db

# Many-to-many association table for Incident-Parts relationship
incident_parts = db.Table('incident_parts',
    db.Column('incident_id', db.Integer, db.ForeignKey('incidents.id'), primary_key=True),
    db.Column('part_id', db.Integer, db.ForeignKey('parts.id'), primary_key=True),
    db.Column('quantity_used', db.Integer, default=1),  # Number of parts used
    db.Column('status', db.String(20), default='required'),  # 'required', 'ordered', 'received', 'installed'
    db.Column('notes', db.Text),  # Additional notes about the part usage
    db.Column('created_at', db.DateTime, default=datetime.utcnow),
    db.Column('updated_at', db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    department = db.Column(db.String(50), nullable=True)  # Engineering department
    role_level = db.Column(db.String(30), nullable=True)  # Engineer role level
    role = db.Column(db.String(20), default='user')  # 'admin', 'manager', 'user'
    is_active = db.Column(db.Boolean, default=True)
    notifications_enabled = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships with incidents (avoiding backref conflicts)
    # Note: backrefs are defined in the Incident model to avoid conflicts
    
    def set_password(self, password):
        """Set password hash."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password against hash."""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Incident(db.Model):
    """
    Enhanced Incident model to store submitted incidents with engineering-specific fields.
    Includes engineer_id, date_reported, equipment, location, description, and status fields.
    """
    __tablename__ = 'incidents'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    
    # Required fields as requested
    equipment = db.Column(db.String(200), nullable=False)  # Equipment involved in incident
    location = db.Column(db.String(100), nullable=False)   # Physical location of incident
    date_reported = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Incident classification
    severity = db.Column(db.String(20), nullable=False)  # 'low', 'medium', 'high', 'critical'
    status = db.Column(db.String(20), default='open')    # 'open', 'in_progress', 'resolved', 'closed'
    category = db.Column(db.String(50), nullable=False)  # 'mechanical', 'electrical', 'software', etc.
    priority = db.Column(db.String(20), default='medium') # 'low', 'medium', 'high', 'urgent'
    
    # Additional timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    resolved_at = db.Column(db.DateTime)
    
    # Foreign keys and relationships to Engineer and User
    reporter_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    engineer_id = db.Column(db.Integer, db.ForeignKey('engineers.id'), nullable=True)  # Assigned engineer
    assigned_to_id = db.Column(db.Integer, db.ForeignKey('users.id'))  # Backup assignment to any user
    
    # Additional incident details
    incident_type = db.Column(db.String(50))  # 'safety', 'quality', 'maintenance', 'operational'
    root_cause = db.Column(db.Text)           # Analysis of root cause
    corrective_action = db.Column(db.Text)    # Action taken to resolve
    preventive_action = db.Column(db.Text)    # Action to prevent recurrence
    
    # Impact assessment
    downtime_minutes = db.Column(db.Integer, default=0)  # Equipment downtime in minutes
    cost_estimate = db.Column(db.Float)                  # Estimated cost impact
    safety_impact = db.Column(db.String(20))             # 'none', 'minor', 'major', 'critical'
    
    # Relationships
    reporter = db.relationship('User', foreign_keys=[reporter_id], backref='reported_incidents')
    assigned_to = db.relationship('User', foreign_keys=[assigned_to_id], backref='assigned_incidents')
    engineer = db.relationship('Engineer', foreign_keys=[engineer_id], backref='incidents_assigned')
    
    # Many-to-many relationship with parts
    parts = db.relationship('Part', 
                           secondary=incident_parts, 
                           back_populates='incidents',
                           lazy='dynamic')
    
    def __repr__(self):
        return f'<Incident {self.id}: {self.title} - {self.status}>'
    
    def get_duration_minutes(self):
        """Calculate incident duration in minutes."""
        if self.resolved_at:
            duration = self.resolved_at - self.date_reported
            return int(duration.total_seconds() / 60)
        else:
            duration = datetime.utcnow() - self.date_reported
            return int(duration.total_seconds() / 60)
    
    def is_overdue(self):
        """Check if incident is overdue based on severity."""
        if self.status in ['resolved', 'closed']:
            return False
        
        hours_since_reported = (datetime.utcnow() - self.date_reported).total_seconds() / 3600
        
        # Define SLA based on severity
        sla_hours = {
            'critical': 2,
            'high': 8,
            'medium': 24,
            'low': 72
        }
        
        return hours_since_reported > sla_hours.get(self.severity, 24)

class Engineer(db.Model):
    """
    Engineer model to represent engineering staff who can be assigned to incidents.
    This extends the base User model with engineering-specific information.
    """
    __tablename__ = 'engineers'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    employee_id = db.Column(db.String(20), unique=True, nullable=False)
    specialization = db.Column(db.String(100))  # e.g., "Mechanical", "Electrical", "Software"
    certification_level = db.Column(db.String(50))  # e.g., "Junior", "Senior", "Lead"
    years_experience = db.Column(db.Integer)
    shift = db.Column(db.String(20))  # e.g., "Day", "Night", "Rotating"
    is_on_call = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship to User
    user = db.relationship('User', backref=db.backref('engineer_profile', uselist=False))
    
    # Note: Relationship to incidents is defined in Incident model as 'assigned_incidents'
    
    def __repr__(self):
        return f'<Engineer {self.employee_id}: {self.user.username}>'

class Part(db.Model):
    """
    Part model to represent spare parts, components, and materials used in incident resolution.
    Links to incidents through the many-to-many incident_parts association table.
    """
    __tablename__ = 'parts'
    
    id = db.Column(db.Integer, primary_key=True)
    part_number = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    
    # Part classification
    category = db.Column(db.String(50))  # 'mechanical', 'electrical', 'hydraulic', 'pneumatic', etc.
    subcategory = db.Column(db.String(50))  # More specific classification
    
    # Supplier and procurement information
    supplier = db.Column(db.String(100))
    supplier_part_number = db.Column(db.String(50))
    manufacturer = db.Column(db.String(100))
    model_number = db.Column(db.String(50))
    
    # Cost and inventory
    unit_cost = db.Column(db.Float)  # Cost per unit
    currency = db.Column(db.String(3), default='USD')  # Currency code
    minimum_stock = db.Column(db.Integer, default=0)  # Minimum stock level
    current_stock = db.Column(db.Integer, default=0)  # Current inventory level
    location = db.Column(db.String(100))  # Storage location
    
    # Technical specifications
    specifications = db.Column(db.Text)  # Technical specifications in JSON or text format
    compatibility = db.Column(db.Text)  # Compatible equipment/systems
    
    # Status and lifecycle
    status = db.Column(db.String(20), default='active')  # 'active', 'discontinued', 'obsolete'
    lead_time_days = db.Column(db.Integer)  # Lead time for ordering in days
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Many-to-many relationship with incidents
    incidents = db.relationship('Incident', 
                               secondary=incident_parts, 
                               back_populates='parts',
                               lazy='dynamic')
    
    def __repr__(self):
        return f'<Part {self.part_number}: {self.name}>'
    
    def is_low_stock(self):
        """Check if part is below minimum stock level."""
        return self.current_stock <= self.minimum_stock
    
    def total_usage_count(self):
        """Get total number of times this part has been used in incidents."""
        return db.session.query(incident_parts).filter_by(part_id=self.id).count()
    
    def get_usage_in_incident(self, incident_id):
        """Get part usage details for a specific incident."""
        return db.session.query(incident_parts).filter_by(
            incident_id=incident_id, 
            part_id=self.id
        ).first()
    
    @classmethod
    def get_low_stock_parts(cls):
        """Get all parts that are below minimum stock level."""
        return cls.query.filter(cls.current_stock <= cls.minimum_stock).all()
    
    @classmethod
    def search_by_equipment(cls, equipment_name):
        """Search for parts compatible with specific equipment."""
        return cls.query.filter(
            cls.compatibility.contains(equipment_name) |
            cls.description.contains(equipment_name)
        ).all()
