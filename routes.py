from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from models import User, Incident
from extensions import db
from datetime import datetime

# Create blueprints
main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__)

# Home and main routes
@main_bp.route('/')
def home():
    """Home page - landing page for the application."""
    return render_template('index.html')

@main_bp.route('/index')
@main_bp.route('/dashboard')
def index():
    """Dashboard/Index page showing recent incidents for authenticated users."""
    if not current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    # Get recent incidents for dashboard
    recent_incidents = Incident.query.order_by(Incident.created_at.desc()).limit(10).all()
    
    # Get user's own incidents
    user_incidents = Incident.query.filter_by(reporter_id=current_user.id).order_by(Incident.created_at.desc()).limit(5).all()
    
    # Get incident statistics
    total_incidents = Incident.query.count()
    open_incidents = Incident.query.filter_by(status='open').count()
    in_progress_incidents = Incident.query.filter_by(status='in_progress').count()
    resolved_incidents = Incident.query.filter(Incident.status.in_(['resolved', 'closed'])).count()
    
    stats = {
        'total': total_incidents,
        'open': open_incidents,
        'in_progress': in_progress_incidents,
        'resolved': resolved_incidents
    }
    
    return render_template('dashboard.html', 
                         incidents=recent_incidents,
                         user_incidents=user_incidents,
                         stats=stats)

@main_bp.route('/incidents')
@login_required
def incidents():
    """List all incidents."""
    page = request.args.get('page', 1, type=int)
    incidents = Incident.query.order_by(Incident.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    return render_template('incidents.html', incidents=incidents)

@main_bp.route('/incident/new', methods=['GET', 'POST'])
@login_required
def new_incident():
    """Create a new incident."""
    if request.method == 'POST':
        incident = Incident(
            title=request.form['title'],
            description=request.form['description'],
            severity=request.form['severity'],
            category=request.form['category'],
            location=request.form.get('location', ''),
            reporter_id=current_user.id
        )
        db.session.add(incident)
        db.session.commit()
        flash('Incident reported successfully!', 'success')
        return redirect(url_for('main.index'))
    
    return render_template('new_incident.html')

@main_bp.route('/incident/<int:id>')
@login_required
def incident_detail(id):
    """View incident details."""
    incident = Incident.query.get_or_404(id)
    return render_template('incident_detail.html', incident=incident)

@main_bp.route('/incident/<int:id>/update', methods=['POST'])
@login_required
def update_incident(id):
    """Update incident status."""
    incident = Incident.query.get_or_404(id)
    
    # Check if user has permission to update
    if current_user.role not in ['admin', 'manager'] and incident.reporter_id != current_user.id:
        flash('You do not have permission to update this incident.', 'error')
        return redirect(url_for('main.incident_detail', id=id))
    
    incident.status = request.form['status']
    incident.updated_at = datetime.utcnow()
    
    if incident.status in ['resolved', 'closed']:
        incident.resolved_at = datetime.utcnow()
    
    db.session.commit()
    flash('Incident updated successfully!', 'success')
    return redirect(url_for('main.incident_detail', id=id))

@main_bp.route('/about')
def about():
    """About page with system information."""
    return render_template('about.html')

@main_bp.route('/contact')
def contact():
    """Contact page."""
    return render_template('contact.html')

@main_bp.route('/api/stats')
@login_required
def api_stats():
    """API endpoint for dashboard statistics."""
    stats = {
        'total_incidents': Incident.query.count(),
        'open_incidents': Incident.query.filter_by(status='open').count(),
        'in_progress_incidents': Incident.query.filter_by(status='in_progress').count(),
        'resolved_incidents': Incident.query.filter(Incident.status.in_(['resolved', 'closed'])).count(),
        'critical_incidents': Incident.query.filter_by(severity='critical').count(),
        'high_priority_incidents': Incident.query.filter_by(severity='high').count()
    }
    return jsonify(stats)

@main_bp.route('/search')
@login_required
def search():
    """Search incidents."""
    query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    
    if query:
        incidents = Incident.query.filter(
            Incident.title.contains(query) | 
            Incident.description.contains(query)
        ).order_by(Incident.created_at.desc()).paginate(
            page=page, per_page=20, error_out=False
        )
    else:
        incidents = Incident.query.order_by(Incident.created_at.desc()).paginate(
            page=page, per_page=20, error_out=False
        )
    
    return render_template('search_results.html', incidents=incidents, query=query)

# Authentication routes
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user, remember=request.form.get('remember'))
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        else:
            flash('Invalid username or password.', 'error')
    
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration."""
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'error')
            return render_template('register.html')
        
        # Create new user
        user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """User logout."""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))
