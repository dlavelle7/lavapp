from app import db
from app.models import User, Income, Expense, round_for_currency, Budget
import base_test
import datetime
from decimal import Decimal


class TestBudget(base_test.BaseTest):

    def test_budget(self):
        # Create a new user
        user = User(username='john', password='pass', email='john@foo.com')
        db.session.add(user)
        db.session.commit()

        # Create a new budget for user john
        budget = Budget("Plan-A", user.id)
        db.session.add(budget)
        db.session.commit()
        self.assertEqual("Plan-A", budget.name)
        self.assertEqual(budget.user, user)
        self.assertEqual(budget.user_id, user.id)

        # Create an Income for the budget
        income = Income(name='salary', amount=Decimal('4321.09'),
                budget_id=budget.id, interval='weekly')
        db.session.add(income)
        db.session.commit()
        self.assertTrue(income in budget.incomes)
        self.assertEqual(income.budget, budget)
        self.assertEqual(income.budget_id, budget.id)

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
