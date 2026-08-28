# Owner: mousamdas156@gmail.com
"""
Router layer for StoreStaffPermission.
Exposes endpoints to grant, list, and revoke store-level permission overrides.
"""

import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.rbac import Roles, require_role
from app.db.session import getDb
from app.schemas.storeStaffPermission import (
    StoreStaffPermissionCreate,
    StoreStaffPermissionResponse,
)
from app.services.storeStaffService import StoreStaffPermissionService

router = APIRouter(
    prefix="/users/{userId}/store-permissions",
    tags=["Store Staff Permissions"],
    dependencies=[Depends(require_role(Roles.PLATFORM_OWNER, Roles.STORE_OWNER))],
)


@router.post("/", response_model=StoreStaffPermissionResponse, status_code=status.HTTP_201_CREATED)
async def grantStorePermission(
    userId: uuid.UUID,
    data: StoreStaffPermissionCreate,
    session: AsyncSession = Depends(getDb),
):
    """
    """
    service = StoreStaffPermissionService(session)
    return await service.grantStorePermission(userId, data)


@router.get("/", response_model=list[StoreStaffPermissionResponse])
async def listStorePermissions(
    userId: uuid.UUID,
    storeId: uuid.UUID,
    session: AsyncSession = Depends(getDb),
):
    """
    """
    service = StoreStaffPermissionService(session)
    return await service.listStorePermissions(userId, storeId)


@router.delete("/{recordId}", status_code=status.HTTP_204_NO_CONTENT)
async def revokeStorePermission(
    userId: uuid.UUID,
    recordId: uuid.UUID,
    session: AsyncSession = Depends(getDb),
):
    """
    """
    service = StoreStaffPermissionService(session)
    await service.revokeStorePermission(recordId)
