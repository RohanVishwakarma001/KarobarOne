# Owner: mousamdas156@gmail.com
"""
Router layer for UserRoleMapping.
Exposes endpoints to assign, list, and revoke roles for a user.
"""

import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.rbac import Roles, require_role
from app.db.session import getDb
from app.schemas.userRole import UserRoleAssign, UserRoleResponse
from app.services.userRoleService import UserRoleService

router = APIRouter(
    prefix="/users/{userId}/roles",
    tags=["User Roles"],
    dependencies=[Depends(require_role(Roles.PLATFORM_OWNER, Roles.STORE_OWNER))],
)


@router.post("/", response_model=UserRoleResponse, status_code=status.HTTP_201_CREATED)
async def assignRole(
    userId: uuid.UUID,
    data: UserRoleAssign,
    session: AsyncSession = Depends(getDb),
):
    """
    """
    service = UserRoleService(session)
    return await service.assignRole(userId, data)


@router.get("/", response_model=list[UserRoleResponse])
async def listUserRoles(
    userId: uuid.UUID,
    session: AsyncSession = Depends(getDb),
):
    """
    """
    service = UserRoleService(session)
    return await service.listUserRoles(userId)


@router.delete("/{mappingId}", status_code=status.HTTP_204_NO_CONTENT)
async def revokeRole(
    userId: uuid.UUID,
    mappingId: uuid.UUID,
    session: AsyncSession = Depends(getDb),
):
    """
    """
    service = UserRoleService(session)
    await service.revokeRole(mappingId)
