from flask import current_app
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from . import mail


def generate_confirmation_token(email: str) -> str:
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='email-confirm-salt')


def confirm_token(token: str, expiration: int = 3600 * 24):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt='email-confirm-salt', max_age=expiration)
    except Exception:
        return False
    return email


def send_confirmation_email(to_email: str, confirm_url: str) -> bool:
    """Attempt to send a confirmation email. Returns True if sent; False if not configured.
    In development when mail isn't configured, the confirm_url can be surfaced to the user via flash.
    """
    cfg = current_app.config
    if not cfg.get('MAIL_SERVER'):
        # Mail not configured
        return False
    subject = 'Confirm your Cyberflix account'
    body = f"Welcome to Cyberflix! Please confirm your account by visiting: {confirm_url}\n\nIf you did not sign up, ignore this message."
    msg = Message(subject=subject, recipients=[to_email], body=body)
    try:
        mail.send(msg)
        return True
    except Exception:
        current_app.logger.exception('Failed to send confirmation email')
        return False
