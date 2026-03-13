from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user_model import User


class UserRepo:

    @staticmethod
    async def get_user_by_email(session: AsyncSession, email: str):
        return await session.scalar(
            select(User).where(User.email == email))

    @staticmethod
    async def create_user(user: User, session: AsyncSession):
        session.add(user)
        try:
            await session.commit()
            await session.refresh(user)
            return user
        except IntegrityError:
            await session.rollback()
            return None




