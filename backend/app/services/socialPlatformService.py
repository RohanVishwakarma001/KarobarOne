# Owner: mousamdas156@gmail.com
# ================================================================================
# FILE: services/socialPlatformService.py — Social Platform Master Service
# ================================================================================
# Why this file is used:
#   - Manages master templates of supported platforms (e.g. YouTube, Instagram).
#
# What components are inside:
#   - SocialPlatformService:
#       - createPlatform()  -> Adds platforms, checking code uniqueness.
#       - getPlatform()     -> Resolves platforms.
#       - listPlatforms()   -> Returns active platforms.
#       - updatePlatform()  -> Modifies platform definitions.
#       - deletePlatform()  -> Removes platform definitions.
# ================================================================================
"""
================================================================================
SOCIAL PLATFORM SERVICE
================================================================================
Yeh file social platforms master table ke business rules validate karti hai.
This service layer module manages the supported social platform options.

Why it is used:
- Prevents creation of duplicate platform configurations (e.g. creating two Instagram platforms).
- Manages transactional commits.
================================================================================
"""

import uuid
from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptionsCompat import ConflictError, NotFoundError
from app.db.models.socialPlatform import SocialPlatform
from app.repositories.socialPlatformRepository import SocialPlatformRepository
from app.schemas.socialPlatform import SocialPlatformCreate, SocialPlatformUpdate


class SocialPlatformService:
    """
    Service class containing business rules for managing master Social Platforms.
    """

    def __init__(self, session: AsyncSession):
        self.repo = SocialPlatformRepository(session)
        self.session = session

    async def createPlatform(self, data: SocialPlatformCreate) -> SocialPlatform:
        """
        Registers a new social media platform after validating that the 
        platform code string is unique globally.
        """
        # Ensure that no platform already exists with this code (e.g., 'INSTAGRAM')
        if await self.repo.getByCode(data.platformCode):
            raise ConflictError(f"Social platform with code '{data.platformCode}' already exists")

        platform = SocialPlatform(**data.model_dump())
        result = await self.repo.create(platform)
        await self.session.commit()
        return result

    async def getPlatform(self, platformId: uuid.UUID) -> SocialPlatform:
        """
        Retrieves a SocialPlatform by its ID.
        """
        platform = await self.repo.getById(platformId)
        if not platform:
            raise NotFoundError("SocialPlatform", str(platformId))
        return platform

    async def listPlatforms(self, activeOnly: bool = False) -> Sequence[SocialPlatform]:
        """
        Lists all social platforms, with optional filtering to only active ones.
        """
        return await self.repo.getAll(activeOnly=activeOnly)

    async def updatePlatform(self, platformId: uuid.UUID, data: SocialPlatformUpdate) -> SocialPlatform:
        """
        Updates an existing social platform's details, checking code uniqueness if modified.
        """
        platform = await self.repo.getById(platformId)
        if not platform:
            raise NotFoundError("SocialPlatform", str(platformId))

        updateData = data.model_dump(exclude_unset=True)
        # If the platformCode is changing, check that the new code is not taken by another master record.
        if "platformCode" in updateData:
            existing = await self.repo.getByCode(updateData["platformCode"])
            if existing and existing.id != platformId:
                raise ConflictError(f"Social platform with code '{updateData['platformCode']}' already exists")

        result = await self.repo.update(platform, updateData)
        await self.session.commit()
        return result

    async def deletePlatform(self, platformId: uuid.UUID) -> None:
        """
        Deletes a master platform, cascading the deletion to all linked store social mappings.
        """
        platform = await self.repo.getById(platformId)
        if not platform:
            raise NotFoundError("SocialPlatform", str(platformId))
        await self.repo.delete(platform)
        await self.session.commit()