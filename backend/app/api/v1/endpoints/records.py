from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.api.deps import RequireRole, get_current_active_user
from app.db.session import get_session
from app.models.user import Role
from app.models.record import RecordType
from app.schemas.record import RecordCreate, RecordResponse, RecordUpdate
from app.services.record_service import RecordService

router = APIRouter()

@router.get("/", response_model=list[RecordResponse])
def get_records(
    db: Session = Depends(get_session),
    skip: int = 0,
    limit: int = 100,
    type: Optional[RecordType] = None,
    category: Optional[str] = None,
    _ = Depends(get_current_active_user)
):
    return RecordService.get_records(db, skip=skip, limit=limit, type=type, category=category)

@router.post("/", response_model=RecordResponse)
def create_record(record_in: RecordCreate, db: Session = Depends(get_session), current_user = Depends(RequireRole([Role.ADMIN]))):
    return RecordService.create_record(db, record_in, current_user.id)

@router.put("/{record_id}", response_model=RecordResponse)
def update_record(record_id: int, record_in: RecordUpdate, db: Session = Depends(get_session), _ = Depends(RequireRole([Role.ADMIN]))):
    record = RecordService.get_record(db, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return RecordService.update_record(db, record, record_in)

@router.delete("/{record_id}")
def delete_record(record_id: int, db: Session = Depends(get_session), _ = Depends(RequireRole([Role.ADMIN]))):
    record = RecordService.get_record(db, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    RecordService.delete_record(db, record_id)
    return {"success": True}
