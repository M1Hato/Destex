from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task_model import Task
from app.schemas.task_schemas import TaskCreate, TaskUpdate, TaskRead

class TaskRepo:

    @staticmethod
    async def get_user_task_repo(user_id: int, session: AsyncSession):
        result = await session.execute(
            select(Task).where(Task.user_id == user_id, Task.is_deleted == False)
        )
        return result.scalars().all()

    @staticmethod
    async def create_task_repo(task: TaskCreate, session: AsyncSession):
        session.add(task)

        try:
            await session.commit()
            await session.refresh(task)
            return task
        except IntegrityError:
            await session.rollback()
            return None


    @staticmethod
    async def update_task_repo(update_data: dict, user_id: int, task_id: int, session: AsyncSession):

        stmt = (update(Task).where(
            Task.id == task_id,
                        Task.user_id == user_id,
                        Task.is_deleted == False)
                .values(**update_data).returning(Task))


        result = await session.execute(stmt)
        updated_task = result.scalar_one_or_none()
        if updated_task:
            await session.commit()

        return updated_task
