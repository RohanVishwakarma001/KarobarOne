# Owner: mousamdas156@gmail.com
# ================================================================================
# FILE: services/rolePermissionService.py — Role-Permission Mapping Service
# ================================================================================
# Why this file is used:
#   - Coordinates grant configurations mapping permissions to target roles.
#
# What components are inside:
#   - RolePermissionService:
#       - grantPermission()      -> Pairs a permission with a role.
#       - listRolePermissions()  -> Returns permissions granted to a specific role.
#       - revokePermission()     -> Removes role permission pairs.
# ================================================================================
"""
Service layer for RolePermissionMapping.
Handles granting and revoking permissions for a role.
"""

import uuid
from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptionsCompat import ConflictError, NotFoundError
from app.db.models.rolePermissionMapping import RolePermissionMapping
from app.repositories.permissionRepository import PermissionRepository
from app.repositories.rolePermissionRepository import RolePermissionRepository
from app.repositories.roleRepository import RoleRepository
from app.schemas.rolePermission import RolePermissionCreate


class RolePermissionService:
    """
    Manages the many-to-many grant relationship between roles and permissions.
    """
    def __init__(self, session: AsyncSession):
        """
        Handles the init functionality.
        """
        self.repo = RolePermissionRepository(session)
        self.roleRepo = RoleRepository(session)
        self.permissionRepo = PermissionRepository(session)
        self.session = session

    async def grantPermission(
        self,
        roleId: uuid.UUID,
        data: RolePermissionCreate,
    ) -> RolePermissionMapping:
        """
        """
        role = await self.roleRepo.getById(roleId)
        if not role:
            raise NotFoundError("Role", str(roleId))

        permission = await self.permissionRepo.getById(data.permissionId)
        if not permission:
            raise NotFoundError("Permission", str(data.permissionId))

        existing = await self.repo.getByRoleAndPermission(
            roleId, data.permissionId
        )
        if existing:
            raise ConflictError(
                "This permission is already granted to the role"
            )

        mapping = RolePermissionMapping(
            roleId=roleId,
            permissionId=data.permissionId,
        )
        result = await self.repo.create(mapping)
        await self.session.commit()
        return result

    async def listRolePermissions(
        self,
        roleId: uuid.UUID,
    ) -> Sequence[RolePermissionMapping]:
        """
        """
        role = await self.roleRepo.getById(roleId)
        if not role:
            raise NotFoundError("Role", str(roleId))
        return await self.repo.getByRoleId(roleId)

    async def revokePermission(self, mappingId: uuid.UUID) -> None:
        """
        Handles the revoke permission functionality.
        """
        mapping = await self.repo.getById(mappingId)
        if not mapping:
            raise NotFoundError("Role permission mapping", str(mappingId))
        await self.repo.delete(mapping)
        await self.session.commit()