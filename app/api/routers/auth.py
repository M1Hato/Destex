from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.schemas.user_schemas import UserCreate
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