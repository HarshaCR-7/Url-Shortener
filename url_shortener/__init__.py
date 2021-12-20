from flask import Flask, app

from .api import initialize_routes
from .models import db, User
from .routes import views
from .auth import auth
from flask_restful import Api

def create_app(config_file='settings.py'):
    app = Flask(__name__)
    api =   Api(app)
    app.config['SECRET_KEY'] = 'hjshjhdjahjfjfjkjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///db.sqlite3'
    db.init_app(app)


    app.register_blueprint(views)
    app.register_blueprint(auth)
    from flask_login import LoginManager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    initialize_routes(api)

    return app