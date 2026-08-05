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
            
    def search_by_category(self, category):
        conn = get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT * FROM expenses
                WHERE LOWER(category) = LOWER(?)
            """, (category,))

            return cursor.fetchall()

        finally:
            conn.close()
            
    def get_expense_summary(self):
        conn = get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    COUNT(*),
                    COALESCE(SUM(amount), 0),
                    COALESCE(AVG(amount), 0),
                    COALESCE(MAX(amount), 0),
                    COALESCE(MIN(amount), 0)
                FROM expenses
            """)

            return cursor.fetchone()

        finally:
            conn.close()    
            