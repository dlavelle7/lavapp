import os
import unittest
from app import app, db
from app.models import User, Income, Expense
from config import basedir
from sqlalchemy.exc import IntegrityError


class TestUser(unittest.TestCase):
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

    def test_user(self):
        # Create a new user
        user = User(username='john', password='pass', email='john@foo.com')
        db.session.add(user)
        db.session.commit()

        self.assertEqual(user.id, 1)
        self.assertEqual(user.username, 'john')
        self.assertEqual(user.email, 'john@foo.com')
        self.assertNotEqual(user.password, 'pass')
        self.assertFalse(user.verify_password('foo'))
        self.assertTrue(user.verify_password('pass'))
        self.assertEqual(user.get_id(), u'1')

        # Retrieve user
        user = User.query.filter(User.username == 'john').first()
        self.assertEqual(user.id, 1)
        self.assertEqual(user.username, 'john')
        self.assertEqual(user.email, 'john@foo.com')
        self.assertNotEqual(user.password, 'pass')
        self.assertFalse(user.verify_password('foo'))
        self.assertTrue(user.verify_password('pass'))
        
        # Try create another john
        john2 = User(username='john', password='password', email='john22@bar.com')
        db.session.add(john2)
        self.assertRaises(IntegrityError, db.session.commit)
        db.session.rollback()

        all_johns = User.query.filter(User.username == user.username).all()
        self.assertTrue(len(all_johns), 1)
        self.assertEqual(user, all_johns[0])

    def test_total_income(self):
        user = User(username='john', password='pass', email='john@foo.com')
        db.session.add(user)
        db.session.commit()
        income = Income(name='salary', amount=100, user_id=user.id,
                interval='weekly')
        db.session.add(income)
        income2 = Income(name='investment', amount=555, user_id=user.id,
                interval='monthly')
        db.session.add(income2)
        db.session.commit()
        self.assertEqual('955.00', user.total_income)

        db.session.delete(income2)
        db.session.commit()
        self.assertEqual('400.00', user.total_income)

    def test_balance(self):
        user = User(username='john', password='pass', email='john@foo.com')
        db.session.add(user)
        db.session.commit()

        income = Income(name='salary', amount=100, user_id=user.id,
                interval='weekly')
        db.session.add(income)
        income2 = Income(name='investment', amount=555, user_id=user.id,
                interval='monthly')
        db.session.add(income2)
        db.session.commit()
        self.assertEqual('955.00', user.total_income)
        self.assertEqual('955.00', user.balance)

        expense = Expense(name='rent', amount=1250.0, user_id=user.id,
                interval='monthly', shared_by=2)
        self.assertEqual(expense.total, 625)
        db.session.add(expense)
        db.session.commit()


        self.assertEqual('330.00', user.balance)

        expense2 = Expense(name='UPC', amount=60.0, user_id=user.id,
                interval='monthly', shared_by=2)
        self.assertEqual(expense2.total, 30)
        db.session.add(expense2)
        db.session.commit()

        self.assertEqual('300.00', user.balance)
