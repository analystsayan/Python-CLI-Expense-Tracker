from datetime import datetime
from collections import defaultdict
import json
import os

class Expense:
    """Represents a single expense record."""
    
    def __init__(self, amount, category, note, date=None):
        self.amount = amount
        self.category = category
        self.note = note
        self.date = date if date else datetime.now().strftime("%Y-%m-%d")
    
    def to_dict(self):
        """Convert this Expense object into a dictionary (for JSON saving)."""
        return {
            "amount": self.amount,
            "category": self.category,
            "note": self.note,
            "date": self.date
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create an Expense object from a dictionary (for JSON loading)."""
        return cls(data["amount"], data["category"], data["note"], data["date"])
    
    def __str__(self):
        """How this object looks when printed."""
        return f"₹{self.amount} | {self.category} | {self.date} | {self.note}"

class ExpenseTracker:
    """Manages the full collection of expenses: add, view, delete, save, load."""
    
    def __init__(self, filename="expenses.json", budget_filename="budgets.json"):
        self.filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
        self.budget_filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), budget_filename)
        self.expenses = []
        self.budgets = {}
        self.load_expenses()
        self.load_budgets()
    
    def load_expenses(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as file:
                    data = json.load(file)
                    self.expenses = [Expense.from_dict(item) for item in data]
            except (json.JSONDecodeError, FileNotFoundError):
                self.expenses = []
        else:
            self.expenses = []
    
    def save_expenses(self):
        with open(self.filename, "w") as file:
            data = [exp.to_dict() for exp in self.expenses]
            json.dump(data, file, indent=4)

    def load_budgets(self):
        if os.path.exists(self.budget_filename):
            try:
                with open(self.budget_filename, "r") as file:
                    self.budgets = json.load(file)
            except (json.JSONDecodeError, FileNotFoundError):
                self.budgets = {}
        else:
            self.budgets = {}
    
    def save_budgets(self):
        with open(self.budget_filename, "w") as file:
            json.dump(self.budgets, file, indent=4)
    
    def set_budget(self, category, limit):
        self.budgets[category] = limit
        self.save_budgets()
    
    def check_budget(self, category, totals=None):
        """Returns (spent, limit, over_budget: bool) for a category, or None if no budget set.

        Pass a precomputed `totals` dict (from spend_by_category()) to avoid
        recomputing category totals on every call, e.g. when checking many
        categories in a loop.
        """
        if category not in self.budgets:
            return None
        spent = (totals if totals is not None else self.spend_by_category()).get(category, 0.0)
        limit = self.budgets[category]
        return (spent, limit, spent > limit)
    
    def add_expense(self, amount, category, note):
        expense = Expense(amount, category, note)
        self.expenses.append(expense)
        self.save_expenses()

    def edit_expense(self, index, amount=None, category=None, note=None):
        """Update fields on an existing expense. Pass None to leave a field unchanged."""
        if 1 <= index <= len(self.expenses):
            exp = self.expenses[index - 1]
            if amount is not None:
                exp.amount = amount
            if category is not None:
                exp.category = category
            if note is not None:
                exp.note = note
            self.save_expenses()
            return exp
        return None
    
    def view_expenses(self):
        if not self.expenses:
            print("No expenses yet.\n")
            return
        print("\n--- All Expenses ---")
        for i, exp in enumerate(self.expenses, start=1):
            print(f"{i}. {exp}")
        print()
    
    def delete_expense(self, index):
        if 1 <= index <= len(self.expenses):
            removed = self.expenses.pop(index - 1)
            self.save_expenses()
            return removed
        return None

    def total_spent(self):
        """Sum of all expense amounts."""
        return sum(exp.amount for exp in self.expenses)

    def spend_by_category(self):
        """Returns a dict like {'Food': 450.0, 'Travel': 200.0}."""
        totals = defaultdict(float)
        for exp in self.expenses:
            totals[exp.category] += exp.amount
        return dict(totals)

    def highest_expense(self):
        """Returns the single largest Expense object, or None if empty."""
        if not self.expenses:
            return None
        return max(self.expenses, key=lambda exp: exp.amount)

    def filter_by_date_range(self, start_date, end_date):
        """Returns expenses where start_date <= date <= end_date (format: YYYY-MM-DD)."""
        return [exp for exp in self.expenses if start_date <= exp.date <= end_date]

    def generate_report(self):
        if not self.expenses:
            print("No expenses to report.\n")
            return
        
        print("\n=== Expense Report ===")
        print(f"Total spent: ₹{self.total_spent():.2f}")
        
        print("\nSpend by category:")
        # Compute totals once and reuse for every budget check below,
        # instead of recomputing spend_by_category() per category (O(n·k) -> O(n)).
        totals = self.spend_by_category()
        for category, amount in sorted(totals.items(), key=lambda x: -x[1]):
            print(f"  {category}: ₹{amount:.2f}")
            budget_check = self.check_budget(category, totals)
            if budget_check:
                spent, limit, over = budget_check
                if over:
                    print(f"    ⚠ Over budget! Limit was ₹{limit:.2f}")
                else:
                    print(f"    (Budget: ₹{limit:.2f}, remaining: ₹{limit - spent:.2f})")
        
        top = self.highest_expense()
        print(f"\nHighest single expense: {top}")
        print()

    def show_chart(self):
        """Display a bar chart of spending by category."""
        data = self.spend_by_category()
        if not data:
            print("No data to chart.\n")
            return

        # Imported here rather than at module level so the tracker starts up
        # fast and doesn't pull in matplotlib for people who never chart.
        import matplotlib.pyplot as plt

        categories = list(data.keys())
        amounts = list(data.values())
        
        plt.figure(figsize=(8, 5))
        plt.bar(categories, amounts, color="skyblue")
        plt.title("Spending by Category")
        plt.xlabel("Category")
        plt.ylabel("Amount (₹)")
        plt.tight_layout()
        plt.show()


def get_valid_amount():
    while True:
        try:
            value = float(input("Enter amount: "))
            if value <= 0:
                print("Amount must be greater than zero.\n")
                continue
            return value
        except ValueError:
            print("Invalid amount. Please enter a number.\n")


def get_valid_category(prompt="Enter category (Food/Travel/Bills/etc): "):
    """Normalizes category input (trims whitespace, consistent casing) so
    'Food', 'food', and 'FOOD ' don't fragment into separate categories."""
    while True:
        category = input(prompt).strip()
        if category:
            return category.title()
        print("Category can't be empty.\n")


def main():
    tracker = ExpenseTracker()
    
    while True:
        print("Expense Tracker")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Delete Expense")
        print("4. Generate Report")
        print("5. Filter by Date Range")
        print("6. Edit Expense")
        print("7. Set Budget")
        print("8. Show Chart")
        print("9. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            amount = get_valid_amount()
            category = get_valid_category()
            note = input("Enter note (optional): ")
            tracker.add_expense(amount, category, note)
            
            budget_check = tracker.check_budget(category)
            if budget_check:
                spent, limit, over = budget_check
                if over:
                    print(f"⚠ Warning: You're over budget for {category}! (₹{spent:.2f} / ₹{limit:.2f})")
            print("Expense added!\n")
        
        elif choice == "2":
            tracker.view_expenses()
        
        elif choice == "3":
            tracker.view_expenses()
            if tracker.expenses:
                try:
                    index = int(input("Enter the number of the expense to delete: "))
                    removed = tracker.delete_expense(index)
                    print(f"Deleted: {removed}\n" if removed else "Invalid expense number.\n")
                except ValueError:
                    print("Please enter a valid number.\n")
        
        elif choice == "4":
            tracker.generate_report()
        
        elif choice == "5":
            start = input("Start date (YYYY-MM-DD): ")
            end = input("End date (YYYY-MM-DD): ")
            results = tracker.filter_by_date_range(start, end)
            if results:
                print(f"\n--- Expenses from {start} to {end} ---")
                for exp in results:
                    print(exp)
                print()
            else:
                print("No expenses found in that range.\n")
        
        elif choice == "6":
            tracker.view_expenses()
            if tracker.expenses:
                try:
                    index = int(input("Enter the number of the expense to edit: "))
                    print("Leave blank to keep current value.")
                    new_amount_input = input("New amount: ")
                    new_category = input("New category: ")
                    new_note = input("New note: ")
                    
                    new_amount = float(new_amount_input) if new_amount_input.strip() else None
                    new_category = new_category.strip().title() if new_category.strip() else None
                    new_note = new_note if new_note.strip() else None
                    
                    updated = tracker.edit_expense(index, new_amount, new_category, new_note)
                    print(f"Updated: {updated}\n" if updated else "Invalid expense number.\n")
                except ValueError:
                    print("Invalid input.\n")
        
        elif choice == "7":
            category = get_valid_category("Category to set budget for: ")
            try:
                limit = float(input("Monthly budget limit: "))
                tracker.set_budget(category, limit)
                print(f"Budget set: {category} → ₹{limit:.2f}\n")
            except ValueError:
                print("Invalid amount.\n")
        
        elif choice == "8":
            tracker.show_chart()
        
        elif choice == "9":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice, try again.\n")


if __name__ == "__main__":
    main()