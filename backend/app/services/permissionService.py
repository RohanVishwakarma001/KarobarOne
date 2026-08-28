# Owner: mousamdas156@gmail.com
# ================================================================================
# FILE: services/permissionService.py — Permission Management Service (RBAC)
# ================================================================================
# Why this file is used:
#   - Manages granular security permission definitions.
#
# What components are inside:
#   - PermissionService:
#       - createPermission()  -> Adds permissions, checking code uniqueness.
#       - getPermission()     -> Resolves permission identifiers.
#       - listPermissions()   -> Exposes configured scopes.
#       - updatePermission()  -> Modifies permission parameters.
#       - deletePermission()  -> Removes permission definitions.
# ================================================================================
"""
Service layer for Permission.
Handles creation, listing, updating, and deletion of permission definitions.
"""

import uuid
from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptionsCompat import ConflictError, NotFoundError
from app.db.models.permission import Permission
from app.repositories.permissionRepository import PermissionRepository
from app.schemas.permission import PermissionCreate, PermissionUpdate


class PermissionService:
    """
    Manages granular permission definitions used for access control.
    """
    def __init__(self, session: AsyncSession):
        """
        Handles the init functionality.
        """
        self.repo = PermissionRepository(session)
        self.session = session

    async def createPermission(self, data: PermissionCreate) -> Permission:
        """
        Creates a new permission.
        Validates that the permissionCode is globally unique.
        """
        if await self.repo.getByCode(data.permissionCode):
            raise ConflictError(
                f"Permission with code '{data.permissionCode}' already exists"
            )
        permission = Permission(**data.model_dump())
        result = await self.repo.create(permission)
        await self.session.commit()
        return result

    async def getPermission(self, permissionId: uuid.UUID) -> Permission:
        """
        Handles the get permission functionality.
        """
        permission = await self.repo.getById(permissionId)
        if not permission:
            raise NotFoundError("Permission", str(permissionId))
        return permission

    async def listPermissions(self) -> Sequence[Permission]:
        """
        Handles the list permissions functionality.
        """
        return await self.repo.getAll()

    async def updatePermission(
        self,
        permissionId: uuid.UUID,
        data: PermissionUpdate,
    ) -> Permission:
        """
        """
        permission = await self.repo.getById(permissionId)
        if not permission:
            raise NotFoundError("Permission", str(permissionId))

        updateData = data.model_dump(exclude_unset=True)
        if not updateData:
            return permission

        result = await self.repo.update(permission, updateData)
        await self.session.commit()
        return result

    async def deletePermission(self, permissionId: uuid.UUID) -> None:
        """
        Handles the delete permission functionality.
        """
        permission = await self.repo.getById(permissionId)
        if not permission:
            raise NotFoundError("Permission", str(permissionId))
        await self.repo.delete(permission)
        await self.session.commit()