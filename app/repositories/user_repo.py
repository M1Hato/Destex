from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import verify_password
from app.models.user_model import User
from app.schemas.user_schemas import UserLogin


class UserRepo:

    @staticmethod
    async def get_user_by_email(email: str, session: AsyncSession):
        return await session.scalar(
            select(User).where(User.email == email))

    @staticmethod
    async def create_user_repo(user: User, session: AsyncSession):
        session.add(user)
        try:
            await session.commit()
            await session.refresh(user)
            return user
        except IntegrityError:
            await session.rollback()
            return None

    @staticmethod
    async def login_user_repo(data: UserLogin, session: AsyncSession):
        user = await UserRepo.get_user_by_email(data.email, session)
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid Email or Password")

        check_pwd = verify_password(user.password, data.password)

        if not check_pwd:
            raise HTTPException(status_code=401, detail="Invalid Email or Password")

        return user