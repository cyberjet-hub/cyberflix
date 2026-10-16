from flask import Blueprint, render_template, redirect, url_for, flash, request
from .forms import LoginForm, RegisterForm
from .models import User
from . import db, login_manager
from flask_login import login_user, logout_user, login_required

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Logged in successfully.', 'success')
            next_page = request.args.get('next') or url_for('main.index')
            return redirect(next_page)
        flash('Invalid email or password.', 'danger')
    return render_template('login.html', form=form)

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        existing = User.query.filter_by(email=form.email.data.lower()).first()
        if existing:
            flash('Email already registered. Try logging in.', 'warning')
            return redirect(url_for('auth.login'))
        u = User(full_name=form.full_name.data, email=form.email.data.lower())
        u.set_password(form.password.data)
        db.session.add(u)
        db.session.commit()
        flash('Account created! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('signup.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))
