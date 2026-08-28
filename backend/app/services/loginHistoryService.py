# Owner: mousamdas156@gmail.com
# ================================================================================
# FILE: services/loginHistoryService.py — Login Audit Trail Service
# ================================================================================
# Why this file is used:
#   - Tracks successful and failed authentication processes.
#
# What components are inside:
#   - LoginHistoryService:
#       - recordAttempt()  -> Adds authentication logs (captures failures with null IDs).
#       - getHistory()     -> Returns login audit logs for users.
# ================================================================================
"""
Service layer for LoginHistory.
Handles recording and retrieving authentication audit entries.
"""

import uuid
from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptionsCompat import NotFoundError
from app.db.models.loginHistory import LoginHistory
from app.repositories.loginHistoryRepository import LoginHistoryRepository
from app.repositories.userRepository import UserRepository
from app.schemas.loginHistory import LoginHistoryCreate


class LoginHistoryService:
    def __init__(self, session: AsyncSession):
        """
        Handles the init functionality.
        """
        self.repo = LoginHistoryRepository(session)
        self.userRepo = UserRepository(session)
        self.session = session

    async def recordAttempt(self, data: LoginHistoryCreate) -> LoginHistory:
        """
        Records a login attempt (success or failure). Does not raise if the
        user is not found, since failed attempts with unknown emails are
        still valid audit entries (userId stays NULL in that case).
        """
        record = LoginHistory(**data.model_dump())
        result = await self.repo.create(record)
        await self.session.commit()
        return result

    async def getHistory(
        self,
        userId: uuid.UUID,
        *,
        skip: int = 0,
        limit: int = 20,
    ) -> tuple[Sequence[LoginHistory], int]:
        """
        """
        user = await self.userRepo.getById(userId)
        if not user or user.deletedAt is not None:
            raise NotFoundError("User", str(userId))
        return await self.repo.getByUserId(userId, skip=skip, limit=limit)