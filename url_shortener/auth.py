from os import name
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from .models import db
from flask_login import login_user, login_required, logout_user, current_user

from .models import User, Link, Subscription

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    subscription = Subscription.query.all()
    if request.method == 'POST':
        subscription = Subscription.query.all()
        email = request.form.get('email')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        plan = request.form.get('select')
        user = User.query.filter_by(email=email).first()
        sub = Subscription.query.filter_by(name=str(plan)).first()
        if user:
            message=['Email already exists.', 'error']
            return render_template("register.html", message=message,subscription=subscription)
        elif len(email) < 4:
            message=['Email must be greater than 3 characters.', 'error']
            return render_template("register.html", message=message,subscription=subscription)
        elif len(name) < 2:
            message=['First name must be greater than 1 character.', 'error']
            return render_template("register.html", message=message,subscription=subscription)
        elif password1 != password2:
            message=['Passwords don\'t match.', 'error']
            return render_template("register.html", message=message,subscription=subscription)
        elif len(password1) < 7:
            message=['Password must be at least 7 characters.', 'error']
            return render_template("register.html", message=message,subscription=subscription)
        else:
            new_user = User(email=email, first_name=name, password=password1,plan_id=sub.sub_id)
            db.session.add(new_user)
            db.session.commit()
            message=['Account created!', 'success']
            return redirect(url_for('auth.login'))
    return render_template("register.html", message="None",subscription=subscription)


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


@auth.route('/admin' ,methods=['GET', 'POST'])
def admin():
    a="adminadmin"
    if current_user.password == "adminadmin":
        subscription = Subscription.query.all()
        if request.method == 'POST':
            name = request.form.get('name')
            price = request.form.get('price')
            max_urls = request.form.get('max_urls')
            max_feeds = request.form.get('max_feeds')
            try:
                
                new_plan = Subscription(name=name, price=price,max_urls=max_urls, max_feeds=max_feeds)
                db.session.add(new_plan)
                db.session.commit()
                subscription = Subscription.query.all()
                message = ["Successfully created new subscription",'success']
                return render_template("admin.html", message=message,subscription=subscription)
            except Exception as e:
                message = [e,'error']
                return render_template("admin.html", message=message,subscription=subscription)
    else:
        
        return redirect(url_for('views.index'))
    return render_template("admin.html", message="None",subscription=subscription)