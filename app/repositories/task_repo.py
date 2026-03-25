from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task_model import Task
from app.schemas.task_schemas import TaskCreate, TaskUpdate, TaskRead

class TaskRepo:

    @staticmethod
    async def create_task_repo(task: Task, session: AsyncSession):
        session.add(task)

        try:
            await session.commit()
            await session.refresh(task)
            return task
        except IntegrityError:
            await session.rollback()
            return None

    @staticmethod
    async def get_user_task_repo(user_id: int, session: AsyncSession):
        result = await session.execute(
            select(Task).where(Task.user_id == user_id, Task.is_deleted == False)
        )
        return result.scalars().all()


    @staticmethod
    async def update_task_repo(task_id: int, task: TaskUpdate, session: AsyncSession):
        update_data = task.model_dump(exclude_none=True)
        if not update_data:
            return None

        change = await session.execute(update(Task).where(Task.id == task_id).values(**update_data))
        await session.commit()
        await session.refresh(task)
        return task


