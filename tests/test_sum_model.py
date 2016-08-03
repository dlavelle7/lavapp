from app import db
from app.models import Income, Expense, round_for_currency, Budget
import base_test
import datetime
from decimal import Decimal


class TestSum(base_test.BaseTest):

    def test_income(self):
        budget = Budget("Plan-A", 1)
        db.session.add(budget)
        db.session.commit()

        # Create a new income
        self.assertEqual('0.00', budget.total_income)
        income = Income(name='salary', amount=Decimal('4321.09'),
                budget_id=budget.id, interval='weekly')
        db.session.add(income)
        db.session.commit()
        self.assertTrue(income in budget.incomes)

        income2 = Income(name='investment', amount=Decimal('123.0'),
                budget_id=budget.id, interval='weekly')
        db.session.add(income2)
        db.session.commit()
        self.assertTrue(income2 in budget.incomes)
        self.assertEquals(2, len(budget.incomes)) # lazy 'select' returns list
        self.assertEquals(budget.incomes[0].budget, budget) # 'backref'

    def test_total_property(self):
        income = Income(name='salary', amount=Decimal('600.0'),
                budget_id=100, interval='weekly')
        # Assert with weekly interval total = amount x 4
        self.assertEqual(2400.0, income.total)

        # Assert with fortnightly interval total = amount x 2
        income.interval = "fortnightly"
        self.assertEqual(1200.0, income.total)

        # Assert with monthly interval total = amount
        income.interval = 'monthly'
        self.assertEqual(600.0, income.total)

        # Assert with bimonthly interval total = amount / 2
        income.interval = "bimonthly"
        self.assertEqual(300.0, income.total)

        # Assert with quarterly interval total = amount / 3
        income.interval = "quarterly"
        self.assertEqual(200.0, income.total)

        # Assert with yearly interval total = amount / 12
        income.interval = "yearly"
        self.assertEqual(50.0, income.total)

    def test_rounded_total_property(self):
        income = Income(name='salary', amount=Decimal(2.222), budget_id=100,
                interval='weekly')
        self.assertEqual('8.89', income.rounded_total)
        income = Income(name='salary', amount=Decimal(123.455), budget_id=100,
                interval='monthly')
        self.assertEqual('123.45', income.rounded_total)
        income.amount = Decimal(1.200)
        self.assertEqual('1.20', income.rounded_total)
        income = Income(name='salary', amount=Decimal(120.12), budget_id=100,
                interval='yearly')
        self.assertEqual('10.01', income.rounded_total)

    def test_round_for_currency(self):
        self.assertEqual('50,000,000.00', round_for_currency(50000000))
        self.assertEqual('5,000,000.00', round_for_currency(5000000))
        self.assertEqual('5,000.00', round_for_currency(5000))
        self.assertEqual('500.00', round_for_currency(500))

    def test_sum_date(self):
        income = Income(name='salary', amount=Decimal('123'), budget_id=100,
                interval='weekly')
        income.date_created = datetime.datetime(2000, 12, 28, 04, 50)
        self.assertEqual(income.formatted_date_created, '28-12-2000')

    def test_expense(self):
        budget = Budget("Plan-A", 1)
        db.session.add(budget)
        db.session.commit()

        self.assertEqual('0.00', budget.total_expense)
        expense = Expense(name='rent', amount=Decimal(1250.0), budget_id=budget.id,
                interval='monthly', shared_by=2)
        self.assertEqual(expense.total, 625.0)
        expense2 = Expense(name='UPC', amount=Decimal(60.0), budget_id=budget.id,
                interval='monthly', shared_by=2)
        self.assertEqual(expense2.total, 30.0)
        db.session.add(expense)
        db.session.add(expense2)
        db.session.commit()

        self.assertEqual(2, len(budget.expenses))
        self.assertTrue(expense in budget.expenses)
        self.assertTrue(expense in budget.expenses)
        self.assertEqual(expense.budget, budget)

        self.assertEqual(budget.total_expense, '655.00')

        expense3 = Expense(name='Water', amount=Decimal(60.0), budget_id=budget.id,
                interval='quarterly', shared_by=2)
        self.assertEqual(expense3.total, 10.0)
