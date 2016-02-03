from app import app
from flask import render_template, flash, redirect, g, url_for, session
from app.forms import LoginForm, RegisterForm, ForgotForm
from flask.ext.login import current_user, login_required, login_user, logout_user
from app.models import User
from app import db
from sqlalchemy.exc import IntegrityError

#@app.before_request
#def before_request():
#    pass

@app.login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/')
@login_required
def index():
    return render_template('index.html', title="Home")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user and current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        #session['remember_me'] = form.remember.data

        user = User.query.filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        flash('Incorrect login details')
    return render_template('login.html', title="Sign In", form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        user = User(username=form.username.data, password=form.password.data,
                email=form.email.data)
        db.session.add(user)

        try:
            db.session.commit()
        except IntegrityError as e:
            print e
            db.session.rollback()
            return render_template('register.html', title="Sign Up", form=form)

        login_user(user)

        return redirect('/')
    return render_template('register.html', title="Sign Up", form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    form = ForgotForm()
    if form.validate_on_submit():
        flash('{0}'.format(form.forgot.data))
    return render_template('forgot.html', title="Forgot Password", form=form)
