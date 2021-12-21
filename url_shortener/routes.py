import re
from flask import Blueprint, render_template,redirect,request
from flask.helpers import flash
from .models import db
from flask_login import login_user, login_required, logout_user, current_user
from .models import Link,User

views = Blueprint('views', __name__)

@views.route('/')
def index():
    return render_template('index.html',user=current_user) 


@views.route('/add_link', methods=['GET','POST'])
def add_link():
    if request.method == 'POST':
        original_url = request.form['original_url']
        short_url = request.form['short_url']
        link = Link(original_url=original_url, short_url=short_url)
        db.session.add(link)
        db.session.commit()

        return render_template('link_added.html', 
            new_link=link.short_url, original_url=link.original_url)
    return render_template('link_added.html')


@views.route('/<short_url>')
def redirect_to_url(short_url):
    link = Link.query.filter_by(short_url=short_url).first_or_404()

    link.visits = link.visits + 1
    db.session.commit()

    return redirect(link.original_url) 

@views.route('/stats')
def stats():
    links = Link.query.all()
    return render_template('stats.html',links=links, user=current_user)


@views.route('/add', methods = ['GET','POST'])
@login_required
def add():
    links = Link.query.filter_by(user_id=current_user.id).order_by(Link.id.desc()).all() 	
    if request.method == 'POST':
        full_url = request.form.getlist('field[]')
        n = request.form['limit']
        i = 1
        #str = 'http://127.0.0.1:8000/rss?f='
        str = 'https://feed-mixer.herokuapp.com/rss?f='
        for value in full_url:
            if value != '':
                if i == 1:
                    str += value 
                    i += 1
                    str1 = value
                else:
                    str +='&f=' + value
                    i += 1
            else:
                flash('Input field cannot be empty', category='error')
                return render_template('url_add.html',user=current_user,links=links)
        if n:
            str += '&n=' + n
        
        link = Link(original_url=str, user_id=current_user.id)
        db.session.add(link)
        db.session.commit()
        result = Link.query.filter_by(original_url=str).first_or_404()
        links = Link.query.filter_by(user_id=current_user.id).all()
        
        return render_template('link_added.html',original_url=result.original_url,new_link=result.short_url,user=current_user)
    links = Link.query.filter_by(user_id=current_user.id).all()
    return render_template('url_add.html',user=current_user,links=links)