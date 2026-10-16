from os import environ
from pathlib import Path

basedir = Path(__file__).parent

class Config:
    SECRET_KEY = environ.get('FLASK_SECRET', 'dev-secret-change-me')
    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL', f"sqlite:///{basedir / 'cyberflix.db'}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_TIME_LIMIT = None

    # Mail settings (optional - set these in instance/.env for production email sending)
    MAIL_SERVER = environ.get('MAIL_SERVER')
    MAIL_PORT = int(environ.get('MAIL_PORT') or 0)
    MAIL_USERNAME = environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = environ.get('MAIL_PASSWORD')
    MAIL_USE_TLS = environ.get('MAIL_USE_TLS', 'true').lower() in ('true', '1', 'yes')
    MAIL_USE_SSL = environ.get('MAIL_USE_SSL', 'false').lower() in ('true', '1', 'yes')
    MAIL_DEFAULT_SENDER = environ.get('MAIL_DEFAULT_SENDER')
