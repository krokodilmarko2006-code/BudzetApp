from fastapi import APIRouter, HTTPException
from app.database.db import get_connection
from app.models.user import UserCreate
from app.utils.security import hash_password
router = APIRouter(prefix="/auth", tags=["Auth"])
@router.post("/register")
def register(user: UserCreate):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    try:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (user.username, hash_password(user.password))
        )
        conn.commit()
    except:
        raise HTTPException(status_code=400, detail="Korisnik već postoji")
    return {"message": "Registracija uspešna"}
from app.models.user import UserLogin

@router.post("/login")
def login(user: UserLogin):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (user.username,))
    db_user = cursor.fetchone()

    if not db_user:
        raise HTTPException(status_code=400, detail="Korisnik ne postoji")

    if db_user["password"] != hash_password(user.password):
        raise HTTPException(status_code=400, detail="Pogresna sifra")

    return {
        "id": db_user["id"],
        "username": db_user["username"]
    }
