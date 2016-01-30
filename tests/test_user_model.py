import os
import unittest
from app import app, db
from app.models import User
from config import basedir
from sqlalchemy.exc import IntegrityError


class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_user(self):
        # Create a new user
        user = User(username='john', password='pass')
        db.session.add(user)
        db.session.commit()

        self.assertTrue(type(user.id), int)
        self.assertEqual(user.username, 'john')
        self.assertNotEqual(user.password, 'pass')
        self.assertFalse(user.check_password('foo'))
        self.assertTrue(user.check_password('pass'))
        self.assertEqual(user.get_id(), u'1')
        
        # Try create another john
        john2 = User(username='john', password='password')
        db.session.add(john2)
        self.assertRaises(IntegrityError, db.session.commit)
        db.session.rollback()

        all_johns = User.query.filter(User.username == user.username).all()
        self.assertTrue(len(all_johns), 1)
        self.assertEqual(user, all_johns[0])
