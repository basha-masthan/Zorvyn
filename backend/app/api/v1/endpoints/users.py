from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.api.deps import RequireRole, get_current_active_user
from app.db.session import get_session
from app.models.user import Role
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import UserService

router = APIRouter()

@router.get("/", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_session), skip: int = 0, limit: int = 100, _ = Depends(RequireRole([Role.ADMIN]))):
    return UserService.get_users(db, skip=skip, limit=limit)

@router.post("/", response_model=UserResponse)
def create_user(user_in: UserCreate, db: Session = Depends(get_session), _ = Depends(RequireRole([Role.ADMIN]))):
    user = UserService.get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return UserService.create_user(db, user_in)

@router.get("/me", response_model=UserResponse)
def get_me(current_user = Depends(get_current_active_user)):
    return current_user
