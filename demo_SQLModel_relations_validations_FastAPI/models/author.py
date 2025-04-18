from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from pydantic import EmailStr

class AuthorBase(SQLModel):
    name: str

class Author(AuthorBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    entries: List["Entry"] = Relationship(back_populates="author")  # type: ignore

class AuthorCreate(AuthorBase):
    email: EmailStr = Field(..., index=True, unique=True, min_length=1, regex=r"^[\w\.-]+@[\w\.-]+\.\w+$", description="Email is mandatory") 
