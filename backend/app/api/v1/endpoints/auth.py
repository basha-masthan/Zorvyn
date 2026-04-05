from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from app.core import security
from app.core.config import settings
from app.db.session import get_session
from app.services.user_service import UserService

router = APIRouter()

@router.post("/login/access-token")
def login(db: Session = Depends(get_session), form_data: OAuth2PasswordRequestForm = Depends()):
    user = UserService.get_user_by_email(db, email=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(user.id, expires_delta=expires),
        "token_type": "bearer",
    }
