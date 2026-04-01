from sqlalchemy.ext.asyncio import AsyncSession
from app.models.task_model import Task
from app.schemas.task_schemas import TaskCreate, TaskUpdate
from fastapi import HTTPException
from app.repositories.task_repo import TaskRepo


class TaskService:

    @staticmethod
    async def get_task_service(user_id: int, limit: int, offset: int, search, priority, session: AsyncSession):
        result = await TaskRepo.get_user_task_repo(user_id, limit, offset, search, priority, session)
        return result

    @staticmethod
    async def create_task_service(data: TaskCreate, user_id: int, session: AsyncSession):
        clean_deadline = data.deadline.replace(tzinfo=None)
        new_task_model = Task(**data.model_dump(exclude={"deadline"}), deadline=clean_deadline, user_id = user_id)

        result = await TaskRepo.create_task_repo(new_task_model, session)
        if result is None:
            raise HTTPException(status_code=404, detail="Task was not created")

        return result

    @staticmethod
    async def update_task_service(data: TaskUpdate, user_id: int, task_id: int, session: AsyncSession):
        update_data = data.model_dump(exclude_unset=True)

        if "deadline" in update_data and update_data["deadline"] is not None:
            update_data["deadline"] = update_data["deadline"].replace(tzinfo=None)

        result = await TaskRepo.update_task_repo(update_data, user_id, task_id, session)
        if result is None:
            raise HTTPException(status_code=404, detail="Task was not found")
        return result

    @staticmethod
    async def delete_task_service(task_id: int, user_id: int,  session: AsyncSession):
        result = await TaskRepo.delete_task_repo(task_id, user_id, session)

        if result is None:
            raise HTTPException(status_code=404, detail="Task was not found")

        return result




