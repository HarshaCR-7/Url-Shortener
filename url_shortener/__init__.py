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
    
    ENV = 'Prod'  #For Production porpose
    #ENV = 'dev'  #local For Development porpose

    if ENV == 'dev':  #local For Development porpose
        app.debug = True
        #app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/mixer'
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///db.sqlite3'
        #app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://csvwriuijpgbki:f00571a2992db6f219b352125c7c87633baf0e1de5999a900210ad6b1f6829c7@ec2-50-19-160-40.compute-1.amazonaws.com:5432/d36uf0phsvofer'
    else:  #For Production porpose
        app.debug = False
        #app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///db.sqlite3'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://csvwriuijpgbki:f00571a2992db6f219b352125c7c87633baf0e1de5999a900210ad6b1f6829c7@ec2-50-19-160-40.compute-1.amazonaws.com:5432/d36uf0phsvofer'
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



