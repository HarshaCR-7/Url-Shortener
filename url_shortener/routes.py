import re
from flask import Blueprint, render_template,redirect,Response,request,url_for
from flask.helpers import flash
from .models import db
from flask_login import login_user, login_required, logout_user, current_user
from .models import Link,User,Subscription
import requests
views = Blueprint('views', __name__)

@views.route('/')
def index():
    return render_template('index.html',user=current_user) 


@views.route('/<short_url>')
def redirect_to_url(short_url):
    link = Link.query.filter_by(short_url=short_url).first_or_404()

    link.visits = link.visits + 1
    db.session.commit()

    r = requests.get(link.original_url)
    return Response(r, mimetype='text/xml')


@views.route('/add', methods = ['GET','POST'])
@login_required
def add():
    user_plan = User.query.filter_by(id=current_user.id).first()
    sub_plan = Subscription.query.filter_by(sub_id=user_plan.plan_id).first()
    sub_maxurls = sub_plan.max_urls
    sub_maxfeeds = sub_plan.max_feeds
    links = Link.query.filter_by(user_id=current_user.id).limit(sub_maxfeeds).all()
    
    if request.method == 'POST':
        full_url = request.form.getlist('field[]')
        n = request.form['limit']
        print(len(full_url))
        if len(full_url)<=0:
            flash('Input field cannot be empty', category='error')
            return render_template('url_add.html',sub_maxfeeds=sub_maxfeeds,sub_maxurls=sub_maxurls,user=current_user,links=links)
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
                return render_template('url_add.html',user=current_user,links=links,sub_maxfeeds=sub_maxfeeds,sub_maxurls=sub_maxurls)
        if n:
            if n.isdigit():
                str += '&n=' + n
            else:
                flash('Feeds per URL should be integer', category='error')
                return render_template('url_add.html',user=current_user,links=links,sub_maxfeeds=sub_maxfeeds,sub_maxurls=sub_maxurls) 
        if len(links) >= sub_maxfeeds:
            flash('Feed are Maxed out!', category='error')
            return render_template('url_add.html',user=current_user,links=links,sub_maxfeeds=sub_maxfeeds,sub_maxurls=sub_maxurls)
        link = Link(original_url=str, user_id=current_user.id)
        db.session.add(link)
        db.session.commit()
        result = Link.query.filter_by(original_url=str).first_or_404()
        links = Link.query.filter_by(user_id=current_user.id).limit(sub_maxfeeds).all()
        
        return render_template('link_added.html',original_url=result.original_url,new_link=result.short_url,user=current_user,sub_maxfeeds=sub_maxfeeds,sub_maxurls=sub_maxurls)
    links = Link.query.filter_by(user_id=current_user.id).limit(sub_maxfeeds).all()
    return render_template('url_add.html',user=current_user,links=links,sub_maxfeeds=sub_maxfeeds,sub_maxurls=sub_maxurls)


@views.route('/dellink', methods = ['GET','POST'])
def dellink():
  if request.method == 'POST':
    link = request.form['linkid']
    Cust_id = Link.query.get(link)
    db.session.delete(Cust_id)
    db.session.commit()
    return redirect('/add')




@views.route('/profile', methods = ['GET','POST'])
def profile():
    plan = Subscription.query.filter_by(sub_id = current_user.plan_id).first()
    if request.method == 'POST':
        options = request.form['options']
        user_plan = Subscription.query.filter_by(name=str(options)).first()
        current_user.plan_id = user_plan.sub_id
        db.session.commit()
        return redirect(url_for('views.profile'))
    return render_template('profile.html',user=current_user,plan=plan.name)