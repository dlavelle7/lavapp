from app import app
from flask import render_template, flash, redirect, g, url_for, session
from app.forms import LoginForm, RegisterForm

@app.route('/')
def index():
    return render_template('index.html', title="Home")

@app.route('/login', methods=['GET', 'POST'])
def login():
    #if g.user and g.user.is_authenticated:
    #    return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        flash("Login data: {0}, {1}, {2}".format(
            form.username.data, form.password.data, form.remember.data))
        return redirect('/')
    return render_template('login.html', title="Sign In", form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        flash("Register data: {0}, {1}".format(
            form.username.data, form.password.data))
        return redirect('/')
    return render_template('register.html', title="Sign Up", form=form)
