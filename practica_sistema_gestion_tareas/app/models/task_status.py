from sqlmodel import SQLModel, Field
from typing import Optional

class TaskStatusBase(SQLModel):
    name: str = Field(..., unique=True)
    color: Optional[str]

class TaskStatus(TaskStatusBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
