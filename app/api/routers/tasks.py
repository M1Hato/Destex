from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from app.services.task_service import TaskService
from app.database import get_async_session
from app.models.user_model import User
from app.schemas.task_schemas import TaskCreate, TaskUpdate
from app.api.deps import get_current_user

task_router = APIRouter(
    prefix="/tasks",
)

@task_router.get("/all")
async def get_all_tasks(
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await TaskService.get_task_repo(current_user.id, session)
@task_router.post("/create")
async def create_task(
        data: TaskCreate,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):

    return await TaskService.create_task_service(data, current_user.id, session)


@task_router.patch("/update/{task_id}")
async def update_task(
        data: TaskUpdate,
        task_id: int,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await TaskService.update_task_service(data, current_user.id, task_id, session)