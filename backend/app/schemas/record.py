from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import date
from app.models.record import RecordType

class RecordBase(BaseModel):
    amount: float = Field(gt=0, description="Amount must be positive")
    type: RecordType
    category: str
    record_date: date
    notes: Optional[str] = None

class RecordCreate(RecordBase):
    pass

class RecordUpdate(BaseModel):
    amount: Optional[float] = None
    type: Optional[RecordType] = None
    category: Optional[str] = None
    record_date: Optional[date] = None
    notes: Optional[str] = None

class RecordResponse(RecordBase):
    id: int
    created_by: int

    model_config = ConfigDict(from_attributes=True)

class DashboardSummaryResponse(BaseModel):
    total_income: float
    total_expenses: float
    net_balance: float
    category_totals: dict[str, float]
    recent_activity: list[RecordResponse]
    monthly_trends: dict[str, float]
