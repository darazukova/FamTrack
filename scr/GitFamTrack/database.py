"""Слой данных FamTrack: работа с базой данных SQLite."""
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / "famtrack.db"
SCHEMA_PATH = BASE_DIR / "schema.sql"


def get_connection():
    """Открывает соединение с базой и включает проверку внешних ключей."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Создаёт таблицы и тестовые данные, выполняя schema.sql."""
    with get_connection() as conn:
        conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))


def get_users():
    """Пользователи вместе с названием роли."""
    with get_connection() as conn:
        return conn.execute("""
            SELECT u.user_id, u.full_name, u.login, r.name
            FROM users u
            JOIN user_roles r ON u.role_id = r.role_id
        """).fetchall()


def get_expenses():
    """История расходов: кто, на что, сколько и когда."""
    with get_connection() as conn:
        return conn.execute("""
            SELECT e.expense_id, e.expense_date, u.full_name,
                   c.name, e.amount, e.description
            FROM expenses e
            JOIN users u ON e.user_id = u.user_id
            JOIN categories c ON e.category_id = c.category_id
            ORDER BY e.expense_date, e.expense_id
        """).fetchall()


def get_totals_by_category():
    """Сумма расходов по каждой категории."""
    with get_connection() as conn:
        return conn.execute("""
            SELECT c.name, SUM(e.amount)
            FROM expenses e
            JOIN categories c ON e.category_id = c.category_id
            GROUP BY c.name
            ORDER BY SUM(e.amount) DESC
        """).fetchall()
