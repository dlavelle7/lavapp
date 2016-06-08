import simplejson
from app import app
from flask import render_template, flash, redirect, g, url_for, session, \
        request
from app.forms import LoginForm, RegisterForm, ForgotForm, IncomeForm, \
        ExpenseForm, BudgetForm
from flask.ext.login import current_user, login_required, login_user, logout_user
from app.models import User, Income, Expense, Budget
from app import db
from sqlalchemy.exc import IntegrityError
from app.emails import send_registration_email
from decimal import Decimal


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
    return render_template('index.html', title="Summary")

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

@app.route('/budget', methods=['GET', 'POST'])
@login_required
def budget():
    form = BudgetForm()
    if form.validate_on_submit():
        budget = Budget(form.name.data, current_user.id)
        add_commit_model(budget)
        return redirect(url_for('income', budget_id=budget.id))
    return render_template('budget.html', title="Budget", form=form)

@app.route('/income', methods=['GET', 'POST'])
@login_required
def income():
    form = IncomeForm()
    budget = Budget.query.get(request.args.get("budget_id"))
    if form.validate_on_submit() and budget:
        income = Income(name=form.name.data, amount=form.amount.data,
                budget_id=budget.id, interval=form.interval.data)
        add_commit_model(income)
        return redirect(url_for('income', budget_id=budget.id))
    return render_template('income.html', title="Income", form=form,
            budget=budget)

@app.route('/delete/income/<int:model_id>', methods=['POST'])
@login_required
def delete_income(model_id):
    # TODO: HTML forms don't support DELETE. Workaround / XMLHttpRequest?
    income = Income.query.get(model_id)
    delete_commit_model(income)
    return redirect(url_for('income', budget_id=income.budget_id))

@app.route('/expense', methods=['GET', 'POST'])
@login_required
def expense():
    form = ExpenseForm()
    budget = Budget.query.get(request.args.get("budget_id"))
    if form.validate_on_submit() and budget:
        expense = Expense(name=form.name.data, amount=form.amount.data,
                budget_id=budget.id, interval=form.interval.data,
                shared_by=form.shared_by.data)
        add_commit_model(expense)
        return redirect(url_for('expense', budget_id=budget.id))
    return render_template('expense.html', title="Expense", form=form,
            budget=budget)

@app.route('/delete/expense/<int:model_id>', methods=['POST'])
def delete_expense(model_id):
    # TODO: HTML forms don't support DELETE. Workaround / XMLHttpRequest?
    expense = Expense.query.get(model_id)
    delete_commit_model(expense)
    return redirect(url_for('expense', budget_id=expense.budget_id))

@app.route('/delete/budget/<int:model_id>', methods=['POST'])
def delete_budget(model_id):
    budget = Budget.query.get(model_id)
    if budget:
        delete_commit_model(budget)
    return redirect(url_for('budget'))

@app.route('/budget/<int:model_id>/incomes', methods=['GET'])
@login_required
def budget_incomes(model_id):
    budget = Budget.query.get(model_id)
    if budget:
        incomes = []
        for income in budget.incomes:
            incomes.append({"name": income.name, "y": income.total})
        title = "Income - {0}".format(budget.name)
        return simplejson.dumps({"data": incomes, "title": title})

@app.route('/budget/<int:model_id>/expenses', methods=['GET'])
@login_required
def budget_expenses(model_id):
    budget = Budget.query.get(model_id)
    if budget:
        expenses = []
        for expense in budget.expenses:
            expenses.append({"name": expense.name, "y": expense.total})
        title = "Expense - {0}".format(budget.name)
        return simplejson.dumps({"data": expenses, "title": title})

@app.route('/budget/<int:model_id>/summary', methods=['GET'])
@login_required
def budget_summary(model_id):
    budget = Budget.query.get(model_id)
    if budget:
        data = [{"name": u"Expense", "y": budget._total_expense()},
                {"name": u"Income", "y": budget._total_income()}]
        title = "Summary - {0}".format(budget.name)
        return simplejson.dumps({"data": data, "title": title})
