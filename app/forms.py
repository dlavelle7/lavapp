from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField, TextField
from wtforms.validators import DataRequired, EqualTo


class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])


class RegisterForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired(),
                    EqualTo('repeat_pass', message="Passwords don't match")])
    repeat_pass = PasswordField('password', validators=[DataRequired()])
