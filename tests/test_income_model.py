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
        mincome = Income(name='salary', amount=4321.09, user_id=user.id)
        db.session.add(mincome)
        db.session.commit()
        self.assertTrue(mincome in user.incomes)

        mincome = Income.query.filter(Income.name == 'salary').first()
        self.assertEquals(mincome.name, 'salary')
        self.assertEquals(mincome.amount, 4321.09)
        self.assertEquals(mincome.user_id, 1)

        mincome2 = Income(name='investment', amount=123, user_id=user.id)
        db.session.add(mincome2)
        db.session.commit()
        self.assertTrue(mincome2 in user.incomes)
        self.assertEquals(2, len(user.incomes)) # lazy 'select' returns list
        self.assertEquals(user.incomes[0].user, user) # 'backref'
