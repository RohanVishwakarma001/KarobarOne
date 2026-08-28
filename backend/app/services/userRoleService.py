# Owner: mousamdas156@gmail.com
# ================================================================================
# FILE: services/userRoleService.py — User-Role Assignment Service
# ================================================================================
# Why this file is used:
#   - Coordinates user role assignments with optional tenant context scopes.
#
# What components are inside:
#   - UserRoleService:
#       - assignRole()     -> Assigns roles to users inside scoped contexts.
#       - listUserRoles()  -> Returns roles linked to users.
#       - revokeRole()     -> Revokes assignments.
# ================================================================================
"""
Service layer for UserRoleMapping.
Handles assigning and revoking roles for a user, with optional tenant scope.
"""

import uuid
from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptionsCompat import ConflictError, NotFoundError
from app.db.models.userRoleMapping import UserRoleMapping
from app.repositories.roleRepository import RoleRepository
from app.repositories.userRepository import UserRepository
from app.repositories.userRoleRepository import UserRoleRepository
from app.schemas.userRole import UserRoleAssign


class UserRoleService:
    """
    Manages role assignments for users, supporting multi-role and tenant scoping.
    """
    def __init__(self, session: AsyncSession):
        """
        Handles the init functionality.
        """
        self.repo = UserRoleRepository(session)
        self.userRepo = UserRepository(session)
        self.roleRepo = RoleRepository(session)
        self.session = session

    async def assignRole(
        self,
        userId: uuid.UUID,
        data: UserRoleAssign,
    ) -> UserRoleMapping:
        """
        """
        user = await self.userRepo.getById(userId)
        if not user or user.deletedAt is not None:
            raise NotFoundError("User", str(userId))

        role = await self.roleRepo.getById(data.roleId)
        if not role:
            raise NotFoundError("Role", str(data.roleId))

        existing = await self.repo.getByUserRoleTenant(
            userId, data.roleId, data.tenantId
        )
        if existing:
            raise ConflictError(
                "This role is already assigned to the user for this tenant scope"
            )

        mapping = UserRoleMapping(
            userId=userId,
            roleId=data.roleId,
            tenantId=data.tenantId,
            assignedBy=data.assignedBy,
        )
        result = await self.repo.create(mapping)
        await self.session.commit()
        return result

    async def listUserRoles(
        self,
        userId: uuid.UUID,
    ) -> Sequence[UserRoleMapping]:
        """
        """
        user = await self.userRepo.getById(userId)
        if not user or user.deletedAt is not None:
            raise NotFoundError("User", str(userId))
        return await self.repo.getByUserId(userId)

    async def revokeRole(self, mappingId: uuid.UUID) -> None:
        """
        Handles the revoke role functionality.
        """
        mapping = await self.repo.getById(mappingId)
        if not mapping:
            raise NotFoundError("User role mapping", str(mappingId))
        await self.repo.delete(mapping)
        await self.session.commit()