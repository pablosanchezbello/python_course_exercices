from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from models.author import Author
from models.category import Category

class EntryBase(SQLModel):
    title: str = Field(index=True, unique=True)  # Make title unique and indexed
    content: str
    is_deleted: bool = Field(default=False)

class Entry(EntryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    author_id: int = Field(foreign_key="author.id")
    author: Optional["Author"] = Relationship(back_populates="entries") 
    category_id: int = Field(foreign_key="category.id")
    category: Optional["Category"] = Relationship(back_populates="categories")

class EntryCreate(EntryBase):
    author_name: str 
    title: str = Field(..., index=True, unique=True, min_length=1, description="Title is now mandatory for EntryCreate")

class EntryRead(EntryBase):
    id: int
    author: Author
