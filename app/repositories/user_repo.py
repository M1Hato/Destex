from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import verify_password
from app.logging import logger
from app.models.user_model import User
from app.schemas.user_schemas import UserLogin


class UserRepo:

    @staticmethod
    async def get_user_by_email(email: str, session: AsyncSession):
        logger.debug(f"Getting user with email {email}")
        return await session.scalar(
            select(User).where(User.email == email))


    @staticmethod
    async def create_user_repo(user: User, session: AsyncSession):
        session.add(user)
        try:
            await session.commit()
            await session.refresh(user)
            logger.info(f"User has been successfully registered. ID: {user.id}")
            return user
        except IntegrityError as e:
            await session.rollback()
            logger.error(f"Integrity Error during create user: {e}", exc_info=True)
            return None

    @staticmethod
    async def login_user_repo(data: UserLogin, session: AsyncSession):
        user = await UserRepo.get_user_by_email(data.email, session)
        logger.debug(f"Searching user with email {data.email}")
        if user is None:
            logger.warning(f"User with email {data.email} not found")
            raise HTTPException(status_code=401, detail="Invalid Email or Password")

        check_pwd = verify_password(data.password, user.password)

        if not check_pwd:
            logger.warning(f"Password mismatch for user with email {data.email}")
            raise HTTPException(status_code=401, detail="Invalid Email or Password")

        logger.info(f"{data.email} logged in")
        return user