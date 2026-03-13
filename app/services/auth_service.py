from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user_schemas import UserCreate
from app.models.user_model import User
from app.repositories.user_repo import UserRepo
from app.core.security import hash_password


class AuthService:

    @staticmethod
    async def create_user(data: UserCreate, session: AsyncSession):
        data.password = hash_password(data.password)

        new_user_model = User(**data.model_dump())
        result = await UserRepo.create_user(new_user_model, session)

        if result is None:
            raise HTTPException(status_code=409, detail="User is already registered")

        return result



