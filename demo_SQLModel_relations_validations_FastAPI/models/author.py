from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from pydantic import EmailStr, model_validator

class AuthorBase(SQLModel):
    name: str
    email: str
    is_deleted: bool = Field(default=False)
    created_at: datetime = Field(default=datetime.now(), description="Creation date of the author")
    updated_at: datetime | None = Field(
        default_factory= lambda: datetime.now(timezone.utc), 
        nullable=False,
        sa_column_kwargs={
            "onupdate": lambda: datetime.now(timezone.utc),
        },
        description="Last update date of the author")

    class Config:
        validate_assignment = True

class Author(AuthorBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    entries: List["Entry"] = Relationship(back_populates="author")  # type: ignore

class AuthorCreate(AuthorBase):
    email: EmailStr = Field(..., index=True, unique=True, min_length=1, regex=r"^[\w\.-]+@[\w\.-]+\.\w+$", description="Email is mandatory")
    name: str = Field(..., min_length=1, max_length=100, description="Name is mandatory") 
