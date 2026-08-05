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
        print("3. Exit")

        choice = input("\nEnter Choice : ")

        if choice == "1":
            add_expense()

        elif choice == "2":
            view_expenses()

        elif choice == "3":
            print("\nThank You ❤️")
            break

        else:
            print("\nInvalid Choice")

def view_expenses():

    expenses = service.get_all_expenses()

    if not expenses:
        console.print("\n[red]No expenses found![/red]")
        return

    table = Table(title="All Expenses")

    table.add_column("ID", style="cyan")
    table.add_column("Title", style="green")
    table.add_column("Amount", style="yellow")
    table.add_column("Category", style="magenta")
    table.add_column("Date", style="blue")

    for expense in expenses:
        table.add_row(
            str(expense[0]),
            expense[1],
            f"₹{expense[2]}",
            expense[3],
            expense[4]
        )

    console.print(table)

create_table()
print("Database Created")
menu()