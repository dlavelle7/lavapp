from app import db
from app.models import Income, Expense, round_for_currency, Budget
import base_test
import datetime
from decimal import Decimal


class TestBudget(base_test.BaseTest):

    def test_budget(self):
        # Create a new budget budget 
        budget = Budget("Plan-A", 1)
        db.session.add(budget)
        db.session.commit()
        self.assertEqual("Plan-A", budget.name)

        # Create an Income for the budget
        income = Income(name='salary', amount=Decimal('4321.09'),
                budget_id=budget.id, interval='weekly')
        db.session.add(income)
        db.session.commit()
        self.assertTrue(income in budget.incomes)
        self.assertEqual(income.budget, budget)

        # Create an Expense for the budget
        expense = Expense(name='rent', amount=Decimal(1250.0), budget_id=budget.id,
                interval='monthly', shared_by=2)
        self.assertEqual(expense.total, 625.0)
        expense2 = Expense(name='UPC', amount=Decimal(60.0), budget_id=budget.id,
                interval='monthly', shared_by=2)
        self.assertEqual(expense2.total, 30.0)
        db.session.add(expense)
        db.session.add(expense2)
        db.session.commit()
        self.assertEqual(sorted([expense, expense2]), sorted(budget.expenses))

    def test_total_income(self):
        budget = Budget("Plan-A", 1)
        db.session.add(budget)
        db.session.commit()

        income = Income(name='salary', amount=Decimal(100), budget_id=budget.id,
                interval='weekly')
        db.session.add(income)
        income2 = Income(name='investment', amount=Decimal(555),
                budget_id=budget.id, interval='monthly')
        db.session.add(income2)
        db.session.commit()
        self.assertEqual('955.00', budget.total_income)

        db.session.delete(income2)
        db.session.commit()
        self.assertEqual('400.00', budget.total_income)

    def test_balance(self):
        budget = Budget("Plan-A", 1)
        db.session.add(budget)
        db.session.commit()

        income = Income(name='salary', amount=Decimal(100), budget_id=budget.id,
                interval='weekly')
        db.session.add(income)
        income2 = Income(name='investment', amount=Decimal(555),
                budget_id=budget.id, interval='monthly')
        db.session.add(income2)
        db.session.commit()
        self.assertEqual('955.00', budget.total_income)
        self.assertEqual('955.00', budget.balance)

        expense = Expense(name='rent', amount=Decimal(1250.0), budget_id=budget.id,
                interval='monthly', shared_by=2)
        self.assertEqual(expense.total, 625.0)
        db.session.add(expense)
        db.session.commit()

        self.assertEqual('330.00', budget.balance)

        expense2 = Expense(name='UPC', amount=Decimal(60.0), budget_id=budget.id,
                interval='monthly', shared_by=2)
        self.assertEqual(expense2.total, 30.0)
        db.session.add(expense2)
        db.session.commit()

        self.assertEqual('300.00', budget.balance)
