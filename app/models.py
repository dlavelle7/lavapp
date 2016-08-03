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
    budgets = db.relationship("Budget", backref='user')

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


class Budget(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    incomes = db.relationship("Income", backref='budget')
    expenses = db.relationship("Expense", backref='budget')
    date_created = db.Column(db.DateTime)

    def __init__(self, name, user_id):
        self.name = name
        self.user_id = user_id
        self.date_created = datetime.datetime.now()

    @property
    def formatted_date_created(self):
        return format_date(self.date_created)

    def _total_income(self):
        return sum(income.total for income in self.incomes)

    @property
    def total_income(self):
        return round_for_currency(self._total_income())

    def _total_expense(self):
        return sum(expense.total for expense in self.expenses)

    @property
    def total_expense(self):
        return round_for_currency(self._total_expense())

    @property
    def balance(self):
        return round_for_currency(self._balance())

    def _balance(self):
        return self._total_income() - self._total_expense()


class Sum(db.Model):

    __tablename__ = "sum"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    amount = db.Column(db.Numeric)  # Decimal for precision with finances
    date_created = db.Column(db.DateTime)
    interval = db.Column(db.String(64))
    budget_id = db.Column(db.Integer, db.ForeignKey('budget.id'))

    type = db.Column(db.String(50))
    __mapper_args__ = {
        'polymorphic_identity':'sum',
        'polymorphic_on':type
    }

    def __init__(self, name, amount, budget_id, interval):
        self.name = name
        self.amount = amount
        self.budget_id = budget_id
        self.date_created = datetime.datetime.now()
        self.interval = interval

    @property
    def total(self):
        options = {
            "weekly": lambda amount: amount * 4,
            "fortnightly": lambda amount: amount * 2,
            "monthly": lambda amount: amount,
            "bimonthly": lambda amount: amount / 2,
            "quarterly": lambda amount: amount / 3,
            "yearly": lambda amount: amount / 12,
        }
        return options.get(self.interval)(self.amount)

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
    shared_by = db.Column(db.Integer)
    __mapper_args__ = {
        'polymorphic_identity':'expense',
    }

    def __init__(self, name, amount, budget_id, interval, shared_by):
        super(Expense, self).__init__(name, amount, budget_id, interval)
        self.shared_by = shared_by

    @property
    def total(self):
        return super(Expense, self).total / self.shared_by
