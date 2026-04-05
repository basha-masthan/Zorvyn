from typing import Optional
from sqlmodel import Session, select
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash

class UserService:
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        return db.exec(select(User).where(User.email == email)).first()

    @staticmethod
    def get_users(db: Session, skip: int = 0, limit: int = 100):
        return db.exec(select(User).offset(skip).limit(limit)).all()

    @staticmethod
    def create_user(db: Session, user: UserCreate) -> User:
        db_user = User(
            email=user.email,
            hashed_password=get_password_hash(user.password),
            role=user.role,
            is_active=user.is_active,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def update_user(db: Session, user: User, user_in: UserUpdate) -> User:
        data = user_in.model_dump(exclude_unset=True)
        if "password" in data:
            data["hashed_password"] = get_password_hash(data.pop("password"))
            
        for key, val in data.items():
            setattr(user, key, val)
            
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
