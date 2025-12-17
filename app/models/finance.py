from pydantic import BaseModel

class ExpenseCreate(BaseModel):
    name: str
    amount: float
    category: str
    date: str

class IncomeCreate(BaseModel):
    amount: float
    date: str
