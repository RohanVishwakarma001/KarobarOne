# Owner: mousamdas156@gmail.com
"""
Repository layer for RolePermissionMapping.
Handles direct database queries for role-to-permission grants.
"""

import uuid
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.rolePermissionMapping import RolePermissionMapping


class RolePermissionRepository:
    def __init__(self, session: AsyncSession):
        """
        Handles the init functionality.
        """
        self.session = session

    async def getById(self, mappingId: uuid.UUID) -> RolePermissionMapping | None:
        """
        Handles the get by id functionality.
        """
        result = await self.session.execute(
            select(RolePermissionMapping).where(RolePermissionMapping.id == mappingId)
        )
        return result.scalar_one_or_none()

    async def getByRoleAndPermission(
        self,
        roleId: uuid.UUID,
        permissionId: uuid.UUID,
    ) -> RolePermissionMapping | None:
        """
        """
        result = await self.session.execute(
            select(RolePermissionMapping).where(
                RolePermissionMapping.roleId == roleId,
                RolePermissionMapping.permissionId == permissionId,
            )
        )
        return result.scalar_one_or_none()

    async def getByRoleId(self, roleId: uuid.UUID) -> Sequence[RolePermissionMapping]:
        """
        Handles the get by role id functionality.
        """
        result = await self.session.execute(
            select(RolePermissionMapping).where(RolePermissionMapping.roleId == roleId)
        )
        return result.scalars().all()

    async def create(self, mapping: RolePermissionMapping) -> RolePermissionMapping:
        """
        Handles the create functionality.
        """
        self.session.add(mapping)
        await self.session.flush()
        await self.session.refresh(mapping)
        return mapping

    async def delete(self, mapping: RolePermissionMapping) -> None:
        """
        Handles the delete functionality.
        """
        await self.session.delete(mapping)
        await self.session.flush()
