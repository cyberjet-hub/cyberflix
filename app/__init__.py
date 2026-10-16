from os import path
from flask import Flask
from . import db, migrate, login_manager, csrf

from flask_sqlalchemy import SQLAlchemy

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config.Config')
    try:
        app.config.from_pyfile('config.py')
    except Exception:
        pass

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = 'auth.login'

    from .auth import auth_bp
    from .routes import main_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    with app.app_context():
        db.create_all()
        # seed sample data
        try:
            from .seed import seed_sample_data
            seed_sample_data()
        except Exception:
            pass

    return app
