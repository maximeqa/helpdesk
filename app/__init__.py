"""
Main application factory and configuration.
This file sets up the Flask application with all necessary extensions.
"""

# Initialise Flask extensions
from .auth.routes import limiter
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_talisman import Talisman
import os

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():

    """
    Application factory function that creates and configures the Flask app.
    Returns a configured Flask application instance.
    """

    app = Flask(__name__)
    load_dotenv()
    app.config['SECRET_KEY'] =os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] =os.getenv('DATABASE_URI')

    csp = {
        'default-src': "'self'",
        'style-src': ["'self'"]
    }
    Talisman(app, content_security_policy=csp, force_https=False)

    db.init_app(app)
    login_manager.init_app(app)
    limiter.init_app(app)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

def seed_database():
    """
    Populate the database with sample records if it is empty.
    """
    from .models import User, Ticket
    from werkzeug.security import generate_password_hash

    if User.query.first() is not None:
        print("Database already seeded, skipping.")
        return

    admin1 = User(
        username='alice_admin',
        password=generate_password_hash('AdminPass1!', method='pbkdf2:sha256'),
        role='admin'
    )
    admin2 = User(
        username='bob_admin',
        password=generate_password_hash('AdminPass2!', method='pbkdf2:sha256'),
        role='admin'
    )
    user1 = User(
        username='charlie_user',
        password=generate_password_hash('UserPass1!', method='pbkdf2:sha256'),
        role='user'
    )
    user2 = User(
        username='diana_user',
        password=generate_password_hash('UserPass2!', method='pbkdf2:sha256'),
        role='user'
    )
    user3 = User(
        username='eve_user',
        password=generate_password_hash('UserPass3!', method='pbkdf2:sha256'),
        role='user'
    )

    db.session.add_all([admin1, admin2, user1, user2, user3])
    db.session.commit()

    tickets = [
        Ticket(title='Laptop wont boot', description='Dell XPS fails to POST on startup.', system_type='Hardware', system='Dell XPS 15', status='Open', user_id=user1.id),
        Ticket(title='VPN connection dropping', description='Cisco AnyConnect drops every 20 minutes.', system_type='Software', system='Cisco AnyConnect', status='In Progress', user_id=user1.id, assignee_id=admin1.id),
        Ticket(title='Printer offline', description='HP LaserJet shows offline despite being on.', system_type='Hardware', system='HP LaserJet 400', status='Open', user_id=user2.id),
        Ticket(title='Outlook not syncing', description='Emails not syncing since last Windows update.', system_type='Software', system='Microsoft Outlook', status='Closed', user_id=user2.id, assignee_id=admin2.id),
        Ticket(title='Monitor flickering', description='Second monitor flickers when connected via HDMI.', system_type='Hardware', system='Dell U2722D', status='Open', user_id=user3.id),
        Ticket(title='Password reset request', description='User locked out after too many failed attempts.', system_type='Software', system='Active Directory', status='In Progress', user_id=user3.id, assignee_id=admin1.id),
    ]

    db.session.add_all(tickets)
    db.session.commit()
    print("Database seeded successfully.")