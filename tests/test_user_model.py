import base_test
from app import db
from app.models import User, Income, Expense
from sqlalchemy.exc import IntegrityError
from decimal import Decimal


class TestUser(base_test.BaseTest):

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
        john2 = User(username='john', password='password',
                email='john22@bar.com')
        db.session.add(john2)
        self.assertRaises(IntegrityError, db.session.commit)
        db.session.rollback()

        all_johns = User.query.filter(User.username == user.username).all()
        self.assertTrue(len(all_johns), 1)
        self.assertEqual(user, all_johns[0])


