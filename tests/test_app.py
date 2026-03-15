"""
Pytest test suite covering authentication, access control, and ticket CRUD.
Run with: pytest tests/tests.py -v
"""

import pytest
from app import create_app, db
from app.models import User, Ticket
from flask_bcrypt import generate_password_hash

#Fixtures

@pytest.fixture
def app():
    """Create a test app instance with an in-memory SQLite database."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.app_context():
        db.create_all()
        _seed_test_data()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Return a test client for the app."""
    return app.test_client()


def _seed_test_data():
    """Insert minimal test records into the in-memory database."""

    admin = User(
        username='test_admin',
        password=generate_password_hash('AdminPass1!').decode('utf-8'),
        role='admin'
    )
    user = User(
        username='test_user',
        password=generate_password_hash('UserPass1!').decode('utf-8'),
        role='user'
    )

    db.session.add_all([admin, user])
    db.session.commit()

    ticket = Ticket(
        title='Test Ticket',
        description='A test ticket.',
        system_type='Software',
        system='TestOS',
        status='Open',
        user_id=user.id
    )
    db.session.add(ticket)
    db.session.commit()


def login(client, username, password):
    """Helper to log a user in via the login route."""
    return client.post('/login', data={
        'username': username,
        'password': password
    }, follow_redirects=True)


def logout(client):
    """Helper to log out."""
    return client.get('/logout', follow_redirects=True)


# Auth

def test_login_valid_user(client):
    """A valid user can log in and is redirected to user home."""
    response = login(client, 'test_user', 'UserPass1!')
    assert response.status_code == 200
    assert b'Your Tickets' in response.data


def test_login_valid_admin(client):
    """A valid admin can log in and is redirected to admin home."""
    response = login(client, 'test_admin', 'AdminPass1!')
    assert response.status_code == 200
    assert b'All Tickets' in response.data


def test_login_wrong_password(client):
    """Login fails with an incorrect password."""
    response = login(client, 'test_user', 'wrongpassword')
    assert b'Invalid username or password' in response.data


def test_login_nonexistent_user(client):
    """Login fails for a username that does not exist."""
    response = login(client, 'ghost_user', 'irrelevant')
    assert b'Invalid username or password' in response.data


def test_logout(client):
    """A logged-in user can log out and is redirected to the index."""
    login(client, 'test_user', 'UserPass1!')
    response = logout(client)
    assert response.status_code == 200
    assert b'Login' in response.data


def test_register_new_user(client):
    """A new user can register successfully."""
    response = client.post('/register', data={
        'username': 'brand_new_user',
        'password': 'NewPass1!'
    }, follow_redirects=True)
    assert b'Registration successful' in response.data


def test_register_duplicate_username(client):
    """Registration fails if the username is already taken."""
    response = client.post('/register', data={
        'username': 'test_user',
        'password': 'AnyPass1!'
    }, follow_redirects=True)
    assert b'Username already taken' in response.data


#Access Control

def test_unauthenticated_user_cannot_reach_user_home(client):
    """An unauthenticated request to /user is redirected to login."""
    response = client.get('/user', follow_redirects=True)
    assert b'Login' in response.data


def test_unauthenticated_user_cannot_reach_admin_home(client):
    """An unauthenticated request to /admin is redirected to login."""
    response = client.get('/admin', follow_redirects=True)
    assert b'Login' in response.data


def test_regular_user_cannot_reach_admin_home(client):
    """A regular user visiting /admin is redirected to user home."""
    login(client, 'test_user', 'UserPass1!')
    response = client.get('/admin', follow_redirects=True)
    assert b'Your Tickets' in response.data


def test_regular_user_cannot_reach_manage_users(client):
    """A regular user visiting /admin/manage-users is redirected away."""
    login(client, 'test_user', 'UserPass1!')
    response = client.get('/admin/manage-users', follow_redirects=True)
    assert b'Your Tickets' in response.data


def test_admin_can_reach_admin_home(client):
    """An admin can access the admin dashboard."""
    login(client, 'test_admin', 'AdminPass1!')
    response = client.get('/admin')
    assert response.status_code == 200
    assert b'All Tickets' in response.data

#Tickets

def test_user_can_submit_ticket(client):
    """A logged-in user can submit a new ticket."""
    login(client, 'test_user', 'UserPass1!')
    response = client.post('/submit-ticket', data={
        'title': 'New Issue',
        'system_type': 'Hardware',
        'system': 'HP Laptop',
        'description': 'Screen cracked.'
    }, follow_redirects=True)
    assert b'Ticket submitted' in response.data


def test_user_cannot_delete_another_users_ticket(client, app):
    """A user cannot delete a ticket that belongs to someone else."""
    # Create a second user with their own ticket
    with app.app_context():
        other_user = User(
            username='other_user',
            password=generate_password_hash('OtherPass1!').decode('utf-8'),
            role='user'
        )
        db.session.add(other_user)
        db.session.commit()
        other_ticket = Ticket(
            title='Other Ticket',
            description='Not yours.',
            system_type='Software',
            system='Linux',
            status='Open',
            user_id=other_user.id
        )
        db.session.add(other_ticket)
        db.session.commit()
        other_ticket_id = other_ticket.id

    login(client, 'test_user', 'UserPass1!')
    response = client.post(f'/delete_ticket/{other_ticket_id}', follow_redirects=True)
    assert b'Unauthorised' in response.data


def test_admin_can_delete_any_ticket(client, app):
    """An admin can delete any ticket regardless of who created it."""
    with app.app_context():
        ticket = Ticket.query.first()
        ticket_id = ticket.id

    login(client, 'test_admin', 'AdminPass1!')
    response = client.post(f'/delete_ticket/{ticket_id}', follow_redirects=True)
    assert b'Ticket deleted' in response.data


def test_unauthenticated_user_cannot_delete_ticket(client, app):
    """An unauthenticated POST to delete_ticket is redirected to login."""
    with app.app_context():
        ticket_id = Ticket.query.first().id

    response = client.post(f'/delete_ticket/{ticket_id}', follow_redirects=True)
    assert b'Login' in response.data