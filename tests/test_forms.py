import os
import unittest
from app import app
from app.forms import IncomeForm


class TestForms(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False

    def test_income_form(self):
        with app.app_context():
            form = IncomeForm(name='foo', interval='monthly', amount=123.123)
