"""
WTForms definitions for handling form validation and rendering.
Each form class represents a HTML form with validation rules.
"""

from flask_wtf import FlaskForm 
from wtforms import SelectField, StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2,max=150)])
    password = PasswordField('Password', validators=[DataRequired()])
    admin = BooleanField('Login as Admin')
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2,max=150)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Register')

class TicketForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2,max=150)])
    system_type = SelectField(
        'System Type',
        choices=[('', '-- Select Type --'), ('Hardware', 'Hardware'), ('Software', 'Software')],
        validators=[DataRequired()]
    )
    system = StringField('System', validators=[DataRequired(), Length(min=2,max=150)])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit Ticket')