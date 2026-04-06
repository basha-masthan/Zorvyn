from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from app.models.user import Role

class UserBase(BaseModel):
    email: EmailStr
    role: Role = Role.VIEWER
    is_active: bool = True

class UserCreate(UserBase):
    password: str = Field(min_length=4)

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[Role] = None
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)
