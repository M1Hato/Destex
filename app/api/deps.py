from fastapi import HTTPException
from fastapi.params import Depends
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from app.core.login_token import decode_refresh_token
from app.database import get_async_session
from app.repositories.user_repo import UserRepo

async def get_current_user(
        request: Request,
        session: AsyncSession = Depends(get_async_session)
):

    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer"):
        raise HTTPException(status_code=401, detail="Invalid token")

    token = auth_header.split(" ")[1]

    try:
        payload = decode_refresh_token(token)

        if isinstance(payload, Exception):
            raise HTTPException(status_code=400, detail="Invalid or expire token")

        email = payload.get("sub")

        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token: no email provided")

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = await UserRepo.get_user_by_email(email, session)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    return user