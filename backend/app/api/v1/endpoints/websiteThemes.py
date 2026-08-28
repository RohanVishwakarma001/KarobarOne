# Owner: mousamdas156@gmail.com
"""
================================================================================
WEBSITE THEMES ENDPOINTS ROUTER
================================================================================
Yeh file website themes ke REST API endpoints expose karti hai.
This module defines the routing layer for design theme templates.

Why it is used:
- Exposes administration endpoints to add, change, list, or delete website design theme presets.
================================================================================
"""

import uuid
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import getDb
from app.schemas.websiteTheme import (
    WebsiteThemeCreate,
    WebsiteThemeResponse,
    WebsiteThemeUpdate,
)
from app.services.websiteThemeService import WebsiteThemeService

# Router configuration
router = APIRouter(prefix="/website-themes", tags=["Website Themes"])


@router.post("/", response_model=WebsiteThemeResponse, status_code=status.HTTP_201_CREATED)
async def createTheme(
    data: WebsiteThemeCreate,
    session: AsyncSession = Depends(getDb),
):
    """
    Registers a new website design theme template. Returns 201 Created.
    """
    service = WebsiteThemeService(session)
    return await service.createTheme(data)


@router.get("/{themeId}", response_model=WebsiteThemeResponse)
async def getTheme(
    themeId: uuid.UUID,
    session: AsyncSession = Depends(getDb),
):
    """
    Gets details of a single theme layout preset using database UUID.
    """
    service = WebsiteThemeService(session)
    return await service.getTheme(themeId)


@router.get("/", response_model=list[WebsiteThemeResponse])
async def listThemes(
    activeOnly: bool = Query(False),
    session: AsyncSession = Depends(getDb),
):
    """
    Lists themes. ActiveOnly flag option queries active visual templates.
    """
    service = WebsiteThemeService(session)
    return await service.listThemes(activeOnly=activeOnly)


@router.patch("/{themeId}", response_model=WebsiteThemeResponse)
async def updateTheme(
    themeId: uuid.UUID,
    data: WebsiteThemeUpdate,
    session: AsyncSession = Depends(getDb),
):
    """
    Updates details of a design theme configuration preset (like styling schema or fonts).
    """
    service = WebsiteThemeService(session)
    return await service.updateTheme(themeId, data)


@router.delete("/{themeId}", status_code=status.HTTP_204_NO_CONTENT)
async def deleteTheme(
    themeId: uuid.UUID,
    session: AsyncSession = Depends(getDb),
):
    """
    Deletes a website design theme template preset. Returns 204 No Content.
    """
    service = WebsiteThemeService(session)
    await service.deleteTheme(themeId)
