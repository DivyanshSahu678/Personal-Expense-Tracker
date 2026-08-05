from utils.database import get_connection


class ExpenseService:

    def add_expense(self, expense):
        conn = get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO expenses (title, amount, category, date)
                VALUES (?, ?, ?, ?)
            """, (
                expense.title,
                expense.amount,
                expense.category,
                expense.date
            ))

            conn.commit()
            print("\n✅ Expense Added Successfully!")

        except Exception as e:
            print(f"\n❌ Error: {e}")

        finally:
            conn.close()

    def get_all_expenses(self):
        conn = get_connection()

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM expenses")
            return cursor.fetchall()

        finally:
            conn.close()