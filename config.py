import os
basedir = os.path.abspath(os.path.dirname(__file__))

if os.environ.get('DATABASE_URL') is None:
    # Path to sqlite db file for local development
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
else:
    # Heroku sets an env var named $DATABASE_URL
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True

WTF_CSRF_ENABLED = True
SECRET_KEY = 'onetwothree'

# email server
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
#MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
#MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
MAIL_USERNAME = 'team.lavapp'
MAIL_PASSWORD = 'pythonapp'

# administrator list
ADMINS = ['team.lavapp@gmail.com']
