from app import db
from app.models import User, Income, Expense, round_for_currency
from decimal import Decimal
import base_test
import datetime


# TODO: Fix Decimal income amounts

class TestSum(base_test.BaseTest):

    def test_monthly_income(self):
        # Create a new user
        # TODO: Put john in base test
        user = User(username='john', password='pass', email='john@foo.com')
        db.session.add(user)
        db.session.commit()

        # Create a new income
        self.assertEqual('0.00', user.total_income)
        income = Income(name='salary', amount=Decimal('4321.09'),
                user_id=user.id, interval='weekly')
        db.session.add(income)
        db.session.commit()
        self.assertTrue(income in user.incomes)

        income = Income.query.filter(Income.name == 'salary').first()
        self.assertEquals(income.name, 'salary')
        self.assertEquals(income.amount, Decimal('4321.09'))
        self.assertEquals(income.user_id, 1)

        income2 = Income(name='investment', amount=Decimal('123.0'),
                user_id=user.id, interval='weekly')
        db.session.add(income2)
        db.session.commit()
        self.assertTrue(income2 in user.incomes)
        self.assertEquals(2, len(user.incomes)) # lazy 'select' returns list
        self.assertEquals(user.incomes[0].user, user) # 'backref'
        self.assertEquals(income2.amount, Decimal('123.0'))

    def test_total_property(self):
        income = Income(name='salary', amount=Decimal('100.1'),
                user_id=100, interval='weekly')
        # Assert with weekly interval total = amount x 4
        self.assertEqual(income.total, income.amount * 4)

        # Assert with fortnightly interval total = amount x 2
        income.interval = "fortnightly"
        self.assertEqual(income.total, income.amount * 2)

        # Assert with monthly interval total = amount
        income.interval = 'monthly'
        self.assertEqual(income.total, income.amount)

        # Assert with bimonthly interval total = amount / 2
        income.interval = "bimonthly"
        self.assertEqual(income.total, income.amount / 2)

        # Assert with quarterly interval total = amount / 3
        income.interval = "quarterly"
        self.assertEqual(income.total, income.amount / 3)

        # Assert with yearly interval total = amount / 12
        income.interval = "yearly"
        self.assertEqual(income.total, income.amount / 12)

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
        self.assertEqual('50,000,000.00', round_for_currency(50000000))
        self.assertEqual('5,000,000.00', round_for_currency(5000000))
        self.assertEqual('5,000.00', round_for_currency(5000))
        self.assertEqual('500.00', round_for_currency(500))

    def test_sum_date(self):
        income = Income(name='salary', amount=Decimal('123'), user_id=100,
                interval='weekly')
        income.date_created = datetime.datetime(2000, 12, 28, 04, 50)
        self.assertEqual(income.formatted_date_created, '28-12-2000')

    def test_expense(self):
        user = User(username='john', password='pass', email='john@foo.com')
        db.session.add(user)
        db.session.commit()

        self.assertEqual('0.00', user.total_expense)
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
