import os
import unittest
from app import app, db
from app.models import User, Income
from config import basedir


class TestUser(unittest.TestCase):

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

        income2 = Income(name='investment', amount=123, user_id=user.id,
                interval='weekly')
        db.session.add(income2)
        db.session.commit()
        self.assertTrue(income2 in user.incomes)
        self.assertEquals(2, len(user.incomes)) # lazy 'select' returns list
        self.assertEquals(user.incomes[0].user, user) # 'backref'

    def test_income_total_property(self):
        income = Income(name='salary', amount=100.05, user_id=100,
                interval='weekly')
        self.assertEqual(400.2, income.total)
        income.interval = 'monthly'
        self.assertEqual(100.05, income.total)
        income.interval = "yearly"
        income.amount = 560
        self.assertEqual(10, income.total)
