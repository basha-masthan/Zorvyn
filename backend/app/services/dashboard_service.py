from sqlmodel import Session, select
from sqlalchemy import func, desc, text
from app.models.record import FinancialRecord, RecordType
from app.schemas.record import DashboardSummaryResponse

class DashboardService:
    @staticmethod
    def get_summary(db: Session) -> DashboardSummaryResponse:
        income_query = select(func.sum(FinancialRecord.amount)).where(FinancialRecord.type == RecordType.INCOME)
        income_val = db.exec(income_query).one_or_none()
        total_income = float(income_val[0]) if income_val and income_val[0] is not None else 0.0
        expense_query = select(func.sum(FinancialRecord.amount)).where(FinancialRecord.type == RecordType.EXPENSE)
        expense_val = db.exec(expense_query).one_or_none()
        total_expenses = float(expense_val[0]) if expense_val and expense_val[0] is not None else 0.0
        category_query = select(FinancialRecord.category, func.sum(FinancialRecord.amount)).group_by(FinancialRecord.category)
        category_results = db.exec(category_query).all()
        category_totals = {category: float(total) for category, total in category_results}
        recent_activity_query = select(FinancialRecord).order_by(desc(FinancialRecord.record_date)).limit(10)
        recent_activity = db.exec(recent_activity_query).all()
        monthly_query = (
            select(
                func.to_char(FinancialRecord.record_date, "YYYY-MM").label("month"),
                func.sum(
                    func.case(
                        (FinancialRecord.type == RecordType.INCOME, FinancialRecord.amount),
                        else_=-FinancialRecord.amount
                    )
                ).label("net")
            )
            .group_by("month")
            .order_by("month")
        )
        monthly_results = db.exec(monthly_query).all()
        monthly_trends = {row.month: float(row.net) for row in monthly_results}
        return DashboardSummaryResponse(
            total_income=total_income,
            total_expenses=total_expenses,
            net_balance=total_income - total_expenses,
            category_totals=category_totals,
            recent_activity=recent_activity,
            monthly_trends=monthly_trends
        )
