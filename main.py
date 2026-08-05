from rich.console import Console
from rich.table import Table
from datetime import datetime

from models.expense import Expense
from services.expense_service import ExpenseService
from utils.database import create_table


service = ExpenseService()
console = Console()


def add_expense():

    print("\n------ Add Expense ------")

    title = input("Enter Title : ")

    amount = float(input("Enter Amount : "))

    category = input("Enter Category : ")

    date = input("Enter Date (YYYY-MM-DD): ")

    if date == "":
        date = datetime.today().strftime("%Y-%m-%d")

    expense = Expense(
        title,
        amount,
        category,
        date
    )

    service.add_expense(expense)


def menu():

    while True:

        print("\n========== Personal Expense Tracker ==========")

        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Search by Category")
        print("4. Exit")

        choice = input("\nEnter Choice : ")

        if choice == "1":
            add_expense()

        elif choice == "2":
            view_expenses()

        elif choice == "3":
            search_expenses()

        elif choice == "4":
            print("\nThank You ❤️")
            break

        else:
            print("\nInvalid Choice")

def view_expenses():

    expenses = service.get_all_expenses()

    if not expenses:
        console.print("\n[red]No expenses found![/red]")
        return

    display_table(expenses, "All Expenses")
    
def display_table(expenses, title="Expenses"):

    table = Table(title=title)

    table.add_column("ID", style="cyan", justify="center")
    table.add_column("Title", style="green")
    table.add_column("Amount", style="yellow", justify="right")
    table.add_column("Category", style="magenta")
    table.add_column("Date", style="blue")

    for expense in expenses:
        table.add_row(
            str(expense[0]),
            expense[1],
            f"₹{expense[2]:.2f}",
            expense[3],
            expense[4]
        )

    console.print(table)
    
def search_expenses():

    category = input("\nEnter Category : ").strip()

    expenses = service.search_by_category(category)

    if not expenses:
        console.print(f"\n[red]No expenses found in '{category}' category.[/red]")
        return

    display_table(expenses, f"Category: {category}")

create_table()
print("Database Created")
menu()