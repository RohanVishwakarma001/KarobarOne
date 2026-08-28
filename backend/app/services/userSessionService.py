# Owner: mousamdas156@gmail.com
# ================================================================================
# FILE: services/userSessionService.py — User Login Session Service
# ================================================================================
# Why this file is used:
#   - Coordinates login tracking session logs.
#
# What components are inside:
#   - UserSessionService:
#       - startSession()        -> Registers sessions, linking tokens.
#       - listActiveSessions()  -> Returns active sessions.
#       - endSession()          -> Terminates sessions.
# ================================================================================
"""
Service layer for UserSession.
Handles starting, listing, and ending active login sessions.
"""

import uuid
from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptionsCompat import NotFoundError
from app.db.models.userSession import UserSession
from app.repositories.refreshTokenRepository import RefreshTokenRepository
from app.repositories.userRepository import UserRepository
from app.repositories.userSessionRepository import UserSessionRepository
from app.schemas.userSession import UserSessionCreate


class UserSessionService:
    def __init__(self, session: AsyncSession):
        """
        Handles the init functionality.
        """
        self.repo = UserSessionRepository(session)
        self.userRepo = UserRepository(session)
        self.tokenRepo = RefreshTokenRepository(session)
        self.session = session

    async def startSession(
        self,
        userId: uuid.UUID,
        data: UserSessionCreate,
    ) -> UserSession:
        """
        """
        user = await self.userRepo.getById(userId)
        if not user or user.deletedAt is not None:
            raise NotFoundError("User", str(userId))

        token = await self.tokenRepo.getById(data.refreshTokenId)
        if not token:
            raise NotFoundError("Refresh token", str(data.refreshTokenId))

        userSession = UserSession(
            userId=userId,
            **data.model_dump(),
        )
        result = await self.repo.create(userSession)
        await self.session.commit()
        return result

    async def listActiveSessions(self, userId: uuid.UUID) -> Sequence[UserSession]:
        """
        Handles the list active sessions functionality.
        """
        user = await self.userRepo.getById(userId)
        if not user or user.deletedAt is not None:
            raise NotFoundError("User", str(userId))
        return await self.repo.getActiveByUserId(userId)

    async def endSession(self, sessionId: uuid.UUID) -> UserSession:
        """
        Handles the end session functionality.
        """
        userSession = await self.repo.getById(sessionId)
        if not userSession:
            raise NotFoundError("User session", str(sessionId))
        result = await self.repo.endSession(userSession)
        await self.session.commit()
        return result