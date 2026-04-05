from sqlmodel import SQLModel, Field
from typing import Optional
from enum import Enum
from datetime import date

class RecordType(str, Enum):
    INCOME = "Income"
    EXPENSE = "Expense"

class FinancialRecord(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    amount: float = Field(nullable=False)
    type: RecordType = Field(nullable=False)
    category: str = Field(nullable=False)
    record_date: date = Field(default_factory=date.today)
    notes: Optional[str] = None
    created_by: int = Field(foreign_key="user.id")
