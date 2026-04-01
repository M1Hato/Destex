from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

from app.models.task_model import TaskPriority


class UserTask(BaseModel):
    title: str
    description: Optional[str] = None
    deadline: datetime
    priority: TaskPriority = TaskPriority.MEDIUM


class TaskCreate(UserTask):
    pass


class TaskUpdate(UserTask):
    title: Optional[str] = None
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    priority: Optional[TaskPriority] = None
    is_completed: Optional[bool] = None


class TaskRead(BaseModel):
    id: int
    user_id: int
    priority: Optional[TaskPriority]
    is_completed: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
