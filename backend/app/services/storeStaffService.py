# Owner: mousamdas156@gmail.com
# ================================================================================
# FILE: services/storeStaffService.py — Store Staff Permission Override Service
# ================================================================================
# Why this file is used:
#   - Coordinates store-scoped permission assignments.
#
# What components are inside:
#   - StoreStaffPermissionService:
#       - grantStorePermission()  -> Grants permissions to users at a store scope.
#       - listStorePermissions()  -> Returns store-scoped permissions.
#       - revokeStorePermission() -> Revokes permissions.
# ================================================================================
"""
Service layer for StoreStaffPermission.
Handles granting and revoking store-level fine-grained permission overrides.
"""

import uuid
from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptionsCompat import ConflictError, NotFoundError
from app.db.models.storeStaffPermission import StoreStaffPermission
from app.repositories.permissionRepository import PermissionRepository
from app.repositories.storeStaffRepository import StoreStaffPermissionRepository
from app.repositories.userRepository import UserRepository
from app.schemas.storeStaffPermission import StoreStaffPermissionCreate


class StoreStaffPermissionService:
    """
    Manages store-scoped permission overrides for staff members.
    """
    def __init__(self, session: AsyncSession):
        """
        Handles the init functionality.
        """
        self.repo = StoreStaffPermissionRepository(session)
        self.userRepo = UserRepository(session)
        self.permissionRepo = PermissionRepository(session)
        self.session = session

    async def grantStorePermission(
        self,
        userId: uuid.UUID,
        data: StoreStaffPermissionCreate,
    ) -> StoreStaffPermission:
        """
        """
        user = await self.userRepo.getById(userId)
        if not user or user.deletedAt is not None:
            raise NotFoundError("User", str(userId))

        permission = await self.permissionRepo.getById(data.permissionId)
        if not permission:
            raise NotFoundError("Permission", str(data.permissionId))

        existing = await self.repo.getByUserStorePermission(
            userId, data.storeId, data.permissionId
        )
        if existing:
            raise ConflictError(
                "This permission is already granted to the user for this store"
            )

        record = StoreStaffPermission(
            userId=userId,
            storeId=data.storeId,
            permissionId=data.permissionId,
            grantedBy=data.grantedBy,
        )
        result = await self.repo.create(record)
        await self.session.commit()
        return result

    async def listStorePermissions(
        self,
        userId: uuid.UUID,
        storeId: uuid.UUID,
    ) -> Sequence[StoreStaffPermission]:
        """
        """
        user = await self.userRepo.getById(userId)
        if not user or user.deletedAt is not None:
            raise NotFoundError("User", str(userId))
        return await self.repo.getByUserAndStore(userId, storeId)

    async def revokeStorePermission(self, recordId: uuid.UUID) -> None:
        """
        Handles the revoke store permission functionality.
        """
        record = await self.repo.getById(recordId)
        if not record:
            raise NotFoundError("Store staff permission", str(recordId))
        await self.repo.delete(record)
        await self.session.commit()