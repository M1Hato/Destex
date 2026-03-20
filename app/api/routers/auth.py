from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import Response
from app.api.deps import get_current_user
from app.database import get_async_session
from app.schemas.user_schemas import UserCreate, UserLogin
from app.services.auth_service import AuthService

auth_router = APIRouter(
    prefix="/auth",
)


# @auth_router.get("/get/user/{email}")
# async def get_user(
#         email: str,
#         current_user = Depends(get_current_user)
# ):
#     return current_user
@auth_router.get("/me")
async def get_user(
        current_user = Depends(get_current_user),
):
    return current_user

@auth_router.post("/register")
async def register_user(
        data: UserCreate,
        session: AsyncSession = Depends(get_async_session),
):
    return await AuthService.create_user(data, session)


@auth_router.post("/login")
async def login_user(
        data: Annotated[UserLogin, Depends()],
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

@auth_router.post("/refresh")
async def get_new_access(
        request: Request,
        session: AsyncSession = Depends(get_async_session)
):
    result = await AuthService.refresh_access_token(request, session)
    return result
