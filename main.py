from rich.console import Console
from rich.table import Table
from datetime import datetime
from rich.panel import Panel

from models.expense import Expense
from services.expense_service import ExpenseService
from utils.database import create_table


service = ExpenseService()
console = Console()


def add_expense():

    print("\n------ Add Expense ------")

    title = input("Enter Title : ").strip()

    if not title:
        console.print("[red]Title cannot be empty![/red]")
        return

    try:
        amount = float(input("Enter Amount : "))

        if amount <= 0:
            console.print("[red]Amount must be greater than 0![/red]")
            return

    except ValueError:
        console.print("[red]Please enter a valid amount![/red]")
        return

    category = input("Enter Category : ").strip()

    if not category:
        console.print("[red]Category cannot be empty![/red]")
        return

    date = input("Enter Date (YYYY-MM-DD) [Press Enter for Today]: ").strip()

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
        print("4. Expense Summary")
        print("5. Monthly Summary")
        print("6. Delete Expense")
        print("7. Exit")

        choice = input("\nEnter Choice : ")

        if choice == "1":
            add_expense()

        elif choice == "2":
            view_expenses()

        elif choice == "3":
            search_expenses()

        elif choice == "4":
            show_summary()
            
        elif choice == "5":
            monthly_summary()

        elif choice == "6":
            delete_expense()

        elif choice == "7":
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
    
def show_summary():

    summary = service.get_expense_summary()

    total_transactions = summary[0]
    total_amount = summary[1]
    average = summary[2]
    highest = summary[3]
    lowest = summary[4]

    console.print(
        Panel.fit(
            f"""
[bold cyan]Expense Summary[/bold cyan]

💰 Total Expenses      : ₹{total_amount:.2f}
🧾 Total Transactions : {total_transactions}
📊 Average Expense    : ₹{average:.2f}
📈 Highest Expense    : ₹{highest:.2f}
📉 Lowest Expense     : ₹{lowest:.2f}
""",
            title="Summary",
            border_style="green"
        )
    )
    
def delete_expense():

    expenses = service.get_all_expenses()

    if not expenses:
        console.print("\n[red]No expenses available to delete.[/red]")
        return

    display_table(expenses, "Select Expense to Delete")

    try:
            expense_id = int(input("\nEnter Expense ID: "))

    except ValueError:
        console.print("[red]Please enter a valid ID.[/red]")
        return
def monthly_summary():

    summary = service.get_monthly_summary()

    if not summary:
        console.print("\n[red]No expenses found![/red]")
        return

    table = Table(title="Monthly Expense Summary")

    table.add_column("Month", style="cyan")
    table.add_column("Transactions", style="green", justify="center")
    table.add_column("Total Amount", style="yellow", justify="right")

    for row in summary:
        table.add_row(
            row[0],
            str(row[1]),
            f"₹{row[2]:.2f}"
        )

    console.print(table)

create_table()
print("Database Created")
menu()