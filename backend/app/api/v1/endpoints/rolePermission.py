# Owner: mousamdas156@gmail.com
"""
Router layer for RolePermissionMapping.
Exposes endpoints to grant, list, and revoke permissions for a role.
"""

import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.rbac import Roles, require_role
from app.db.session import getDb
from app.schemas.rolePermission import RolePermissionCreate, RolePermissionResponse
from app.services.rolePermissionService import RolePermissionService

router = APIRouter(
    prefix="/roles/{roleId}/permissions",
    tags=["Role Permissions"],
    dependencies=[Depends(require_role(Roles.PLATFORM_OWNER, Roles.STORE_OWNER))],
)


@router.post("/", response_model=RolePermissionResponse, status_code=status.HTTP_201_CREATED)
async def grantPermission(
    roleId: uuid.UUID,
    data: RolePermissionCreate,
    session: AsyncSession = Depends(getDb),
):
    """
    """
    service = RolePermissionService(session)
    return await service.grantPermission(roleId, data)


@router.get("/", response_model=list[RolePermissionResponse])
async def listRolePermissions(
    roleId: uuid.UUID,
    session: AsyncSession = Depends(getDb),
):
    """
    """
    service = RolePermissionService(session)
    return await service.listRolePermissions(roleId)


@router.delete("/{mappingId}", status_code=status.HTTP_204_NO_CONTENT)
async def revokePermission(
    roleId: uuid.UUID,
    mappingId: uuid.UUID,
    session: AsyncSession = Depends(getDb),
):
    """
    """
    service = RolePermissionService(session)
    await service.revokePermission(mappingId)
