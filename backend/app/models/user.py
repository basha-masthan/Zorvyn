from sqlmodel import SQLModel, Field
from typing import Optional
from enum import Enum

class Role(str, Enum):
    VIEWER = "Viewer"
    ANALYST = "Analyst"
    ADMIN = "Admin"

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    role: Role = Field(default=Role.VIEWER)
    is_active: bool = Field(default=True)
