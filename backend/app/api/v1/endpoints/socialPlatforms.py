# Owner: mousamdas156@gmail.com
"""
================================================================================
SOCIAL PLATFORMS ENDPOINTS ROUTER
================================================================================
Yeh file social platforms master table ke REST API endpoints expose karti hai.
This module defines the routing layer for creating and managing master platform categories.

Why it is used:
- Provides admin endpoints to register new platform configurations (like Instagram, TikTok).
================================================================================
"""

import uuid
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import getDb
from app.schemas.socialPlatform import (
    SocialPlatformCreate,
    SocialPlatformResponse,
    SocialPlatformUpdate,
)
from app.services.socialPlatformService import SocialPlatformService

# Router config
router = APIRouter(prefix="/social-platforms", tags=["Social Platforms"])


@router.post("/", response_model=SocialPlatformResponse, status_code=status.HTTP_201_CREATED)
async def createPlatform(
    data: SocialPlatformCreate,
    session: AsyncSession = Depends(getDb),
):
    """
    Registers a new platform. Returns 201 Created.
    """
    service = SocialPlatformService(session)
    return await service.createPlatform(data)


@router.get("/{platformId}", response_model=SocialPlatformResponse)
async def getPlatform(
    platformId: uuid.UUID,
    session: AsyncSession = Depends(getDb),
):
    """
    Retrieves platform details by database ID.
    """
    service = SocialPlatformService(session)
    return await service.getPlatform(platformId)


@router.get("/", response_model=list[SocialPlatformResponse])
async def listPlatforms(
    activeOnly: bool = Query(False),
    session: AsyncSession = Depends(getDb),
):
    """
    Lists platforms. Optional activeOnly query param filters to only available platforms.
    """
    service = SocialPlatformService(session)
    return await service.listPlatforms(activeOnly=activeOnly)


@router.patch("/{platformId}", response_model=SocialPlatformResponse)
async def updatePlatform(
    platformId: uuid.UUID,
    data: SocialPlatformUpdate,
    session: AsyncSession = Depends(getDb),
):
    """
    Updates platform properties (e.g. changing iconMediaId or baseUrl pattern).
    """
    service = SocialPlatformService(session)
    return await service.updatePlatform(platformId, data)


@router.delete("/{platformId}", status_code=status.HTTP_204_NO_CONTENT)
async def deletePlatform(
    platformId: uuid.UUID,
    session: AsyncSession = Depends(getDb),
):
    """
    Deletes a platform master category. Returns 204 No Content.
    """
    service = SocialPlatformService(session)
    await service.deletePlatform(platformId)
