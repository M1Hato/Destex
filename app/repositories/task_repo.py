from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task_model import Task
from app.schemas.task_schemas import TaskCreate

class TaskRepo:

    @staticmethod
    async def get_user_task_repo(user_id: int, limit: int, offset: int, search, priority, session: AsyncSession):
        stmt = select(Task).where(Task.user_id == user_id, Task.is_deleted == False)

        if search:
            stmt = stmt.where(Task.title.like(f"%{search}%"))
        if priority:
            stmt = stmt.where(Task.priority == priority)

        stmt = stmt.order_by(Task.created_at.desc()).limit(limit).offset(offset)

        result = await session.execute(stmt)
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


    @staticmethod
    async def delete_task_repo(task_id: int, user_id: int, session: AsyncSession):

        stmt = (update(Task).where(
            Task.id == task_id,
                        Task.user_id == user_id,
                        Task.is_deleted == False)
                .values(is_deleted=True).returning(Task))

        result = await session.execute(stmt)
        deleted_task = result.scalar_one_or_none()
        if deleted_task:
            await session.commit()

        return deleted_task
