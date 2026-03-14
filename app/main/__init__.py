"""
Main application blueprint initialisation.
Creates a Blueprint for organizing main application routes.
"""

from flask import Blueprint

main = Blueprint('main', __name__)

from . import routes