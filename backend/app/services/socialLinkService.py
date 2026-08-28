# Owner: mousamdas156@gmail.com
# ================================================================================
# FILE: services/socialLinkService.py — Store Social Link Service
# ================================================================================
# Why this file is used:
#   - Manages media links mapped to storefront entries.
#
# What components are inside:
#   - SocialLinkService:
#       - createSocialLink()  -> Maps link handles, verifying duplicate platform records.
#       - getSocialLink()     -> Resolves link parameters.
#       - listSocialLinks()   -> Returns link handles.
#       - updateSocialLink()  -> Modifies link parameters.
#       - deleteSocialLink()  -> Removes link parameters.
# ================================================================================
"""
================================================================================
SOCIAL LINK SERVICE
================================================================================
Yeh file social links map karne aur profile handles validate karne ka kaam karti hai.
This service layer module manages the business rules validation for assigning 
social platforms (like Instagram, Facebook) to stores.

Why it is used:
- Enforces the business logic rule that a store can only map one handle per social platform.
- Orchestrates transactional saves/deletes.
================================================================================
"""

import uuid
from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptionsCompat import ConflictError, NotFoundError
from app.db.models.socialLink import SocialLink
from app.repositories.socialLinkRepository import SocialLinkRepository
from app.schemas.socialLink import SocialLinkCreate, SocialLinkUpdate


class SocialLinkService:
    """
    Service class containing business rules for managing Store Social Links.
    """

    def __init__(self, session: AsyncSession):
        self.repo = SocialLinkRepository(session)
        self.session = session

    async def createSocialLink(self, data: SocialLinkCreate) -> SocialLink:
        """
        Creates a new SocialLink after verifying that the store hasn't already 
        linked their profile to the target social platform.
        """
        # Ensure that the store doesn't already have a social link map for this platform
        if await self.repo.getByStoreAndPlatform(data.storeId, data.platformId):
            raise ConflictError("A link for this platform already exists for this store")

        socialLink = SocialLink(**data.model_dump())
        result = await self.repo.create(socialLink)
        await self.session.commit()
        return result

    async def getSocialLink(self, socialLinkId: uuid.UUID) -> SocialLink:
        """
        Retrieves a social link mapping by its unique ID.
        """
        link = await self.repo.getById(socialLinkId)
        if not link:
            raise NotFoundError("SocialLink", str(socialLinkId))
        return link

    async def listSocialLinks(self, storeId: uuid.UUID | None = None) -> Sequence[SocialLink]:
        """
        Lists all social links mapped, optionally filtered to a specific store.
        """
        return await self.repo.getAll(storeId=storeId)

    async def updateSocialLink(self, socialLinkId: uuid.UUID, data: SocialLinkUpdate) -> SocialLink:
        """
        Updates an existing social link details. Checks unique platform validation 
        if changing the platform ID.
        """
        link = await self.repo.getById(socialLinkId)
        if not link:
            raise NotFoundError("SocialLink", str(socialLinkId))

        updateData = data.model_dump(exclude_unset=True)
        # If the platform itself is changing, ensure the store doesn't already have another mapping for that platform.
        if "platformId" in updateData:
            existing = await self.repo.getByStoreAndPlatform(link.storeId, updateData["platformId"])
            if existing and existing.id != socialLinkId:
                raise ConflictError("A link for this platform already exists for this store")

        result = await self.repo.update(link, updateData)
        await self.session.commit()
        return result

    async def deleteSocialLink(self, socialLinkId: uuid.UUID) -> None:
        """
        Removes a social link mapping.
        """
        link = await self.repo.getById(socialLinkId)
        if not link:
            raise NotFoundError("SocialLink", str(socialLinkId))
        await self.repo.delete(link)
        await self.session.commit()