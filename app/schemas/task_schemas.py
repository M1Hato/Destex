from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.models.task_model import TaskPriority


class Task(BaseModel):
    title: str
    description: Optional[str] = None
    deadline: datetime
    priority: TaskPriority = TaskPriority.MEDIUM


class TaskCreate(Task):
    pass


class TaskUpdate(Task):
    title: Optional[str] = None
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    priority: Optional[TaskPriority] = None
    is_completed: Optional[bool] = None


class TaskRead(Task):
    id: int
    user_id: int
    is_completed: bool
    is_deleted: bool
    created_at: datetime
