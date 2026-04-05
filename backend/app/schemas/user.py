from pydantic import BaseModel, EmailStr
from typing import Optional
from app.models.user import Role

class UserBase(BaseModel):
    email: EmailStr
    role: Role = Role.VIEWER
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[Role] = None
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    id: int
    
    class Config:
        from_attributes = True
