from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional

class CategoryBase(SQLModel):
    name: str
    description: str

class Category(CategoryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    categories: List["Entry"] = Relationship(back_populates="category")  # type: ignore

class CategoryCreate(CategoryBase):
    name: str = Field(..., min_length=1, max_length=100, description="Name is mandatory")
    description: str = Field(..., min_length=1, max_length=255, description="Description is mandatory")