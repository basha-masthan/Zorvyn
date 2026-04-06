import uvicorn
from app.db.session import engine
from sqlmodel import Session, SQLModel
from app.models.user import User, Role
from app.services.user_service import UserService
from app.schemas.user import UserCreate

def init_db():
    print("Initializing Database...")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        admin_email = "admin@example.com"
        admin = UserService.get_user_by_email(session, admin_email)
        if not admin:
            print("Seeding initial users (Admin, Analyst, Viewer)...")
            admin_user = UserService.create_user(session, UserCreate(
                email=admin_email,
                password="admin",
                role=Role.ADMIN,
                is_active=True
            ))
            UserService.create_user(session, UserCreate(
                email="analyst@example.com",
                password="analyst",
                role=Role.ANALYST,
                is_active=True
            ))
            UserService.create_user(session, UserCreate(
                email="viewer@example.com",
                password="viewer",
                role=Role.VIEWER,
                is_active=True
            ))
            from app.models.record import FinancialRecord, RecordType
            from datetime import date, timedelta
            print("Seeding sample financial records...")
            records = [
                FinancialRecord(amount=5000.0, type=RecordType.INCOME, category="Salary", record_date=date.today() - timedelta(days=5), created_by=admin_user.id, notes="Monthly salary payment"),
                FinancialRecord(amount=1200.0, type=RecordType.EXPENSE, category="Rent", record_date=date.today() - timedelta(days=2), created_by=admin_user.id, notes="Apartment rent"),
                FinancialRecord(amount=150.0, type=RecordType.EXPENSE, category="Utilities", record_date=date.today() - timedelta(days=1), created_by=admin_user.id, notes="Electricity and water"),
                FinancialRecord(amount=2000.0, type=RecordType.INCOME, category="Freelance", record_date=date.today() - timedelta(days=10), created_by=admin_user.id, notes="Project completion"),
                FinancialRecord(amount=80.0, type=RecordType.EXPENSE, category="Dining", record_date=date.today(), created_by=admin_user.id, notes="Team dinner")
            ]
            for r in records:
                session.add(r)
            session.commit()
            print("Seeding completed successfully.")
        else:
            print("Database already has data. Skipping seed.")

if __name__ == "__main__":
    init_db()
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
