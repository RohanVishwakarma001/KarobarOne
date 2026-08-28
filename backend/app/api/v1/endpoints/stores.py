# Owner: mousamdas156@gmail.com
"""
================================================================================
STORES ENDPOINTS ROUTER
================================================================================
Yeh file stores ke main REST API endpoints (GET, POST, PATCH, DELETE) ko expose karti hai.
This module defines the routing layer for storefront configurations.

Why it is used:
- Serves as the primary public and admin interfaces for modifying and loading stores.
================================================================================
"""

import uuid
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import getCurrentUserWithRole
from app.core.rbac import Roles, require_role
from app.db.session import getDb
from app.schemas.store import StoreCreate, StoreResponse, StoreUpdate
from app.services.storeService import StoreService

# Router setup
router = APIRouter(prefix="/stores", tags=["Stores"])


@router.post(
    "/",
    response_model=StoreResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role(Roles.PLATFORM_OWNER, Roles.STORE_OWNER))],
)
async def createStore(
    data: StoreCreate,
    session: AsyncSession = Depends(getDb),
):
    """
    Creates a new storefront website. Returns 201 Created.
    """
    service = StoreService(session)
    return await service.createStore(data)


@router.get("/{storeId}", response_model=StoreResponse)
async def getStore(
    storeId: uuid.UUID,
    session: AsyncSession = Depends(getDb),
):
    """
    Fetches store profile using its unique UUID database primary key.
    """
    service = StoreService(session)
    return await service.getStore(storeId)


@router.get("/slug/{storeSlug}", response_model=StoreResponse)
async def getStoreBySlug(
    storeSlug: str,
    session: AsyncSession = Depends(getDb),
):
    """
    Fetches store profile using its unique web URL friendly slug (e.g. /slug/jacks-boutique).
    """
    service = StoreService(session)
    return await service.getStoreBySlug(storeSlug)


@router.get("/", response_model=list[StoreResponse])
async def listStores(
    tenantId: uuid.UUID | None = Query(None),
    current_user: dict = Depends(getCurrentUserWithRole),
    session: AsyncSession = Depends(getDb),
):
    """
    Lists stores. Can filter by tenantId to see stores belonging to a specific owner.
    """
    user_role = current_user.get("role")
    if user_role not in (Roles.PLATFORM_OWNER, Roles.PLATFORM_STAFF):
        user_tenant_id = current_user.get("tenantId")
        if user_tenant_id:
            tenantId = uuid.UUID(str(user_tenant_id)) if isinstance(user_tenant_id, str) else user_tenant_id
        else:
            tenantId = None
    service = StoreService(session)
    return await service.listStores(tenantId=tenantId)


@router.patch("/{storeId}", response_model=StoreResponse)
async def updateStore(
    storeId: uuid.UUID,
    data: StoreUpdate,
    current_user: dict = Depends(getCurrentUserWithRole),
    session: AsyncSession = Depends(getDb),
):
    """
    Updates store details (such as tagline, name, or design-related media links).
    """
    user_role = current_user.get("role")
    if user_role not in (Roles.PLATFORM_OWNER, Roles.STORE_OWNER, Roles.STORE_ADMIN):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Access denied. Required role(s): platform_owner, store_owner, store_admin. Your role: {user_role}",
        )
    service = StoreService(session)
    return await service.updateStore(storeId, data)


@router.delete(
    "/{storeId}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_role(Roles.PLATFORM_OWNER))],
)
@router.delete(
    "/{storeId}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_role(Roles.PLATFORM_OWNER))],
)
async def deleteStore(
    storeId: uuid.UUID,
    session: AsyncSession = Depends(getDb),
):
    """
    Deletes a store profile. Returns 204 No Content.
    """
    service = StoreService(session)
    await service.deleteStore(storeId)


@router.post("/{storeId}/submit", response_model=StoreResponse)
async def submitStoreForApproval(
    storeId: uuid.UUID,
    session: AsyncSession = Depends(getDb),
):
    """
    Submit a store for admin approval.
    """
    service = StoreService(session)
    return await service.submitForApproval(storeId)


@router.post("/{storeId}/publish", response_model=StoreResponse)
async def publishStore(
    storeId: uuid.UUID,
    session: AsyncSession = Depends(getDb),
):
    """
    Publish an approved store.
    """
    service = StoreService(session)
    return await service.publishStore(storeId)
@router.get("/{storeId}/preview")
async def previewStore(
    storeId: uuid.UUID,
    session: AsyncSession = Depends(getDb),
):
    """
    Returns preview URL for a store website.
    """
    service = StoreService(session)
    return await service.previewStore(storeId)
@router.patch("/{storeId}/theme", response_model=StoreResponse)
async def changeTheme(
    storeId: uuid.UUID,
    themeId: uuid.UUID,
    session: AsyncSession = Depends(getDb),
):
    """
    Change website theme.
    """
    service = StoreService(session)
    return await service.changeTheme(storeId, themeId)
@router.patch("/{storeId}/theme")
async def changeTheme(
    storeId: uuid.UUID,
    themeId: uuid.UUID,
    session: AsyncSession = Depends(getDb),
):
    service = StoreService(session)
    return await service.changeTheme(storeId, themeId)
@router.post("/{storeId}/generate-ai")
async def generateAI(
    storeId: uuid.UUID,
    session: AsyncSession = Depends(getDb),
):
    service = StoreService(session)
    return await service.generateAI(storeId)
@router.post("/{storeId}/connect-domain")
async def connectDomain(
    storeId: uuid.UUID,
    domain: str,
    session: AsyncSession = Depends(getDb),
):
    service = StoreService(session)
    return await service.connectDomain(storeId, domain)

@router.get("/{storeId}/status")
async def websiteStatus(
    storeId: uuid.UUID,
    session: AsyncSession = Depends(getDb),
):
    service = StoreService(session)
    return await service.websiteStatus(storeId)