from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.login_token import create_access_token, create_refresh_token
from app.schemas.user_schemas import UserCreate, UserLogin
from app.models.user_model import User
from app.repositories.user_repo import UserRepo
from app.core.security import hash_password, verify_password


class AuthService:

    @staticmethod
    async def create_user(data: UserCreate, session: AsyncSession):
        data.password = hash_password(data.password)

        new_user_model = User(**data.model_dump())
        result = await UserRepo.create_user_repo(new_user_model, session)

        if result is None:
            raise HTTPException(status_code=409, detail="User is already registered")

        return result


    @staticmethod
    async def login_user(data: UserLogin, session: AsyncSession):
        user = await UserRepo.get_user_by_email(data.email, session)
        if user is None:
            raise HTTPException(status_code=401, detail="Invalid Email or Password")

        check_pwd = verify_password(user.password, data.password)

        if not check_pwd:
            raise HTTPException(status_code=401, detail="Invalid Email or Password")

        access_token = create_access_token(data={"sub": user.email})
        refresh_token = create_refresh_token(data={"sub": user.email})
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }