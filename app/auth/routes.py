"""
Authentication routes handling login, registration, and logout.
All routes in this file are prefixed with the auth blueprint.
"""

from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from . import auth
from .. import db, limiter, bcrypt
from ..models import User
from ..forms import LoginForm, RegisterForm

@auth.route('/login', methods=['GET', 'POST'])
@limiter.limit("10 per minute")
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Logged in successfully.', 'success')
            if user.is_admin():
                return redirect(url_for('main.admin_home'))
            else:
                return redirect(url_for('main.user_home'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Username already taken. Please choose another.', 'error')
            return redirect(url_for('auth.register'))
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))