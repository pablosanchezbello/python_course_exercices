from datetime import datetime, timezone, date
from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import EmailStr

class TaskBase(SQLModel):
    title: str = Field(..., unique=True)
    description: Optional[str]
    due_date: Optional[date]
    is_completed: bool
    todo_list_id: int = Field(foreign_key="todolist.id")
    status_id: int = Field(foreign_key="taskstatus.id")

class Task(TaskBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default=datetime.now(timezone.utc), description="Creation date of the task")
