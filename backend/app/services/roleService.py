# Owner: mousamdas156@gmail.com
# ================================================================================
# FILE: services/roleService.py — Role Management Service (RBAC)
# ================================================================================
# Why this file is used:
#   - Coordinates role configurations used for access control.
#
# What components are inside:
#   - RoleService:
#       - createRole()  -> Adds roles, checking code uniqueness.
#       - getRole()     -> Resolves role templates.
#       - listRoles()   -> Returns active roles.
#       - updateRole()  -> Updates role names and metrics.
#       - deleteRole()  -> Removes custom roles, blocking deletion of system roles.
# ================================================================================
"""
Service layer for Role.
Handles creation, listing, updating, and deletion of role definitions.
"""

import uuid
from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptionsCompat import BusinessValidationError, ConflictError, NotFoundError
from app.db.models.role import Role
from app.repositories.roleRepository import RoleRepository
from app.schemas.role import RoleCreate, RoleUpdate


class RoleService:
    """
    Manages role definitions used for access control assignments.
    """
    def __init__(self, session: AsyncSession):
        """
        Handles the init functionality.
        """
        self.repo = RoleRepository(session)
        self.session = session

    async def createRole(self, data: RoleCreate) -> Role:
        """
        Creates a new role.
        Validates that the roleCode is globally unique.
        """
        if await self.repo.getByCode(data.roleCode):
            raise ConflictError(
                f"Role with code '{data.roleCode}' already exists"
            )
        role = Role(**data.model_dump())
        result = await self.repo.create(role)
        await self.session.commit()
        return result

    async def getRole(self, roleId: uuid.UUID) -> Role:
        """
        Handles the get role functionality.
        """
        role = await self.repo.getById(roleId)
        if not role:
            raise NotFoundError("Role", str(roleId))
        return role

    async def listRoles(self) -> Sequence[Role]:
        """
        Handles the list roles functionality.
        """
        return await self.repo.getAll()

    async def updateRole(self, roleId: uuid.UUID, data: RoleUpdate) -> Role:
        """
        Handles the update role functionality.
        """
        role = await self.repo.getById(roleId)
        if not role:
            raise NotFoundError("Role", str(roleId))

        updateData = data.model_dump(exclude_unset=True)
        if not updateData:
            return role

        result = await self.repo.update(role, updateData)
        await self.session.commit()
        return result

    async def deleteRole(self, roleId: uuid.UUID) -> None:
        """
        Deletes a role. System roles (isSystemRole=True) cannot be deleted.
        """
        role = await self.repo.getById(roleId)
        if not role:
            raise NotFoundError("Role", str(roleId))
        if role.isSystemRole:
            raise BusinessValidationError(
                "Cannot delete a system-defined role"
            )
        await self.repo.delete(role)
        await self.session.commit()