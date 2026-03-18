from fastapi import HTTPException
from datetime import datetime, timezone, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import update

from app.config import settings
from app.models.log_tokens import LogTokens

REFRESH_TOKEN = settings.REFRESH_TOKEN_EXPIRE_MINUTES

class RefreshTokenRepo:

    @staticmethod
    async def save_refresh_token(user_id: int, refresh_token, session: AsyncSession):

        aware_now = datetime.now(timezone.utc)
        expires_at = aware_now + timedelta(minutes=REFRESH_TOKEN)

        now = aware_now.replace(tzinfo=None)
        exp = expires_at.replace(tzinfo=None)

        token = LogTokens(
            user_id=user_id,
            refresh_token=refresh_token,
            created_at=now,
            expires_at=exp,
            is_active=True
        )

        session.add(token)
        await session.commit()
        await session.refresh(token)
        return token


    @staticmethod
    async def deactivate_refresh_token(refresh_token: str, session: AsyncSession):

        if not refresh_token:
            raise HTTPException(status_code=400, detail="Refresh token required")

        stmt = (
            update(LogTokens)
            .where(LogTokens.refresh_token == refresh_token)
            .values(is_active=False)
        )

        await session.execute(stmt)
        await session.commit()


