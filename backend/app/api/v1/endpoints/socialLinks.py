# Owner: mousamdas156@gmail.com
"""
================================================================================
SOCIAL LINKS ENDPOINTS ROUTER
================================================================================
Yeh file social links map karne ke REST API endpoints expose karti hai.
This module defines the routing layer for mapping stores to social platform links.

Why it is used:
- Receives HTTP client operations for connecting handles like Twitter or Instagram.
================================================================================
"""

import uuid
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import getDb
from app.schemas.socialLink import (
    SocialLinkCreate,
    SocialLinkResponse,
    SocialLinkUpdate,
)
from app.services.socialLinkService import SocialLinkService

# Route configuration
router = APIRouter(prefix="/social-links", tags=["Social Links"])


@router.post("/", response_model=SocialLinkResponse, status_code=status.HTTP_201_CREATED)
async def createSocialLink(
    data: SocialLinkCreate,
    session: AsyncSession = Depends(getDb),
):
    """
    Creates a social link mapping.
    """
    service = SocialLinkService(session)
    return await service.createSocialLink(data)


@router.get("/{socialLinkId}", response_model=SocialLinkResponse)
async def getSocialLink(
    socialLinkId: uuid.UUID,
    session: AsyncSession = Depends(getDb),
):
    """
    Retrieves a single social link mapping by ID.
    """
    service = SocialLinkService(session)
    return await service.getSocialLink(socialLinkId)


@router.get("/", response_model=list[SocialLinkResponse])
async def listSocialLinks(
    storeId: uuid.UUID | None = Query(None),
    session: AsyncSession = Depends(getDb),
):
    """
    Lists all social link maps, with optional filtering by storeId.
    """
    service = SocialLinkService(session)
    return await service.listSocialLinks(storeId=storeId)


@router.patch("/{socialLinkId}", response_model=SocialLinkResponse)
async def updateSocialLink(
    socialLinkId: uuid.UUID,
    data: SocialLinkUpdate,
    session: AsyncSession = Depends(getDb),
):
    """
    Updates profile url details or active state of a social link.
    """
    service = SocialLinkService(session)
    return await service.updateSocialLink(socialLinkId, data)


@router.delete("/{socialLinkId}", status_code=status.HTTP_204_NO_CONTENT)
async def deleteSocialLink(
    socialLinkId: uuid.UUID,
    session: AsyncSession = Depends(getDb),
):
    """
    Deletes a social link mapping. Returns 204 No Content.
    """
    service = SocialLinkService(session)
    await service.deleteSocialLink(socialLinkId)
