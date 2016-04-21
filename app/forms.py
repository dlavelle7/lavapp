from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField, TextField, \
        SelectField, DecimalField, FloatField
from wtforms.validators import DataRequired, EqualTo, Email


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


class IncomeForm(Form):
    periodic_choices = [('weekly', 'Weekly'), ('monthly', 'Monthly'),
            ('yearly', 'Yearly')]

    name = StringField('name', validators=[DataRequired()])
    period = SelectField('period', choices=periodic_choices)
    amount = DecimalField('amount', places='2', rounding=None,
            validators=[DataRequired()])
