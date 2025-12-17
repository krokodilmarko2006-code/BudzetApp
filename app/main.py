from fastapi import FastAPI
from app.routers import auth
from app.routers import expenses


app = FastAPI(title="Expense Tracker API")

app.include_router(auth.router)
app.include_router(expenses.router)

@app.get("/")
def root():
    return {"message": "API radi"}
