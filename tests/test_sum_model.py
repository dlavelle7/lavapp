import os
import unittest
from app import app, db
from app.models import User, Income, Expense, round_for_currency
from config import basedir


class TestSum(unittest.TestCase):

    # TODO: This is duplicated
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
                basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_monthly_income(self):
        # Create a new user
        user = User(username='john', password='pass', email='john@foo.com')
        db.session.add(user)
        db.session.commit()

        # Create a new income
        income = Income(name='salary', amount=4321.09, user_id=user.id,
                interval='weekly')
        db.session.add(income)
        db.session.commit()
        self.assertTrue(income in user.incomes)

        income = Income.query.filter(Income.name == 'salary').first()
        self.assertEquals(income.name, 'salary')
        self.assertEquals(income.amount, 4321.09)
        self.assertEquals(income.user_id, 1)

        income2 = Income(name='investment', amount=123.0, user_id=user.id,
                interval='weekly')
        db.session.add(income2)
        db.session.commit()
        self.assertTrue(income2 in user.incomes)
        self.assertEquals(2, len(user.incomes)) # lazy 'select' returns list
        self.assertEquals(user.incomes[0].user, user) # 'backref'

    def test_total_property(self):
        income = Income(name='salary', amount=100.05, user_id=100,
                interval='weekly')
        self.assertEqual(400.2, income.total)
        income.interval = 'monthly'
        self.assertEqual(100.05, income.total)
        income.amount = 120.0
        income.interval = "yearly"
        self.assertEqual(10, income.total)
        income.amount = 350.00
        income.interval = "bimonthly"
        self.assertEqual(175.00, income.total)
        income.amount = 300.00
        income.interval = "quarterly"
        self.assertEqual(100.0, income.total)
        income.interval = "fortnightly"
        self.assertEqual(600.0, income.total)

    def test_rounded_total_property(self):
        income = Income(name='salary', amount=2.222, user_id=100,
                interval='weekly')
        self.assertEqual('8.89', income.rounded_total)
        income = Income(name='salary', amount=123.455, user_id=100,
                interval='monthly')
        self.assertEqual('123.45', income.rounded_total)
        income.amount = 1.200
        self.assertEqual('1.20', income.rounded_total)
        income = Income(name='salary', amount=120.12, user_id=100,
                interval='yearly')
        self.assertEqual('10.01', income.rounded_total)

    def test_round_for_currency(self):
        self.assertEqual('5,000,000.00', round_for_currency(5000000))

    def test_expense(self):
        user = User(username='john', password='pass', email='john@foo.com')
        db.session.add(user)
        db.session.commit()

        expense = Expense(name='rent', amount=1250.0, user_id=user.id,
                interval='monthly', shared_by=2)
        self.assertEqual(expense.total, 625)
        expense2 = Expense(name='UPC', amount=60.0, user_id=user.id,
                interval='monthly', shared_by=2)
        self.assertEqual(expense2.total, 30)
        db.session.add(expense)
        db.session.add(expense2)
        db.session.commit()

        self.assertEqual(2, len(user.expenses))
        self.assertTrue(expense in user.expenses)
        self.assertTrue(expense in user.expenses)
        self.assertEqual(expense.user, user)

        self.assertEqual(user.total_expense, '655.00')

        expense3 = Expense(name='Water', amount=60.0, user_id=user.id,
                interval='quarterly', shared_by=2)
        self.assertEqual(expense3.total, 10.0)
