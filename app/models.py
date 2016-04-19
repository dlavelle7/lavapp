from app import db
from passlib.hash import pbkdf2_sha256
import datetime


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(64))
    email = db.Column(db.String(64))
    incomes = db.relationship("Income", backref='user')

    def __init__(self, username, password, email):
        self.username = username
        self.password = self.create_password_hash(password)
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

    def create_password_hash(self, password):
        """Generate password hash with salt"""
        return pbkdf2_sha256.encrypt(password, rounds=1000, salt_size=16)

    def get_id(self):
        return unicode(self.id)

    def verify_password(self, password):
        return pbkdf2_sha256.verify(password, self.password)

    def __repr__(self):
        return "<User {0}>".format(self.username)

    @staticmethod
    def get(user_id):
        return User.query.get(user_id)


# TODO: Split model modules
# TODO: Subclass this with WeeklyIncome too
class Income(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    amount = db.Column(db.Float)
    date_created = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name, amount, user_id):
        self.name = name
        self.amount = amount
        self.user_id = user_id
        self.date_created = datetime.datetime.now()
