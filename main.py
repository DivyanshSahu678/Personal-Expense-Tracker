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
        print("4. Expense Summary")
        print("5. Delete Expense")
        print("6. Exit")

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
            delete_expense()

        elif choice == "6":
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
        expense_id = int(input("\nEnter Expense ID to delete: "))

        deleted = service.delete_expense(expense_id)

        if deleted:
            console.print("\n[green]✅ Expense deleted successfully![/green]")
        else:
            console.print("\n[red]❌ Invalid Expense ID.[/red]")

    except ValueError:
        console.print("\n[red]Please enter a valid numeric ID.[/red]")

create_table()
print("Database Created")
menu()