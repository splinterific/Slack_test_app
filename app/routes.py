from app import app,db
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse
from app.forms import LoginForm, RegistrationForm
import os

client_id = os.environ.get('client_id')
client_secret = os.environ.get('client_secret')

# Just a base homepage to show it working without using Slack
@app.route("/")
@app.route("/index")
@login_required
def index():
    user = {"username": "Mark"}
    return render_template('index.html', title='Home', post=posts)

# This is for allowing the installation of the app to a team
@app.route("/install")
def add_to_slack():
    return render_template('install.html', title='Slack App Install', client_id=client_id)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations you are now a registered User')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/posts')
def posts():
    user = {'username': 'Mark'}
    posts = [
        {
            'author': {'username':'JJ'},
            'body': 'Beautiful day in pdx'
        },
        {
            'author': {'username': 'Darren'},
            'body': 'Nice day in VC'
        }
    ]
    return render_template('posts.html', title='Posts', user=user, posts=posts)





######################
# Errors start here: #
######################


# Error handling for 404
@app.errorhandler(404)
def page_not_found(error):
    return 'This page does not exist - 404', 404

# Error handling 503
@app.errorhandler(503)
def error_503_page(error):
    return 'This is the 503 page', 503
