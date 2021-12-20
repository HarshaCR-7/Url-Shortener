from flask import Flask, app

from .api import initialize_routes
from .models import db, User
from .routes import views
from .auth import auth
from flask_restful import Api
from flask_jwt_extended import JWTManager

def create_app(config_file='settings.py'):
    app = Flask(__name__)
    api =   Api(app)
    app.config.from_pyfile(config_file)
    app.secret_key = 'development'
    app.config['JWT_SECRET_KEY'] = 'JWT_SECRET_KEY'
    db.init_app(app)
    JWTManager(app)

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