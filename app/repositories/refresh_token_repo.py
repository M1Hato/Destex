from fastapi import HTTPException
from datetime import datetime, timezone, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import update, select
from app.config import settings
from app.logging import logger
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
        logger.info(f"Refresh token has been saved for user: {user_id}")
        return token


    @staticmethod
    async def deactivate_refresh_token(refresh_token: str, session: AsyncSession):

        if not refresh_token:
            logger.warning("Refresh token for deactivate required")
            raise HTTPException(status_code=400, detail="Refresh token required")

        stmt = (
            update(LogTokens)
            .where(LogTokens.refresh_token == refresh_token)
            .values(is_active=False)
        )

        await session.execute(stmt)
        logger.info(f"Refresh token has been deactivated for user: {refresh_token}")
        await session.commit()


    @staticmethod
    async def get_token(refresh_token: str, session: AsyncSession):
        logger.debug(f"Attempt to get refresh token for user: {refresh_token}")
        return await session.scalar(
            select(LogTokens)
            .where(LogTokens.refresh_token == refresh_token)
        )

    @staticmethod
    async def get_active_refresh_token(refresh_token: str, session: AsyncSession):
        token = await RefreshTokenRepo.get_token(refresh_token, session)
        aware_now = datetime.now(timezone.utc).replace(tzinfo=None)

        if not token or not token.is_active or token.expires_at < aware_now:
            logger.warning(f"Refresh token expired for user: {refresh_token}")
            raise HTTPException(status_code=401, detail="Refresh token is invalid or expired")
        logger.info(f"Successfully get refresh token for user: {refresh_token}")
        return token



