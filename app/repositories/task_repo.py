from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.logging import logger
from app.models.task_model import Task
from app.schemas.task_schemas import TaskCreate

class TaskRepo:

    @staticmethod
    async def get_user_task_repo(user_id: int, limit: int, offset: int, search, priority, session: AsyncSession):
        stmt = select(Task).where(Task.user_id == user_id, Task.is_deleted == False)
        logger.debug(f"Searching tasks with query {stmt.compile(compile_kwargs={'literal_binds': True})}")

        if search:
            stmt = stmt.where(Task.title.ilike(f"%{search}%"))
        if priority:
            stmt = stmt.where(Task.priority == priority)

        stmt = stmt.order_by(Task.created_at.desc()).limit(limit).offset(offset)
        logger.debug(f"Executing SQL: {stmt.compile(compile_kwargs={'literal_binds': True})}")

        result = await session.execute(stmt)
        return result.scalars().all()

    @staticmethod
    async def create_task_repo(task: TaskCreate, user_id, session: AsyncSession):
        session.add(task)

        try:
            await session.commit()
            await session.refresh(task)
            logger.info(f"Task for user: {user_id} created successfully: {task}")
            return task
        except IntegrityError as e:
            await session.rollback()
            logger.error(f"Integrity error during task creation: {e}", exc_info=True)
            return None
        except Exception as e:
            await session.rollback()
            logger.error(f"Unexpected error: {e}", exc_info=True)
            return None


    @staticmethod
    async def update_task_repo(update_data: dict, user_id: int, task_id: int, session: AsyncSession):

        stmt = (update(Task).where(
            Task.id == task_id,
                        Task.user_id == user_id,
                        Task.is_deleted == False)
                .values(**update_data).returning(Task))
        logger.debug(f"Executing Update SQL query: {stmt.compile(compile_kwargs={'literal_binds': True})}")


        result = await session.execute(stmt)
        updated_task = result.scalar_one_or_none()
        if updated_task:
            logger.info(f"Successfully updated Task {task_id} for user: {user_id}")
            await session.commit()

        return updated_task


    @staticmethod
    async def delete_task_repo(task_id: int, user_id: int, session: AsyncSession):

        stmt = (update(Task).where(
            Task.id == task_id,
                        Task.user_id == user_id,
                        Task.is_deleted == False)
                .values(is_deleted=True).returning(Task))
        logger.debug(f"Executing Delete SQL query: {stmt.compile(compile_kwargs={'literal_binds': True})}")

        result = await session.execute(stmt)
        deleted_task = result.scalar_one_or_none()
        if deleted_task:
            logger.info(f"Successfully deleted Task {task_id} for user: {user_id}")
            await session.commit()

        return deleted_task
