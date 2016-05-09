from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField, TextField, \
        SelectField, DecimalField, IntegerField
from wtforms.validators import DataRequired, EqualTo, Email, NumberRange
from flask.ext.wtf.html5 import NumberInput


class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    #remember = BooleanField('remember', default=False)


class RegisterForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired(),
                    EqualTo('repeat_pass', message="Passwords don't match")])
    repeat_pass = PasswordField('password', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])

class ForgotForm(Form):
    forgot = StringField('forgot', validators=[DataRequired(), Email()])


class BaseBudgetForm(Form):
    interval_choices = [('weekly', 'Weekly'),('fortnightly', 'Fortnightly'),
            ('monthly', 'Monthly'), ('bimonthly', 'Bimonthly'),
            ('quarterly', 'Quarterly'), ('yearly', 'Yearly')]

    name = StringField('name', validators=[DataRequired()])
    interval = SelectField('interval', choices=interval_choices)
    amount = DecimalField('amount', places=2, rounding=None,
            validators=[NumberRange(min=0.01)])


# TODO: Handle user putting in commas
class IncomeForm(BaseBudgetForm):
    pass


class ExpenseForm(BaseBudgetForm):
    shared_by = IntegerField('shared_by', widget=NumberInput(min=1), default=1)
