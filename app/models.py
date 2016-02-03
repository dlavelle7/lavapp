from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(64))
    email = db.Column(db.String(64), unique=True)

    def __init__(self, username, password, email):
        self.username = username
        self.password = self.create_password(password)
        self.email = email

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def create_password(self, password):
        return generate_password_hash(password)

    def get_id(self):
        return unicode(self.id)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return "<User {0}>".format(self.username)

    @staticmethod
    def get(user_id):
        return User.query.get(user_id)
