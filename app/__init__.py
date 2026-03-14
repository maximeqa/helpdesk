"""
Main application factory and configuration.
This file sets up the Flask application with all necessary extensions.
"""

# Initialise Flask extensions
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
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

    db.init_app(app)
    login_manager.init_app(app)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app