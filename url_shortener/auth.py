from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from .models import db
from flask_login import login_user, login_required, logout_user, current_user

from .models import User, Link

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email=email).first()
        if user:
            message=['Email already exists.', 'error']
            return render_template("register.html", message=message)
        elif len(email) < 4:
            message=['Email must be greater than 3 characters.', 'error']
            return render_template("register.html", message=message)
        elif len(name) < 2:
            message=['First name must be greater than 1 character.', 'error']
            return render_template("register.html", message=message)
        elif password1 != password2:
            message=['Passwords don\'t match.', 'error']
            return render_template("register.html", message=message)
        elif len(password1) < 7:
            message=['Password must be at least 7 characters.', 'error']
            return render_template("register.html", message=message)
        else:
            new_user = User(email=email, first_name=name, password=password1)
            db.session.add(new_user)
            db.session.commit()
            message=['Account created!', 'success']
            return redirect(url_for('auth.login'))
    return render_template("register.html", message="None")


@auth.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if user.password == password:
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.add'))
            else:
                message=['Incorrect password, try again.', 'error']
                return render_template("login.html", message=message)
        else:
            message=['Email does not exist.', 'error']
            return render_template("login.html", message=message)

    return render_template("login.html", message="None")

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.index'))