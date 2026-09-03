from datetime import datetime
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
        print("4. Exit")
        
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
                    if removed:
                        print(f"Deleted: {removed}\n")
                    else:
                        print("Invalid expense number.\n")
                except ValueError:
                    print("Please enter a valid number.\n")
        
        elif choice == "4":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice, try again.\n")


main()