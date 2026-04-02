from fastapi import HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from app.config import settings
from app.core.login_token import create_access_token, create_refresh_token
from app.logging import logger
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
        logger.info(f"Attempting to register new user: {data.email}")
        result = await UserRepo.create_user_repo(new_user_model, session)

        if result is None:
            logger.warning(f"Failed to create new user: {result}")
            raise HTTPException(status_code=409, detail="User is already registered")

        logger.info(f"User {data.email} registered successfully (ID: {result.id})")
        return result


    @staticmethod
    async def login_user(data: UserLogin, response: Response, session: AsyncSession):
        user = await UserRepo.login_user_repo(data, session)

        logger.info(f"User {user.email} (ID: {user.id}) logged in and tokens generated")

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
            logger.warning(f"Logout attempted without refresh token in cookies")
            raise HTTPException(status_code=401, detail="Refresh token is missing")

        await RefreshTokenRepo.deactivate_refresh_token(refresh_token, session)
        logger.info("User successfully logged out and token deactivated")
        return {"detail": "User logged out"}

    @staticmethod
    async def refresh_access_token(request: Request, session: AsyncSession):
        refresh_token = request.cookies.get("refresh_token")

        if not refresh_token:
            logger.warning(f"Token refresh failed: No refresh token in cookies")
            raise HTTPException(status_code=401, detail="Refresh token is missing")

        token = await RefreshTokenRepo.get_active_refresh_token(refresh_token, session)

        if not token:
            logger.warning(f"Token refresh failed: Token not found in database or inactive")
            raise HTTPException(status_code=401, detail="Refresh token is missing")

        payload = decode_refresh_token(token.refresh_token)

        if isinstance(payload, HTTPException) or not payload:
            raise HTTPException(status_code=401, detail="Token is invalid or expired")

        email = payload.get("sub")

        user = await UserRepo.get_user_by_email(email, session)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        access_token = create_access_token(data={"sub": user.email})
        logger.info(f"Access token successfully refreshed for user: {user.email}")

        return {"access_token": access_token}