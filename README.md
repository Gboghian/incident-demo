# Incident Management System

A Flask-based web application for managing and tracking incidents with user authentication and role-based access control.

## Features

- User authentication and registration
- Role-based access control (Admin, Manager, User)
- Incident reporting and tracking
- Dashboard with incident overview
- SQLite database with SQLAlchemy ORM
- Responsive Bootstrap UI

## Setup Instructions

### 1. Install Dependencies

**Production dependencies:**
```bash
pip install -r requirements.txt
```

**Development dependencies (optional):**
```bash
pip install -r requirements-dev.txt
```

**Using Make (recommended):**
```bash
make install          # Production dependencies
make install-dev      # Development dependencies
```

### 2. Initialize the Database

```bash
python init_db.py
```

This will create the database tables and an admin user:
- Username: `admin`
- Password: `admin123`

**Important:** Change the default admin password after first login!

### 3. Run the Application

**Option 1: Using the main entry point (recommended)**
```bash
python run.py
```

**Option 2: Using the start script**
```bash
./start.sh
```

**Option 4: Using Make**
```bash
make run
```

**Option 5: Using Docker**
```bash
make docker-build
make docker-run
```

The application will be available at `http://localhost:5000`

## Project Structure

```
Incident-report-system/
├── run.py              # Main entry point for the application
├── app.py              # Flask application instance (for WSGI)
├── extensions.py       # App factory and extension initialization  
├── config.py           # Configuration settings
├── models.py           # Database models (User, Incident)
├── routes.py           # Route handlers and blueprints
├── init_db.py          # Database initialization script
├── requirements.txt    # Python dependencies
├── db/                 # Database directory
│   └── ims.db         # SQLite database (created after init)
└── templates/          # HTML templates
    ├── base.html
    ├── index.html
    ├── login.html
    ├── register.html
    └── dashboard.html
```

## Usage

1. **Registration:** Create a new user account
2. **Login:** Access the system with your credentials
3. **Dashboard:** View your incidents and system overview
4. **Report Incident:** Create new incident reports
5. **Manage Incidents:** Update status and track progress

## Database Schema

### Users Table
- User authentication and profile information
- Role-based permissions (admin, manager, user)

### Incidents Table
- Incident details (title, description, severity, status)
- Timestamps for tracking
- Reporter and assignee relationships

## Security Features

- Password hashing with Werkzeug
- Session management with Flask-Login
- CSRF protection
- Role-based access control

## Environment Variables

- `SECRET_KEY`: Flask secret key for sessions
- `FLASK_CONFIG`: Configuration mode (development, production, testing)
- `DATABASE_URL`: Database connection string (optional)

## Dependencies

### Core Packages
- **Flask**: Web framework
- **Flask-SQLAlchemy**: Database ORM
- **Flask-Login**: User authentication
- **Flask-WTF**: Form handling and CSRF protection
- **Flask-Migrate**: Database migrations
- **Flask-Mail**: Email support
- **Werkzeug**: WSGI utilities and password hashing

### Additional Features
- **python-dotenv**: Environment variable management
- **gunicorn**: Production WSGI server
- **bcrypt**: Enhanced password hashing
- **Flask-Talisman**: Security headers
- **Flask-RESTful**: API support (for future expansion)

### Development Tools
- **pytest**: Testing framework
- **black**: Code formatting
- **flake8**: Code linting
- **mypy**: Type checking
- **pre-commit**: Git hooks

## Testing

Run the test suite:
```bash
pytest
# or
make test
```

Run with coverage:
```bash
pytest --cov=.
```

## Development

### Code Formatting
```bash
make format     # Format code with black and isort
make lint       # Run linting checks
```

### Database Management
```bash
make init-db              # Initialize database
make create-migration     # Create new migration
make migrate             # Apply migrations
```

## Docker Deployment

### Build and Run
```bash
docker build -t incident-management-system .
docker run -p 5000:5000 incident-management-system
```

### Using Docker Compose (coming soon)
```bash
docker-compose up
```

## Environment Configuration

Copy the example environment file and customize:
```bash
cp .env.example .env
# Edit .env with your settings
```

Available environment variables:
- `FLASK_CONFIG`: development/production/testing
- `SECRET_KEY`: Flask secret key
- `DATABASE_URL`: Database connection string
- `MAIL_SERVER`: Email server configuration
- `INCIDENTS_PER_PAGE`: Pagination settings

## Production Deployment

1. Set environment variables:
   ```bash
   export SECRET_KEY="your-secure-secret-key"
   export FLASK_CONFIG=production
   ```

2. Use a production WSGI server like Gunicorn:
   ```bash
   pip install gunicorn
   gunicorn app:app
   ```

## License

This project is open source and available under the MIT License.
