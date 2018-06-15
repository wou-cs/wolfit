from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from app import app
from app.models import User, Post
from app.forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    posts = Post.query.all()
    greeting_name = 'Anonymous'
    if current_user.is_authenticated:
        greeting_name = current_user.username

    return render_template('index.html', greeting_name=greeting_name, posts=posts)


@app.route('/login', methods=['GET', 'POST'])
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
        return redirect(url_for('index'))
    elif form.is_submitted():
        return redirect(url_for('login'))
    else:
        return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
