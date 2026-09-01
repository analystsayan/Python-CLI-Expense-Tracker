expenses = []  # our in-memory storage

def add_expense():
    amount = float(input("Enter amount: "))
    category = input("Enter category (Food/Travel/Bills/etc): ")
    note = input("Enter note (optional): ")
    
    expense = {
        "amount": amount,
        "category": category,
        "note": note
    }
    expenses.append(expense)
    print("Expense added!\n")

def view_expenses():
    if not expenses:
        print("No expenses yet.\n")
        return
    
    print("\n--- All Expenses ---")
    for i, exp in enumerate(expenses, start=1):
        print(f"{i}. ₹{exp['amount']} | {exp['category']} | {exp['note']}")
    print()

def main():
    while True:
        print("Expense Tracker")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.\n")

main()