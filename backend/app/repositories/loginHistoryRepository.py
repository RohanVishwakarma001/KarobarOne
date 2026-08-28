# Owner: mousamdas156@gmail.com
"""
Repository layer for LoginHistory.
Handles direct database queries for the authentication audit log.
"""

import uuid
from typing import Any, Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.loginHistory import LoginHistory


class LoginHistoryRepository:
    def __init__(self, session: AsyncSession):
        """
        Handles the init functionality.
        """
        self.session = session

    async def getById(self, recordId: uuid.UUID) -> LoginHistory | None:
        """
        Handles the get by id functionality.
        """
        result = await self.session.execute(
            select(LoginHistory).where(LoginHistory.id == recordId)
        )
        return result.scalar_one_or_none()

    async def getByUserId(
        self,
        userId: uuid.UUID,
        *,
        skip: int = 0,
        limit: int = 20,
    ) -> tuple[Sequence[LoginHistory], int]:
        """
        """
        query = (
            select(LoginHistory)
            .where(LoginHistory.userId == userId)
            .order_by(LoginHistory.createdAt.desc())
            .offset(skip)
            .limit(limit)
        )
        countQuery = select(func.count()).select_from(LoginHistory).where(
            LoginHistory.userId == userId
        )

        result = await self.session.execute(query)
        totalResult = await self.session.execute(countQuery)

        return result.scalars().all(), totalResult.scalar_one()

    async def create(self, record: LoginHistory) -> LoginHistory:
        """
        Handles the create functionality.
        """
        self.session.add(record)
        await self.session.flush()
        await self.session.refresh(record)
        return record
