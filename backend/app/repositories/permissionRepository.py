# Owner: mousamdas156@gmail.com
"""
Repository layer for Permission.
Handles direct database queries for permission definitions.
"""

import uuid
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.permission import Permission


class PermissionRepository:
    def __init__(self, session: AsyncSession):
        """
        Handles the init functionality.
        """
        self.session = session

    async def getById(self, permissionId: uuid.UUID) -> Permission | None:
        """
        Handles the get by id functionality.
        """
        result = await self.session.execute(
            select(Permission).where(Permission.id == permissionId)
        )
        return result.scalar_one_or_none()

    async def getByCode(self, permissionCode: str) -> Permission | None:
        """
        Handles the get by code functionality.
        """
        result = await self.session.execute(
            select(Permission).where(Permission.permissionCode == permissionCode)
        )
        return result.scalar_one_or_none()

    async def getAll(self) -> Sequence[Permission]:
        """
        Handles the get all functionality.
        """
        result = await self.session.execute(
            select(Permission).order_by(Permission.createdAt.desc())
        )
        return result.scalars().all()

    async def create(self, permission: Permission) -> Permission:
        """
        Handles the create functionality.
        """
        self.session.add(permission)
        await self.session.flush()
        await self.session.refresh(permission)
        return permission

    async def update(self, permission: Permission, data: dict) -> Permission:
        """
        Handles the update functionality.
        """
        for key, value in data.items():
            setattr(permission, key, value)
        await self.session.flush()
        await self.session.refresh(permission)
        return permission

    async def delete(self, permission: Permission) -> None:
        """
        Handles the delete functionality.
        """
        await self.session.delete(permission)
        await self.session.flush()
