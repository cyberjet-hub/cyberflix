from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from .forms import LoginForm, RegisterForm
from .models import User
from . import db, login_manager
from .email import generate_confirmation_token, confirm_token, send_confirmation_email

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
            if not user.confirmed:
                flash('Please confirm your email address before logging in. Check your email or resend confirmation.', 'warning')
                return redirect(url_for('auth.login'))
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

        user = User(full_name=form.full_name.data, email=form.email.data.lower())
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        token = generate_confirmation_token(user.email)
        confirm_url = url_for('auth.confirm_email', token=token, _external=True)
        sent = send_confirmation_email(user.email, confirm_url)
        if sent:
            flash('Account created! A confirmation email has been sent — check your inbox.', 'success')
        else:
            flash('Account created! (Development mode: email not configured)', 'success')
            flash(f'Confirmation link (dev): {confirm_url}', 'info')

        return redirect(url_for('auth.login'))

    return render_template('signup.html', form=form)

@auth_bp.route('/confirm/<token>')
def confirm_email(token):
    email = confirm_token(token)
    if not email:
        flash('The confirmation link is invalid or has expired.', 'danger')
        return redirect(url_for('auth.login'))

    user = User.query.filter_by(email=email).first()
    if not user:
        flash('Account not found for that confirmation link.', 'danger')
        return redirect(url_for('auth.signup'))

    if user.confirmed:
        flash('Account already confirmed. Please log in.', 'info')
        return redirect(url_for('auth.login'))

    from datetime import datetime
    user.confirmed = True
    user.confirmed_at = datetime.utcnow()
    db.session.add(user)
    db.session.commit()

    flash('Your account has been confirmed! You can now log in.', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/resend')
@login_required
def resend_confirmation():
    user = User.query.get(current_user.id)
    if user and not user.confirmed:
        token = generate_confirmation_token(user.email)
        confirm_url = url_for('auth.confirm_email', token=token, _external=True)
        sent = send_confirmation_email(user.email, confirm_url)
        if sent:
            flash('A new confirmation email has been sent.', 'success')
        else:
            flash('Mail not configured. Confirmation link shown below.', 'info')
            flash(f'Confirmation link (dev): {confirm_url}', 'info')
    return redirect(url_for('main.index'))

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))
