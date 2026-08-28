# Owner: mousamdas156@gmail.com
"""
Repository layer for RefreshToken.
Handles direct database queries for JWT refresh token storage.
"""

import uuid
from datetime import datetime, timezone
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.refreshToken import RefreshToken


class RefreshTokenRepository:
    def __init__(self, session: AsyncSession):
        """
        Handles the init functionality.
        """
        self.session = session

    async def getById(self, tokenId: uuid.UUID) -> RefreshToken | None:
        """
        Handles the get by id functionality.
        """
        result = await self.session.execute(
            select(RefreshToken).where(RefreshToken.id == tokenId)
        )
        return result.scalar_one_or_none()

    async def getByTokenHash(self, tokenHash: str) -> RefreshToken | None:
        """
        Handles the get by token hash functionality.
        """
        result = await self.session.execute(
            select(RefreshToken).where(RefreshToken.tokenHash == tokenHash)
        )
        return result.scalar_one_or_none()

    async def getByUserId(self, userId: uuid.UUID) -> Sequence[RefreshToken]:
        """
        Handles the get by user id functionality.
        """
        result = await self.session.execute(
            select(RefreshToken).where(RefreshToken.userId == userId)
        )
        return result.scalars().all()

    async def create(self, token: RefreshToken) -> RefreshToken:
        """
        Handles the create functionality.
        """
        self.session.add(token)
        await self.session.flush()
        await self.session.refresh(token)
        return token

    async def revoke(self, token: RefreshToken) -> RefreshToken:
        """
        Handles the revoke functionality.
        """
        token.revokedAt = datetime.now(timezone.utc)
        await self.session.flush()
        await self.session.refresh(token)
        return token

    async def delete(self, token: RefreshToken) -> None:
        """
        Handles the delete functionality.
        """
        await self.session.delete(token)
        await self.session.flush()
