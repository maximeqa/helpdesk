"""
Database models defining the structure of User and Ticket tables.
Uses SQLAlchemy ORM for database interactions.
"""

from . import db
from flask_login import UserMixin
from . import login_manager

class User(UserMixin, db.Model):
    """
    User model representing registered users in the system.
    Involves 1-M relationships.
    """

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')

    tickets = db.relationship('Ticket', backref='creator', lazy=True, foreign_keys='Ticket.user_id')
    assigned_tickets = db.relationship('Ticket', backref='assignee', lazy=True, foreign_keys='Ticket.assignee_id')

    def is_admin(self):
        return self.role == 'admin'

    def __repr__(self):
        return f'<User {self.username}, Role: {self.role}>'

class Ticket(db.Model):
    """
    Ticket model representing support tickets in the system.
    Each ticket belongs to a user and can be assigned to an admin.
    """

    __tablename__ = 'ticket'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    system_type = db.Column(db.String(50), nullable=False, default='Open')
    system = db.Column(db.String(150), nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    assignee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True, default=None)
    
    status = db.Column(db.String(50), nullable=False, default='Open')

    def __repr__(self):
        return f'<Ticket #{self.id} - {self.title}>'

#Flask-Login callback to reload user from session.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))