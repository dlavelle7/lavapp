import json
from app import app
from flask import render_template, flash, redirect, g, url_for, session
from app.forms import LoginForm, RegisterForm, ForgotForm, IncomeForm, \
        ExpenseForm
from flask.ext.login import current_user, login_required, login_user, logout_user
from app.models import User, Income, Expense
from app import db
from sqlalchemy.exc import IntegrityError
from app.emails import send_registration_email


#@app.before_request
#def before_request():
#    pass

# TODO: Handle db transactions better
def add_commit_model(model):
    try:
        db.session.add(model)
        db.session.commit()
    except Exception as e:
        print e
        db.session.rollback()

def delete_commit_model(model):
    try:
        db.session.delete(model)
        db.session.commit()
    except Exception as e:
        print e
        db.session.rollback()

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
        # TODO: Remember me
        #session['remember_me'] = form.remember.data
        user = User.query.filter(User.username == form.username.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for('index'))
        flash('Incorrect login details')
    return render_template('login.html', title="Sign In", form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        exists = User.query.filter(User.username == form.username.data).first()
        if exists:
            flash("Username already taken", "error")
        else:
            user = User(username=form.username.data,
                    password=form.password.data, email=form.email.data)
            db.session.add(user)

            try:
                db.session.commit()
            except Exception as e:
                print e
                db.session.rollback()
                return render_template('register.html', title="Sign Up",
                        form=form)

            send_registration_email(user)
            login_user(user)

            return redirect(url_for('index'))
    return render_template('register.html', title="Sign Up", form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

# TODO: This does nothing yet
@app.route('/forgot', methods=['GET', 'POST'])
def forgot():
    form = ForgotForm()
    if form.validate_on_submit():
        flash('{0}'.format(form.data))
    return render_template('forgot.html', title="Forgot Password", form=form)

@app.route('/income', methods=['GET', 'POST'])
@login_required
def income():
    form = IncomeForm()
    if form.validate_on_submit():
        income = Income(name=form.name.data, amount=form.amount.data,
                user_id=current_user.id, interval=form.interval.data)
        add_commit_model(income)
        return redirect(url_for('income'))
    return render_template('income.html', title="Income", form=form)

@app.route('/delete/income/<int:model_id>', methods=['POST'])
@login_required
def delete_income(model_id):
    # TODO: HTML forms don't support DELETE. Workaround / XMLHttpRequest?
    income = Income.query.get(model_id)
    if income:
        delete_commit_model(income)
    return redirect(url_for('income'))

@app.route('/expense', methods=['GET', 'POST'])
@login_required
def expense():
    form = ExpenseForm()
    if form.validate_on_submit():
        expense = Expense(name=form.name.data, amount=form.amount.data,
                user_id=current_user.id, interval=form.interval.data,
                shared_by=form.shared_by.data)
        add_commit_model(expense)
        return redirect(url_for('expense'))
    return render_template('expense.html', title="Expense", form=form)

@app.route('/delete/expense/<int:model_id>', methods=['POST'])
def delete_expense(model_id):
    # TODO: HTML forms don't support DELETE. Workaround / XMLHttpRequest?
    expense = Expense.query.get(model_id)
    if expense:
        delete_commit_model(expense)
    return redirect(url_for('expense'))

@app.route('/user/incomes', methods=['GET'])
@login_required
def user_incomes():
    incomes = []
    for income in current_user.incomes:
        incomes.append({"name": income.name, "y": income.total})
    return json.dumps(incomes)

@app.route('/user/expenses', methods=['GET'])
@login_required
def user_expenses():
    expenses = []
    for expense in current_user.expenses:
        expenses.append({"name": expense.name, "y": expense.total})
    return json.dumps(expenses)

@app.route('/user/balance', methods=['GET'])
@login_required
def user_balance():
    balance = current_user._balance()
    data = [{"name": u"Expenses", "y": current_user._total_expense()},
            {"name": u"Income", "y": current_user._total_income()}]
    return json.dumps(data)
