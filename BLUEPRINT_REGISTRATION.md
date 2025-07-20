# Blueprint Import and Registration Example

## ✅ **Main Blueprint Already Imported and Registered**

### **Current Setup in `extensions.py`:**

```python
def create_app(config_name=None):
    """Application factory pattern."""
    app = Flask(__name__)
    
    # Configure the app
    if config_name is None:
        config_name = os.environ.get('FLASK_CONFIG') or 'default'
    app.config.from_object(config[config_name])
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    # User loader function for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        from models import User
        return User.query.get(int(user_id))
    
    # Import and register blueprints
    from routes import main_bp, auth_bp          # ← IMPORT BLUEPRINTS
    app.register_blueprint(main_bp)              # ← REGISTER MAIN BLUEPRINT
    app.register_blueprint(auth_bp, url_prefix='/auth')  # ← REGISTER AUTH BLUEPRINT
    
    # Register CLI commands
    from cli_commands import register_commands
    register_commands(app)
    
    return app
```

### **Blueprint Definition in `routes.py`:**

```python
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from models import User, Incident
from extensions import db
from datetime import datetime

# Create blueprints
main_bp = Blueprint('main', __name__)           # ← MAIN BLUEPRINT DEFINITION
auth_bp = Blueprint('auth', __name__)

# Main blueprint routes
@main_bp.route('/')
def home():
    """Home page - landing page for the application."""
    return render_template('index.html')

@main_bp.route('/index')
@main_bp.route('/dashboard')
def index():
    """Dashboard/Index page showing recent incidents for authenticated users."""
    # ... route implementation
```

### **Verification:**

✅ **Blueprint Created:** `main_bp = Blueprint('main', __name__)`  
✅ **Blueprint Imported:** `from routes import main_bp, auth_bp`  
✅ **Blueprint Registered:** `app.register_blueprint(main_bp)`  
✅ **Routes Working:** All main blueprint routes accessible  

### **Available Main Blueprint Routes:**

- `main.home` - `/` (Homepage)
- `main.index` - `/dashboard` and `/index` (Dashboard)
- `main.about` - `/about` (About page)
- `main.contact` - `/contact` (Contact page)
- `main.incidents` - `/incidents` (All incidents)
- `main.new_incident` - `/incident/new` (Report incident)
- `main.incident_detail` - `/incident/<id>` (Incident details)
- `main.update_incident` - `/incident/<id>/update` (Update incident)
- `main.search` - `/search` (Search incidents)
- `main.api_stats` - `/api/stats` (Statistics API)

### **Testing Blueprint Registration:**

```bash
# List all routes to verify registration
flask list-routes | grep main

# Test main blueprint home route
curl http://127.0.0.1:5000/

# Test main blueprint dashboard route
curl http://127.0.0.1:5000/dashboard
```

## **Status: ✅ COMPLETE**

The 'main' blueprint from routes.py is already properly imported and registered in the Flask application. All routes are working correctly and accessible.
