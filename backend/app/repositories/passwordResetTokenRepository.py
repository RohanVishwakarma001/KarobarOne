# Owner: mousamdas156@gmail.com
"""
Repository layer for PasswordResetToken.
Handles direct database queries for the password recovery flow.
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.passwordResetToken import PasswordResetToken


class PasswordResetTokenRepository:
    def __init__(self, session: AsyncSession):
        """
        Handles the init functionality.
        """
        self.session = session

    async def getById(self, tokenId: uuid.UUID) -> PasswordResetToken | None:
        """
        Handles the get by id functionality.
        """
        result = await self.session.execute(
            select(PasswordResetToken).where(PasswordResetToken.id == tokenId)
        )
        return result.scalar_one_or_none()

    async def getByTokenHash(self, tokenHash: str) -> PasswordResetToken | None:
        """
        Handles the get by token hash functionality.
        """
        result = await self.session.execute(
            select(PasswordResetToken).where(
                PasswordResetToken.tokenHash == tokenHash
            )
        )
        return result.scalar_one_or_none()

    async def create(self, token: PasswordResetToken) -> PasswordResetToken:
        """
        Handles the create functionality.
        """
        self.session.add(token)
        await self.session.flush()
        await self.session.refresh(token)
        return token

    async def markUsed(self, token: PasswordResetToken) -> PasswordResetToken:
        """
        Handles the mark used functionality.
        """
        token.usedAt = datetime.now(timezone.utc)
        await self.session.flush()
        await self.session.refresh(token)
        return token
