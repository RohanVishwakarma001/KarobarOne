# Owner: mousamdas156@gmail.com
"""
Repository layer for UserRoleMapping.
Handles direct database queries for user-to-role assignments.
"""

import uuid
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.userRoleMapping import UserRoleMapping


class UserRoleRepository:
    def __init__(self, session: AsyncSession):
        """
        Handles the init functionality.
        """
        self.session = session

    async def getById(self, mappingId: uuid.UUID) -> UserRoleMapping | None:
        """
        Handles the get by id functionality.
        """
        result = await self.session.execute(
            select(UserRoleMapping).where(UserRoleMapping.id == mappingId)
        )
        return result.scalar_one_or_none()

    async def getByUserRoleTenant(
        self,
        userId: uuid.UUID,
        roleId: uuid.UUID,
        tenantId: uuid.UUID | None,
    ) -> UserRoleMapping | None:
        """
        """
        result = await self.session.execute(
            select(UserRoleMapping).where(
                UserRoleMapping.userId == userId,
                UserRoleMapping.roleId == roleId,
                UserRoleMapping.tenantId == tenantId,
            )
        )
        return result.scalar_one_or_none()

    async def getByUserId(self, userId: uuid.UUID) -> Sequence[UserRoleMapping]:
        """
        Handles the get by user id functionality.
        """
        result = await self.session.execute(
            select(UserRoleMapping).where(UserRoleMapping.userId == userId)
        )
        return result.scalars().all()

    async def create(self, mapping: UserRoleMapping) -> UserRoleMapping:
        """
        Handles the create functionality.
        """
        self.session.add(mapping)
        await self.session.flush()
        await self.session.refresh(mapping)
        return mapping

    async def delete(self, mapping: UserRoleMapping) -> None:
        """
        Handles the delete functionality.
        """
        await self.session.delete(mapping)
        await self.session.flush()
