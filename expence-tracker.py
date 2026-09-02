from datetime import datetime
import json
import os

FILENAME = "expenses.json" #store expenses here
expenses = []  # our in-memory storage

def load_expenses():
    """Load expenses from file when program starts."""
    global expenses
    if os.path.exists(FILENAME):
        try:
            with open(FILENAME, "r") as file:
                expenses = json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            expenses = []
    else:
        expenses = []

def save_expenses():
    """Save current expenses list to file."""
    with open(FILENAME, "w") as file:
        json.dump(expenses, file, indent=4)

def add_expense():
    # Input validation for amount
    while True:
        try:
            amount = float(input("Enter amount: "))
            break
        except ValueError:
            print("Invalid amount. Please enter a number.\n")

    category = input("Enter category (Food/Travel/Bills/etc): ")
    note = input("Enter note (optional): ")
    date = datetime.now().strftime("%Y-%m-%d")
    
    expense = {
        "amount": amount,
        "category": category,
        "note": note,
        "date": date
    }
    expenses.append(expense)
    save_expenses()   # save immediately after adding
    print("Expense added!\n")

def view_expenses():
    if not expenses:
        print("No expenses yet.\n")
        return
    
    print("\n--- All Expenses ---")
    for i, exp in enumerate(expenses, start=1):
        print(f"{i}. ₹{exp['amount']} | {exp['category']} | {exp['date']} | {exp['note']}")
    print()

def delete_expense():
    view_expenses()
    if not expenses:
        return
    
    try:
        index = int(input("Enter the number of the expense to delete: "))
        if 1 <= index <= len(expenses):
            removed = expenses.pop(index - 1)
            save_expenses()   # save immediately after deleting
            print(f"Deleted: ₹{removed['amount']} | {removed['category']}\n")
        else:
            print("Invalid expense number.\n")
    except ValueError:
        print("Please enter a valid number.\n")

def main():
    load_expenses()   # load saved data as soon as program starts
    while True:
        print("Expense Tracker")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Delete Expense")
        print("4. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            delete_expense()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.\n")

main()