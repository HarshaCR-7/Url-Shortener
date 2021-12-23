from flask import Flask, app, render_template
from .models import db, User
from .routes import views
from .auth import auth

def create_app(config_file='settings.py'):
    app = Flask(__name__)
    @app.errorhandler(404) 
    def invalid_route(e): 
        return render_template('404.html')
    app.config['SECRET_KEY'] = 'hjshjhdjahjfjfjkjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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

    return app



