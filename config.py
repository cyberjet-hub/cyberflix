from os import environ
from pathlib import Path

basedir = Path(__file__).parent

class Config:
    SECRET_KEY = environ.get('FLASK_SECRET', 'dev-secret-change-me')
    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL', f"sqlite:///{basedir / 'cyberflix.db'}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_TIME_LIMIT = None
