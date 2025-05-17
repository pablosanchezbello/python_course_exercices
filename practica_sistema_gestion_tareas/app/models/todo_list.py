from datetime import datetime, timezone
from sqlmodel import SQLModel, Field
from typing import Optional

class TodoListBase(SQLModel):
    title: str = Field(..., unique=True)
    description: Optional[str]
    owner_username: str = Field(foreign_key="user.username")


class TodoList(TodoListBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    owner_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default=datetime.now(timezone.utc), description="Creation date of the todo list")
