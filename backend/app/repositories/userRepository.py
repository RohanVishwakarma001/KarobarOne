# Owner: mousamdas156@gmail.com
"""
Repository layer for User.
Handles direct database queries for the core user identity table.
"""

import uuid
from typing import Any, Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.user import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        """
        Handles the init functionality.
        """
        self.session = session

    async def getById(self, userId: uuid.UUID) -> User | None:
        """
        Handles the get by id functionality.
        """
        result = await self.session.execute(
            select(User).where(User.id == userId)
        )
        return result.scalar_one_or_none()

    async def getByEmail(self, email: str) -> User | None:
        """
        Handles the get by email functionality.
        """
        result = await self.session.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def getByMobile(self, mobile: str) -> User | None:
        """
        Handles the get by mobile functionality.
        """
        result = await self.session.execute(
            select(User).where(User.mobile == mobile)
        )
        return result.scalar_one_or_none()

    async def getAll(
        self,
        *,
        skip: int = 0,
        limit: int = 20,
        filters: list[Any] | None = None,
    ) -> tuple[Sequence[User], int]:
        """
        """
        query = select(User)
        countQuery = select(func.count()).select_from(User)

        if filters:
            for condition in filters:
                query = query.where(condition)
                countQuery = countQuery.where(condition)

        query = query.offset(skip).limit(limit).order_by(User.createdAt.desc())

        result = await self.session.execute(query)
        totalResult = await self.session.execute(countQuery)

        return result.scalars().all(), totalResult.scalar_one()

    async def create(self, user: User) -> User:
        """
        Handles the create functionality.
        """
        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)
        return user

    async def update(self, user: User, data: dict) -> User:
        """
        Handles the update functionality.
        """
        for key, value in data.items():
            setattr(user, key, value)
        await self.session.flush()
        await self.session.refresh(user)
        return user

    async def delete(self, user: User) -> None:
        """
        Handles the delete functionality.
        """
        await self.session.delete(user)
        await self.session.flush()
