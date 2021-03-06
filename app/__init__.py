from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.mail import Mail

app = Flask(__name__)
app.config.from_object("config")
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
admin = Admin(app, name='lavapp', template_mode='bootstrap3')
mail = Mail(app)

# TODO: Logging
#if os.environ.get('HEROKU') is not None:
#else:

from app import views, models
admin.add_view(ModelView(models.User, db.session))
admin.add_view(ModelView(models.Budget, db.session))
admin.add_view(ModelView(models.Income, db.session))
admin.add_view(ModelView(models.Expense, db.session))
admin.add_view(ModelView(models.Sum, db.session))
