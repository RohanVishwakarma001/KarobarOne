# Owner: mousamdas156@gmail.com
"""
================================================================================
WEBSITE THEME DATABASE REPOSITORY
================================================================================
Yeh file website_themes table ke database transactions handle karti hai.
This repository class manages queries and writes for website design theme presets.

Why it is used:
- Provides backend database logic to fetch layout configurations for site generation.
================================================================================
"""

import uuid
from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.websiteTheme import WebsiteTheme


class WebsiteThemeRepository:
    """
    Handles CRUD operations and specific database queries for the WebsiteTheme entity.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def getById(self, themeId: uuid.UUID) -> WebsiteTheme | None:
        """
        Retrieves a WebsiteTheme by its primary key UUID.
        """
        result = await self.session.execute(
            select(WebsiteTheme).where(WebsiteTheme.id == themeId)
        )
        return result.scalar_one_or_none()

    async def getByCode(self, themeCode: str) -> WebsiteTheme | None:
        """
        Retrieves a WebsiteTheme using its unique short code string (e.g. 'NEON_GLOW').
        """
        result = await self.session.execute(
            select(WebsiteTheme).where(WebsiteTheme.themeCode == themeCode)
        )
        return result.scalar_one_or_none()

    async def getAll(self, activeOnly: bool = False) -> Sequence[WebsiteTheme]:
        """
        Retrieves all website themes sorted alphabetically by their name.
        If 'activeOnly' is set to True, returns only themes that are flagged active.
        """
        stmt = select(WebsiteTheme).order_by(WebsiteTheme.themeName.asc())
        if activeOnly:
            stmt = stmt.where(WebsiteTheme.isActive == True)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(self, theme: WebsiteTheme) -> WebsiteTheme:
        """
        Registers a new theme layout preset in the database.
        """
        self.session.add(theme)
        await self.session.flush()
        await self.session.refresh(theme)
        return theme

    async def update(self, theme: WebsiteTheme, data: dict) -> WebsiteTheme:
        """
        Performs a partial fields update of a WebsiteTheme layout preset.
        """
        for key, value in data.items():
            setattr(theme, key, value)
        await self.session.flush()
        await self.session.refresh(theme)
        return theme

    async def delete(self, theme: WebsiteTheme) -> None:
        """
        Deletes a WebsiteTheme template record from the database.
        """
        await self.session.delete(theme)
        await self.session.flush()
