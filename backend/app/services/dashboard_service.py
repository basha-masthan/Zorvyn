from sqlmodel import Session, select
from sqlalchemy import func
from app.models.record import FinancialRecord, RecordType
from app.schemas.record import DashboardSummaryResponse

class DashboardService:
    @staticmethod
    def get_summary(db: Session) -> DashboardSummaryResponse:
        income_query = select(func.sum(FinancialRecord.amount)).where(FinancialRecord.type == RecordType.INCOME)
        income_val = db.exec(income_query).first()
        total_income = float(income_val) if income_val else 0.0
             
        expense_query = select(func.sum(FinancialRecord.amount)).where(FinancialRecord.type == RecordType.EXPENSE)
        expense_val = db.exec(expense_query).first()
        total_expenses = float(expense_val) if expense_val else 0.0
             
        category_query = select(FinancialRecord.category, func.sum(FinancialRecord.amount)).group_by(FinancialRecord.category)
        category_results = db.exec(category_query).all()
        
        category_totals = {category: float(total) for category, total in category_results}
        
        return DashboardSummaryResponse(
            total_income=total_income,
            total_expenses=total_expenses,
            net_balance=total_income - total_expenses,
            category_totals=category_totals
        )
