import base_test
from app import app
from app.forms import IncomeForm, ExpenseForm


class TestForms(base_test.BaseTest):

    def test_income_form(self):
        with app.app_context():
            # Assert correct argument values
            ex_form = ExpenseForm(name='bar', interval='weekly', amount=100.0,
                    shared_by=2)
            expect = {'amount': 100.0, 'interval': u'weekly', 'shared_by': 2,
                    'name': 'bar'}
            self.assertEqual(expect, ex_form.data)
