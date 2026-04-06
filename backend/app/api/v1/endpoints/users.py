from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.api.deps import RequireRole, get_current_active_user
from app.db.session import get_session
from app.models.user import Role
from app.schemas.user import UserCreate, UserResponse, UserUpdate
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

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_session), _ = Depends(RequireRole([Role.ADMIN]))):
    user = UserService.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_in: UserUpdate, db: Session = Depends(get_session), _ = Depends(RequireRole([Role.ADMIN]))):
    user = UserService.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserService.update_user(db, user, user_in)

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_session), _ = Depends(RequireRole([Role.ADMIN]))):
    user = UserService.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    UserService.delete_user(db, user_id)
    return {"success": True}
