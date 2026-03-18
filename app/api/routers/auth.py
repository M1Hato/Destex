from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import Response

from app.database import get_async_session
from app.schemas.user_schemas import UserCreate, UserLogin
from app.services.auth_service import AuthService

auth_router = APIRouter(
    prefix="/auth",
)


@auth_router.post("/register")
async def register_user(
        data: UserCreate,
        session: AsyncSession = Depends(get_async_session),
):
    return await AuthService.create_user(data, session)


@auth_router.post("/login")
async def login_user(
        data: UserLogin,
        response: Response,
        session: AsyncSession = Depends(get_async_session)
):
    return await AuthService.login_user(data, response, session)

@auth_router.post("/logout")
async def logout_user(
        response: Response,
        request: Request,
        session: AsyncSession = Depends(get_async_session)
):
    result = await AuthService.logout_user(request, session)

    response.delete_cookie("refresh_token")
    return result