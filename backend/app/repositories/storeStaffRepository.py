# Owner: mousamdas156@gmail.com
"""
Repository layer for StoreStaffPermission.
Handles direct database queries for store-level permission overrides.
"""

import uuid
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.storeStaffPermission import StoreStaffPermission


class StoreStaffPermissionRepository:
    def __init__(self, session: AsyncSession):
        """
        Handles the init functionality.
        """
        self.session = session

    async def getById(self, recordId: uuid.UUID) -> StoreStaffPermission | None:
        """
        Handles the get by id functionality.
        """
        result = await self.session.execute(
            select(StoreStaffPermission).where(StoreStaffPermission.id == recordId)
        )
        return result.scalar_one_or_none()

    async def getByUserStorePermission(
        self,
        userId: uuid.UUID,
        storeId: uuid.UUID,
        permissionId: uuid.UUID,
    ) -> StoreStaffPermission | None:
        """
        """
        result = await self.session.execute(
            select(StoreStaffPermission).where(
                StoreStaffPermission.userId == userId,
                StoreStaffPermission.storeId == storeId,
                StoreStaffPermission.permissionId == permissionId,
            )
        )
        return result.scalar_one_or_none()

    async def getByUserAndStore(
        self,
        userId: uuid.UUID,
        storeId: uuid.UUID,
    ) -> Sequence[StoreStaffPermission]:
        """
        """
        result = await self.session.execute(
            select(StoreStaffPermission).where(
                StoreStaffPermission.userId == userId,
                StoreStaffPermission.storeId == storeId,
            )
        )
        return result.scalars().all()

    async def create(self, record: StoreStaffPermission) -> StoreStaffPermission:
        """
        Handles the create functionality.
        """
        self.session.add(record)
        await self.session.flush()
        await self.session.refresh(record)
        return record

    async def delete(self, record: StoreStaffPermission) -> None:
        """
        Handles the delete functionality.
        """
        await self.session.delete(record)
        await self.session.flush()
