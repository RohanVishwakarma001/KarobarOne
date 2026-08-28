# Owner: mousamdas156@gmail.com
"""
Router layer for Permission.
Exposes creation, retrieval, listing, update, and deletion endpoints.
"""

import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.rbac import Roles, require_role
from app.db.session import getDb
from app.schemas.permission import PermissionCreate, PermissionResponse, PermissionUpdate
from app.services.permissionService import PermissionService

router = APIRouter(
    prefix="/permissions",
    tags=["Permissions"],
    dependencies=[Depends(require_role(Roles.PLATFORM_OWNER, Roles.STORE_OWNER))],
)


@router.post("/", response_model=PermissionResponse, status_code=status.HTTP_201_CREATED)
async def createPermission(
    data: PermissionCreate,
    session: AsyncSession = Depends(getDb),
):
    """
    """
    service = PermissionService(session)
    return await service.createPermission(data)


@router.get("/{permissionId}", response_model=PermissionResponse)
async def getPermission(
    permissionId: uuid.UUID,
    session: AsyncSession = Depends(getDb),
):
    """
    """
    service = PermissionService(session)
    return await service.getPermission(permissionId)


@router.get("/", response_model=list[PermissionResponse])
async def listPermissions(
    session: AsyncSession = Depends(getDb),
):
    """
    """
    service = PermissionService(session)
    return await service.listPermissions()


@router.patch("/{permissionId}", response_model=PermissionResponse)
async def updatePermission(
    permissionId: uuid.UUID,
    data: PermissionUpdate,
    session: AsyncSession = Depends(getDb),
):
    """
    """
    service = PermissionService(session)
    return await service.updatePermission(permissionId, data)


@router.delete("/{permissionId}", status_code=status.HTTP_204_NO_CONTENT)
async def deletePermission(
    permissionId: uuid.UUID,
    session: AsyncSession = Depends(getDb),
):
    """
    """
    service = PermissionService(session)
    await service.deletePermission(permissionId)
