# Owner: mousamdas156@gmail.com
"""
Repository layer for UserSession.
Handles direct database queries for active login session tracking.
"""

import uuid
from datetime import datetime, timezone
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.userSession import UserSession


class UserSessionRepository:
    def __init__(self, session: AsyncSession):
        """
        Handles the init functionality.
        """
        self.session = session

    async def getById(self, sessionId: uuid.UUID) -> UserSession | None:
        """
        Handles the get by id functionality.
        """
        result = await self.session.execute(
            select(UserSession).where(UserSession.id == sessionId)
        )
        return result.scalar_one_or_none()

    async def getByRefreshTokenId(
        self,
        refreshTokenId: uuid.UUID,
    ) -> UserSession | None:
        """
        """
        result = await self.session.execute(
            select(UserSession).where(UserSession.refreshTokenId == refreshTokenId)
        )
        return result.scalar_one_or_none()

    async def getActiveByUserId(self, userId: uuid.UUID) -> Sequence[UserSession]:
        """
        Handles the get active by user id functionality.
        """
        result = await self.session.execute(
            select(UserSession).where(
                UserSession.userId == userId,
                UserSession.isActive.is_(True),
            )
        )
        return result.scalars().all()

    async def create(self, session_: UserSession) -> UserSession:
        """
        Handles the create functionality.
        """
        self.session.add(session_)
        await self.session.flush()
        await self.session.refresh(session_)
        return session_

    async def endSession(self, session_: UserSession) -> UserSession:
        """
        Handles the end session functionality.
        """
        session_.logoutAt = datetime.now(timezone.utc)
        session_.isActive = False
        await self.session.flush()
        await self.session.refresh(session_)
        return session_
