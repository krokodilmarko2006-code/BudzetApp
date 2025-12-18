from fastapi import APIRouter
from pydantic import BaseModel
from app.database.db import get_connection

router = APIRouter(prefix="/expenses", tags=["Expenses"])


class ExpenseCreate(BaseModel):
    user_id: int
    name: str
    amount: float
    category: str
    date: str


@router.post("/")
def add_expense(expense: ExpenseCreate):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT,
            amount REAL,
            category TEXT,
            date TEXT
        )
    """)

    cursor.execute("""
        INSERT INTO expenses (user_id, name, amount, category, date)
        VALUES (?, ?, ?, ?, ?)
    """, (
        expense.user_id,
        expense.name,
        expense.amount,
        expense.category,
        expense.date
    ))

    conn.commit()
    return {"message": "Trošak dodat"}

@router.get("/{user_id}")
def get_expenses(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM expenses WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()

    expenses = []
    for row in rows:
        expenses.append({
            "id": row["id"],
            "name": row["name"],
            "amount": row["amount"],
            "category": row["category"],
            "date": row["date"]
        })

    return expenses


class IncomeCreate(BaseModel):
    user_id: int
    amount: float
    date: str

@router.post("/incomes/")
def add_income(income: IncomeCreate):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS incomes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            amount REAL,
            date TEXT
        )
    """)

    cursor.execute(
        "INSERT INTO incomes (user_id, amount, date) VALUES (?, ?, ?)",
        (income.user_id, income.amount, income.date)
    )
    conn.commit()
    return {"message": "Prihod dodat"}

@router.get("/incomes/{user_id}")
def get_incomes(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM incomes WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()

    incomes = []
    for row in rows:
        incomes.append({
            "id": row["id"],
            "amount": row["amount"],
            "date": row["date"]
        })

    return incomes
