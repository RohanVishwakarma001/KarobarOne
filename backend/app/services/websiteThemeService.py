# Owner: mousamdas156@gmail.com
# ================================================================================
# FILE: services/websiteThemeService.py — Website Theme Service
# ================================================================================
# Why this file is used:
#   - Manages color schemas and layout templates.
#
# What components are inside:
#   - WebsiteThemeService:
#       - createTheme()  -> Adds theme profiles, checking code uniqueness.
#       - getTheme()     -> Resolves theme profiles.
#       - listThemes()   -> Returns active theme configurations.
#       - updateTheme()  -> Modifies theme configs.
#       - deleteTheme()  -> Removes theme templates.
# ================================================================================
"""
================================================================================
WEBSITE THEME SERVICE
================================================================================
Yeh file website design themes ki settings aur updates manage karti hai.
This service layer module manages the templates / theme presets.

Why it is used:
- Validates the uniqueness of theme codes.
- Acts as the interface for creating and modifying active themes.
================================================================================
"""

import uuid
from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptionsCompat import ConflictError, NotFoundError
from app.db.models.websiteTheme import WebsiteTheme
from app.repositories.websiteThemeRepository import WebsiteThemeRepository
from app.schemas.websiteTheme import WebsiteThemeCreate, WebsiteThemeUpdate


class WebsiteThemeService:
    """
    Service class containing business rules for managing website design Themes.
    """

    def __init__(self, session: AsyncSession):
        self.repo = WebsiteThemeRepository(session)
        self.session = session

    async def createTheme(self, data: WebsiteThemeCreate) -> WebsiteTheme:
        """
        Creates a new design theme preset. Validates that the theme code 
        identifier (e.g. 'MINIMAL_DARK') is globally unique.
        """
        if await self.repo.getByCode(data.themeCode):
            raise ConflictError(f"Theme with code '{data.themeCode}' already exists")

        theme = WebsiteTheme(**data.model_dump())
        result = await self.repo.create(theme)
        await self.session.commit()
        return result

    async def getTheme(self, themeId: uuid.UUID) -> WebsiteTheme:
        """
        Retrieves a website theme preset by its unique ID.
        """
        theme = await self.repo.getById(themeId)
        if not theme:
            raise NotFoundError("WebsiteTheme", str(themeId))
        return theme

    async def listThemes(self, activeOnly: bool = False) -> Sequence[WebsiteTheme]:
        """
        Lists all website themes, with optional filtering to only active ones.
        """
        return await self.repo.getAll(activeOnly=activeOnly)

    async def updateTheme(self, themeId: uuid.UUID, data: WebsiteThemeUpdate) -> WebsiteTheme:
        """
        Updates an existing website theme configuration. Verifies themeCode 
        uniqueness if modified.
        """
        theme = await self.repo.getById(themeId)
        if not theme:
            raise NotFoundError("WebsiteTheme", str(themeId))

        updateData = data.model_dump(exclude_unset=True)
        # If modifying the unique themeCode, ensure it does not collision with another theme.
        if "themeCode" in updateData:
            existing = await self.repo.getByCode(updateData["themeCode"])
            if existing and existing.id != themeId:
                raise ConflictError(f"Theme with code '{updateData['themeCode']}' already exists")

        result = await self.repo.update(theme, updateData)
        await self.session.commit()
        return result

    async def deleteTheme(self, themeId: uuid.UUID) -> None:
        """
        Deletes a design theme preset.
        """
        theme = await self.repo.getById(themeId)
        if not theme:
            raise NotFoundError("WebsiteTheme", str(themeId))
        await self.repo.delete(theme)
        await self.session.commit()