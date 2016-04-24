from app import db
from passlib.hash import pbkdf2_sha256
import datetime


def round_for_currency(value):
    return "{:,.2f}".format(value)

def format_date(date_object):
    return date_object.strftime("%d-%m-%Y")


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

    @property
    def total_income(self):
        return round_for_currency(sum(income.total for income in self.incomes))


# TODO: Split models module (one class per module)
class Sum(db.Model):

    __tablename__ = "sum"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    amount = db.Column(db.Float)
    date_created = db.Column(db.DateTime)
    interval = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    type = db.Column(db.String(50))
    __mapper_args__ = {
        'polymorphic_identity':'sum',
        'polymorphic_on':type
    }

    def __init__(self, name, amount, user_id, interval):
        self.name = name
        self.amount = amount
        self.user_id = user_id
        self.date_created = datetime.datetime.now()
        self.interval = interval

    @property
    def total(self):
        if self.interval == "weekly":
            return self.amount * 4
        elif self.interval == "yearly":
            return self.amount / 56
        else:
            return self.amount

    @property
    def rounded_total(self):
        return  round_for_currency(self.total)

    @property
    def formatted_date_created(self):
        return format_date(self.date_created)


# Joined Table Inheritance
class Income(Sum):
    __tablename__ = "income"
    id = db.Column(db.Integer, db.ForeignKey('sum.id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity':'income',
    }


class Expense(Sum):
    __tablename__ = "expense"
    id = db.Column(db.Integer, db.ForeignKey('sum.id'), primary_key=True)
    __mapper_args__ = {
        'polymorphic_identity':'expense',
    }
