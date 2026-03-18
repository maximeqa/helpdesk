# IT Help Desk Ticketing System

A secure web-based IT Help Desk Ticketing System built with Python and Flask, developed using a DevOps approach with a fully automated CI/CD pipeline.

## Live Application

🔗 https://helpdesk-r5vz.onrender.com/

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Security](#security)
- [Project Structure](#project-structure)
- [Running Locally](#running-locally)
- [Running Tests](#running-tests)
- [CI/CD Pipeline](#cicd-pipeline)
- [Deployment](#deployment)
- [Sample Credentials](#sample-credentials)

---

## Overview

This application allows regular users to submit and manage IT support tickets, while administrators can assign, update, and manage all tickets and user accounts. It was developed as part of a university assignment demonstrating secure web application development and DevOps practices.

---

## Features

**Regular Users**
- Register and log in securely
- Submit support tickets with title, system type, system name, and description
- View and delete their own tickets

**Administrators**
- View all tickets across all users
- Assign tickets to admin staff
- Update ticket status (Open / In Progress / Closed)
- Promote, demote, and delete user accounts
- Delete any ticket

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.11 |
| Web Framework | Flask |
| Database | SQLite via SQLAlchemy ORM |
| Authentication | Flask-Login |
| Form Handling | Flask-WTF / WTForms |
| Password Hashing | Flask-Bcrypt |
| Rate Limiting | Flask-Limiter |
| Security Headers | Flask-Talisman |
| Production Server | Waitress |
| Testing | pytest |
| Linting | flake8 |
| Security Scanning | bandit |
| CI/CD | GitHub Actions |
| Deployment | Render |

---

## Project Structure
```
helpdesk/
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions CI/CD pipeline
├── app/
│   ├── __init__.py             # App factory, extensions, seed function
│   ├── models.py               # SQLAlchemy User and Ticket models
│   ├── forms.py                # WTForms form definitions
│   ├── auth/
│   │   ├── __init__.py         # Auth blueprint
│   │   └── routes.py           # Login, register, logout routes
│   ├── main/
│   │   ├── __init__.py         # Main blueprint
│   │   └── routes.py           # Ticket and user management routes
│   └── templates/
│       ├── index.html
│       ├── login.html
│       ├── register.html
│       ├── user_home.html
│       ├── admin_home.html
│       ├── manage_users.html
│       └── submit_ticket.html
├── tests/
│   ├── __init__.py
│   └── test_app.py             # 16 pytest tests
├── conftest.py                 # pytest path configuration
├── pytest.ini                  # pytest settings
├── render.yaml                 # Render deployment configuration
├── render_server.py            # Waitress production server
├── run.py                      # Local development entry point
├── requirements.txt
└── .gitignore
```

---

## Running Locally

### Prerequisites
- Python 3.11+
- pip

### Setup

1. Clone the repository:
```bash
git clone https://github.com/maximeqa/helpdesk.git
cd helpdesk
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root:
```
SECRET_KEY=your-local-secret-key
DATABASE_URI=sqlite:///help-desk.db
```

5. Run the application:
```bash
python run.py
```

The app will be available at `http://127.0.0.1:5000`. The database is created and seeded automatically on first run.

---

## Running Tests
```bash
pytest tests/ -v
```

The test suite runs against an in-memory SQLite database — no setup required. All 16 tests should pass.

### What is tested
- Valid and invalid login attempts
- User registration including duplicate username handling
- Logout
- Unauthenticated access to protected routes
- Regular user attempting to access admin routes
- Ticket submission
- Authorisation on ticket deletion (user cannot delete another user's ticket)
- Admin can delete any ticket
- Unauthenticated delete attempt

---

## CI/CD Pipeline

The pipeline runs automatically on every push to `main` and every pull request via GitHub Actions.
```
Push to GitHub
      │
      ▼
┌─────────────┐
│  Lint       │  flake8 — checks code style and syntax
│  (flake8)   │
└──────┬──────┘
       │ pass
       ▼
┌─────────────┐
│  Security   │  bandit — static analysis for security vulnerabilities
│  (bandit)   │
└──────┬──────┘
       │ pass
       ▼
┌─────────────┐
│  Test       │  pytest — runs all 16 unit and integration tests
│  (pytest)   │
└──────┬──────┘
       │ pass
       ▼
┌─────────────┐
│  Deploy     │  Render auto-deploys on merge to main
│  (Render)   │
└─────────────┘
```

Each job must pass before the next runs. A failure at any stage blocks deployment.

---

## Deployment

The application is deployed on [Render](https://render.com) using Waitress as the production WSGI server.

- Auto-deploys on every push to `main`
- Database is created and seeded automatically on startup
- Environment variables managed via Render dashboard
- `DATABASE_URI` and `SECRET_KEY` are never committed to the repository

---

## Sample Credentials

The following accounts are created automatically when the application starts:

| Username | Password | Role |
|---|---|---|
| `alice_admin` | `AdminPass1!` | Admin |
| `bob_admin` | `AdminPass2!` | Admin |
| `charlie_user` | `UserPass1!` | User |
| `diana_user` | `UserPass2!` | User |
| `eve_user` | `UserPass3!` | User |
-

