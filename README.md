# Flask Ticketing System

A modern web-based ticketing system built with Flask that allows users to submit support tickets and administrators to manage them efficiently.

## Features

### User Features
- **User Registration & Login**: Secure account creation and authentication
- **Ticket Submission**: Create support tickets with system type, description, and priority
- **View Personal Tickets**: Track status of submitted tickets
- **Ticket Management**: Delete own tickets when needed

### Admin Features
- **Admin Dashboard**: Overview of all tickets and assigned tickets
- **Ticket Assignment**: Assign tickets to specific administrators
- **Status Management**: Update ticket status (Open, In Progress, Closed)
- **User Management**: Promote/demote users, manage user accounts
- **Ticket Oversight**: View and manage all tickets in the system

## Technology Stack

- **Backend**: Flask (Python web framework)
- **Database**: SQLAlchemy ORM with SQLite/PostgreSQL support
- **Authentication**: Flask-Login for session management
- **Forms**: WTForms for form validation and rendering
- **Frontend**: HTML templates with modern CSS styling
- **Security**: Werkzeug password hashing (PBKDF2-SHA256)

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd flask-ticketing-system
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   Create a `.env` file in the root directory:
   ```env
   SECRET_KEY=your-secret-key-here
   DATABASE_URI=sqlite:///ticketing.db
   ```

5. **Initialise the database**
   ```bash
   python run.py
   ```
   *The database will be created automatically on first run.*

## Usage

### Starting the Application
```bash
python run.py
```
The application will be available at `http://localhost:5000`

### First Time Setup
1. Navigate to the registration page
2. Create your first user account
3. Manually promote the first user to admin in the database

### User Workflow
1. **Register/Login** - Create an account or log into existing account
2. **Submit Tickets** - Create new support tickets with relevant details
3. **Track Progress** - Monitor ticket status and updates
4. **Manage Tickets** - Delete tickets when resolved

### Admin Workflow
1. **Admin Dashboard** - View all tickets and assigned tickets
2. **Assign Tickets** - Assign tickets to administrators
3. **Update Status** - Change ticket status as work progresses
4. **User Management** - Promote users to admin, manage accounts

## Project Structure

```
help-desk/
├── app/
│   ├── __init__.py              # Application factory
│   ├── models.py                # Database models
│   ├── forms.py                 # WTForms definitions
│   ├── auth/
│   │   ├── __init__.py          # Auth blueprint
│   │   └── routes.py            # Authentication routes
│   ├── main/
│   │   ├── __init__.py          # Main blueprint
│   │   └── routes.py            # Main application routes
│   ├── static/
│   │   └── styles.css           # Application styling
│   └── templates/
│       ├── index.html           # Home page
│       ├── login.html           # Login form
│       ├── register.html        # Registration form
│       ├── user_home.html       # User dashboard
│       ├── admin_home.html      # Admin dashboard
│       ├── submit_ticket.html   # Ticket submission form
│       └── manage_users.html    # User management interface
├── requirements.txt             # Python dependencies
├── run.py                      # Application entry point
└── .env                        # Environment variables
```

## Database Schema

### User Table
- `id` (Primary Key)
- `username` (Unique)
- `password` (Hashed)
- `role` (user/admin)

### Ticket Table
- `id` (Primary Key)
- `title`
- `description`
- `system_type` (Hardware/Software)
- `system`
- `status` (Open/In Progress/Closed)
- `user_id` (Foreign Key to User)
- `assignee_id` (Foreign Key to User - Admin)

## Security Features

- **Password Hashing**: PBKDF2-SHA256 encryption for stored passwords
- **Session Management**: Flask-Login handles user sessions securely
- **CSRF Protection**: WTForms provides CSRF token validation
- **Role-based Access**: Admin-only routes protected with decorators
- **Input Validation**: Server-side validation for all form inputs

## Configuration

### Environment Variables
- `SECRET_KEY`: Flask secret key for session encryption
- `DATABASE_URI`: Database connection string

### Default Settings
- **Database**: SQLite
- **Debug Mode**: Enabled in development
- **Session Timeout**: Handled by Flask-Login defaults

## API Endpoints

### Authentication Routes (`/auth/`)
- `GET/POST /login` - User login
- `GET/POST /register` - User registration
- `GET /logout` - User logout

### Main Application Routes (`/`)
- `GET /` - Home page
- `GET /user` - User dashboard
- `GET /admin` - Admin dashboard
- `GET/POST /submit-ticket` - Ticket submission
- `POST /update-ticket/<id>` - Update ticket status/assignment
- `POST /delete-ticket/<id>` - Delete ticket
- `GET /admin/manage-users` - User management interface
- `POST /admin/manage-users/<id>/promote` - Promote user to admin
- `POST /admin/manage-users/<id>/demote` - Demote admin to user
- `POST /admin/users-edit/<id>/delete` - Delete user account

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## Development

### Running in Development Mode
```bash
export FLASK_ENV=development  # On Windows: set FLASK_ENV=development
python render_server.py
```


## Support

For issues and questions:
- Check existing issues in the repository
- Create a new issue with detailed description
- Include steps to reproduce any bugs
