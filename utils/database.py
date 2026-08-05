import sqlite3

DATABASE_NAME = "data/expenses.db"


def get_connection():
    """Create and return database connection"""
    return sqlite3.connect(DATABASE_NAME, timeout=10)


def create_table():
    """Create expenses table if it doesn't exist"""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()