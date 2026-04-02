from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.task_model import TaskPriority
from app.services.task_service import TaskService
from app.database import get_async_session
from app.models.user_model import User
from app.schemas.task_schemas import TaskCreate, TaskUpdate, TaskRead
from app.api.deps import get_current_user

task_router = APIRouter(
    tags = ["Tasks"],
    prefix="/tasks",
)

@task_router.get("/all", response_model=List[TaskRead])
async def get_all_tasks(
        current_user: User = Depends(get_current_user),
        limit: int = Query(10, ge=1, le=10),
        offset: int = Query(0, ge=0),
        search : Optional[str] = None,
        priority: Optional[TaskPriority] = None,
        session: AsyncSession = Depends(get_async_session)
):
    return await TaskService.get_task_service(current_user.id, limit, offset, search, priority, session)
@task_router.post("/create", status_code = 201, response_model=TaskRead)
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


@task_router.delete("/delete/{task_id}", status_code = 204)
async def delete_task(
        task_id: int,
        current_user: User = Depends(get_current_user),
        session: AsyncSession = Depends(get_async_session)
):
    await TaskService.delete_task_service(task_id, current_user.id, session)
    return None