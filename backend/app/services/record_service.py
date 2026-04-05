from typing import Optional
from sqlmodel import Session, select
from app.models.record import FinancialRecord, RecordType
from app.schemas.record import RecordCreate, RecordUpdate

class RecordService:
    @staticmethod
    def get_record(db: Session, record_id: int) -> Optional[FinancialRecord]:
        return db.get(FinancialRecord, record_id)

    @staticmethod
    def get_records(db: Session, skip: int = 0, limit: int = 100, type: Optional[RecordType] = None, category: Optional[str] = None):
        stmt = select(FinancialRecord)
        if type:
            stmt = stmt.where(FinancialRecord.type == type)
        if category:
            stmt = stmt.where(FinancialRecord.category == category)
        return db.exec(stmt.offset(skip).limit(limit)).all()

    @staticmethod
    def create_record(db: Session, record: RecordCreate, user_id: int) -> FinancialRecord:
        db_record = FinancialRecord(**record.model_dump(), created_by=user_id)
        db.add(db_record)
        db.commit()
        db.refresh(db_record)
        return db_record

    @staticmethod
    def update_record(db: Session, record: FinancialRecord, record_in: RecordUpdate) -> FinancialRecord:
        for key, val in record_in.model_dump(exclude_unset=True).items():
            setattr(record, key, val)
        db.add(record)
        db.commit()
        db.refresh(record)
        return record

    @staticmethod
    def delete_record(db: Session, record_id: int):
        db_record = db.get(FinancialRecord, record_id)
        if db_record:
            db.delete(db_record)
            db.commit()
