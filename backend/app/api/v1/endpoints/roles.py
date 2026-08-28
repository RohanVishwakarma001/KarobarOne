# Owner: mousamdas156@gmail.com
"""
Router layer for Role.
Exposes creation, retrieval, listing, update, and deletion endpoints.
"""

import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.rbac import Roles, require_role
from app.db.session import getDb
from app.schemas.role import RoleCreate, RoleResponse, RoleUpdate
from app.services.roleService import RoleService

router = APIRouter(
    prefix="/roles",
    tags=["Roles"],
    dependencies=[Depends(require_role(Roles.PLATFORM_OWNER, Roles.STORE_OWNER))],
)


@router.post("/", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
async def createRole(
    data: RoleCreate,
    session: AsyncSession = Depends(getDb),
):
    """
    """
    service = RoleService(session)
    return await service.createRole(data)


@router.get("/{roleId}", response_model=RoleResponse)
async def getRole(
    roleId: uuid.UUID,
    session: AsyncSession = Depends(getDb),
):
    """
    """
    service = RoleService(session)
    return await service.getRole(roleId)


@router.get("/", response_model=list[RoleResponse])
async def listRoles(
    session: AsyncSession = Depends(getDb),
):
    """
    """
    service = RoleService(session)
    return await service.listRoles()


@router.patch("/{roleId}", response_model=RoleResponse)
async def updateRole(
    roleId: uuid.UUID,
    data: RoleUpdate,
    session: AsyncSession = Depends(getDb),
):
    """
    """
    service = RoleService(session)
    return await service.updateRole(roleId, data)


@router.delete("/{roleId}", status_code=status.HTTP_204_NO_CONTENT)
async def deleteRole(
    roleId: uuid.UUID,
    session: AsyncSession = Depends(getDb),
):
    """
    """
    service = RoleService(session)
    await service.deleteRole(roleId)
