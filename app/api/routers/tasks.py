from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from app.services.task_service import TaskService
from app.database import get_async_session
from app.models.user_model import User
from app.schemas.task_schemas import TaskCreate
from app.api.deps import get_current_user

task_router = APIRouter(
    prefix="/tasks",
)

@task_router.post("/tasks")
async def create_task(
        data: TaskCreate,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):

    return await TaskService.create_task_service(data, current_user.id, session)