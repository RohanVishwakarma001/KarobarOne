# Owner: mousamdas156@gmail.com
"""
================================================================================
SOCIAL PLATFORM DATABASE REPOSITORY
================================================================================
Yeh file social_platforms table ke database transactions handle karti hai.
This repository class manages master list operations for social media platforms.

Why it is used:
- Provides clean database abstraction for managing the platform catalogs.
================================================================================
"""

import uuid
from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.socialPlatform import SocialPlatform


class SocialPlatformRepository:
    """
    Handles CRUD operations and custom queries for the SocialPlatform entity.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def getById(self, platformId: uuid.UUID) -> SocialPlatform | None:
        """
        Retrieves a SocialPlatform by its primary key UUID.
        """
        result = await self.session.execute(
            select(SocialPlatform).where(SocialPlatform.id == platformId)
        )
        return result.scalar_one_or_none()

    async def getByCode(self, platformCode: str) -> SocialPlatform | None:
        """
        Finds a SocialPlatform using its unique string code (e.g. 'INSTAGRAM').
        
        Why it is used:
        - Used when creating/registering platforms or validating codes.
        """
        result = await self.session.execute(
            select(SocialPlatform).where(SocialPlatform.platformCode == platformCode)
        )
        return result.scalar_one_or_none()

    async def getAll(self, activeOnly: bool = False) -> Sequence[SocialPlatform]:
        """
        Retrieves all social platforms sorted alphabetically by name.
        If 'activeOnly' is True, filters to only retrieve platforms that are currently active.
        """
        stmt = select(SocialPlatform).order_by(SocialPlatform.platformName.asc())
        if activeOnly:
            stmt = stmt.where(SocialPlatform.isActive == True)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(self, platform: SocialPlatform) -> SocialPlatform:
        """
        Adds a new SocialPlatform record and flushes it to generate default attributes.
        """
        self.session.add(platform)
        await self.session.flush()
        await self.session.refresh(platform)
        return platform

    async def update(self, platform: SocialPlatform, data: dict) -> SocialPlatform:
        """
        Performs a partial update of a SocialPlatform entity.
        """
        for key, value in data.items():
            setattr(platform, key, value)
        await self.session.flush()
        await self.session.refresh(platform)
        return platform

    async def delete(self, platform: SocialPlatform) -> None:
        """
        Deletes a SocialPlatform master record from the database.
        """
        await self.session.delete(platform)
        await self.session.flush()
