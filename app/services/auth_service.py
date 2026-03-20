from fastapi import HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from app.config import settings
from app.core.login_token import create_access_token, create_refresh_token
from app.schemas.user_schemas import UserCreate, UserLogin
from app.models.user_model import User
from app.repositories.user_repo import UserRepo
from app.core.security import hash_password
from app.repositories.refresh_token_repo import RefreshTokenRepo
from app.core.login_token import decode_refresh_token

REFRESH_TOKEN = settings.REFRESH_TOKEN_EXPIRE_MINUTES

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
    async def login_user(data: UserLogin, response: Response, session: AsyncSession):
        user = await UserRepo.login_user_repo(data, session)

        access_token = create_access_token(data={"sub": user.email})
        refresh_token = create_refresh_token(data={"sub": user.email})

        await RefreshTokenRepo.save_refresh_token(user.id, refresh_token, session)

        #Збереження в кукі
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            secure=False,
            httponly=True,
            samesite="lax",
            max_age=REFRESH_TOKEN
        )

        return {"access_token": access_token}


    @staticmethod
    async def logout_user(request: Request, session: AsyncSession):

        refresh_token = request.cookies.get("refresh_token")

        if not refresh_token:
            raise HTTPException(status_code=401, detail="Refresh token is missing")

        await RefreshTokenRepo.deactivate_refresh_token(refresh_token, session)
        return {"detail": "User logged out"}

    @staticmethod
    async def refresh_access_token(request: Request, session: AsyncSession):
        refresh_token = request.cookies.get("refresh_token")
        token = await RefreshTokenRepo.get_active_refresh_token(refresh_token, session)

        if not token:
            raise HTTPException(status_code=401, detail="Refresh token is missing")

        payload = decode_refresh_token(token.refresh_token)

        if isinstance(payload, HTTPException) or not payload:
            raise HTTPException(status_code=401, detail="Token is invalid or expired")

        email = payload.get("sub")

        user = await UserRepo.get_user_by_email(email, session)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        access_token = create_access_token(data={"sub": user.email})

        return {"access_token": access_token}