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
    
    def __init__(self, filename="expenses.json"):
        self.filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
        self.expenses = []
        self.load_expenses()
    
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
    
    def add_expense(self, amount, category, note):
        expense = Expense(amount, category, note)
        self.expenses.append(expense)
        self.save_expenses()
    
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

# ---------- Reporting methods ----------

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
        """Prints a full summary report."""
        if not self.expenses:
            print("No expenses to report.\n")
            return
        
        print("\n=== Expense Report ===")
        print(f"Total spent: ₹{self.total_spent():.2f}")
        
        print("\nSpend by category:")
        for category, amount in sorted(self.spend_by_category().items(), key=lambda x: -x[1]):
            print(f"  {category}: ₹{amount:.2f}")
        
        top = self.highest_expense()
        print(f"\nHighest single expense: {top}")
        print()


def get_valid_amount():
    while True:
        try:
            return float(input("Enter amount: "))
        except ValueError:
            print("Invalid amount. Please enter a number.\n")


def main():
    tracker = ExpenseTracker()
    
    while True:
        print("Expense Tracker")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Delete Expense")
        print("4. Generate Report")
        print("5. Filter by Date Range")
        print("6. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            amount = get_valid_amount()
            category = input("Enter category (Food/Travel/Bills/etc): ")
            note = input("Enter note (optional): ")
            tracker.add_expense(amount, category, note)
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
            print("Goodbye!")
            break
                
        else:
            print("Invalid choice, try again.\n")

main()