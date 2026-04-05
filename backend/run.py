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
        # check if admin already exists
        admin = UserService.get_user_by_email(session, "admin@example.com")
        if not admin:
            print("Seeding initial users...")
            # Create default admin
            UserService.create_user(session, UserCreate(
                email="admin@example.com",
                password="admin",
                role=Role.ADMIN,
                is_active=True
            ))
            # Create default analyst
            UserService.create_user(session, UserCreate(
                email="analyst@example.com",
                password="analyst",
                role=Role.ANALYST,
                is_active=True
            ))
            # Create default viewer
            UserService.create_user(session, UserCreate(
                email="viewer@example.com",
                password="viewer",
                role=Role.VIEWER,
                is_active=True
            ))
            print("Initial users created successfully!")
        else:
            print("Database already setup. Skipping seed.")

if __name__ == "__main__":
    # Initialize DB then start server
    init_db()
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
