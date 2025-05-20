from datetime import datetime, timezone
from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import EmailStr

class UserBase(SQLModel):
    username: str = Field(..., unique=True)
    email: EmailStr = Field(..., unique=True)
    role: str = Field(default="user")  # Default role is "user"

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default=datetime.now(timezone.utc), description="Creation date of the user")
    hashed_password: str
    refresh_token: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(...)

class UserResponse(UserBase):
    id: int
    created_at: datetime