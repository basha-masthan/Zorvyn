from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.api.deps import RequireRole
from app.db.session import get_session
from app.models.user import Role
from app.schemas.record import DashboardSummaryResponse
from app.services.dashboard_service import DashboardService

router = APIRouter()

@router.get("/summary", response_model=DashboardSummaryResponse)
def get_summary(db: Session = Depends(get_session), _ = Depends(RequireRole([Role.ADMIN, Role.ANALYST, Role.VIEWER]))):
    return DashboardService.get_summary(db)
