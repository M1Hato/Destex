from sqlalchemy.ext.asyncio import AsyncSession
from app.models.task_model import Task
from app.schemas.task_schemas import TaskCreate, TaskUpdate
from fastapi import HTTPException
from app.repositories.task_repo import TaskRepo


class TaskService:

    @staticmethod
    async def create_task_service(data: TaskCreate, user_id: int, session: AsyncSession):
        clean_deadline = data.deadline.replace(tzinfo=None)
        new_task_model = Task(**data.model_dump(exclude={"deadline"}), deadline=clean_deadline, user_id = user_id)

        result = await TaskRepo.create_task_repo(new_task_model, session)
        if result is None:
            raise HTTPException(status_code=404, detail="Task was not created")

        return result

