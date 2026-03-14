"""
Authentication blueprint initialisation.
Creates a Blueprint for organizing authentication-related routes.
"""

from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import routes