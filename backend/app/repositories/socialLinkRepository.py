# Owner: mousamdas156@gmail.com
"""
================================================================================
SOCIAL LINK DATABASE REPOSITORY
================================================================================
Yeh file social_links (Instagram/Facebook maps) table ke database operations handle karti hai.
This repository class manages database transactions and queries for store social links.

Why it is used:
- Keeps data operations for social mappings encapsulated and independent.
- Adheres to standard Repository architecture.
================================================================================
"""

import uuid
from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.socialLink import SocialLink


class SocialLinkRepository:
    """
    Manages CRUD operations and specific queries for the SocialLink entity.
    """

    def __init__(self, session: AsyncSession):
        """
        Initializes the repository with a database connection session.
        """
        self.session = session

    async def getById(self, socialLinkId: uuid.UUID) -> SocialLink | None:
        """
        Retrieves a social link mapping by its unique primary key ID.
        """
        result = await self.session.execute(
            select(SocialLink).where(SocialLink.id == socialLinkId)
        )
        return result.scalar_one_or_none()

    async def getByStoreAndPlatform(self, storeId: uuid.UUID, platformId: uuid.UUID) -> SocialLink | None:
        """
        Fetches the specific social link for a given store and platform.
        
        Why it is used:
        - Helps verify if a store already linked their account to this specific platform 
          (e.g., checking if Instagram is already registered).
        """
        result = await self.session.execute(
            select(SocialLink).where(
                SocialLink.storeId == storeId,
                SocialLink.platformId == platformId
            )
        )
        return result.scalar_one_or_none()

    async def getAll(self, storeId: uuid.UUID | None = None) -> Sequence[SocialLink]:
        """
        Retrieves all social links, sorted by creation date descending.
        Can optionally filter by storeId to get links belonging only to a specific store.
        """
        stmt = select(SocialLink).order_by(SocialLink.createdAt.desc())
        if storeId:
            stmt = stmt.where(SocialLink.storeId == storeId)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(self, socialLink: SocialLink) -> SocialLink:
        """
        Adds and flushes a new SocialLink entry into the database.
        """
        self.session.add(socialLink)
        await self.session.flush()
        await self.session.refresh(socialLink)
        return socialLink

    async def update(self, socialLink: SocialLink, data: dict) -> SocialLink:
        """
        Partially updates fields of an existing SocialLink mapping record.
        """
        for key, value in data.items():
            setattr(socialLink, key, value)
        await self.session.flush()
        await self.session.refresh(socialLink)
        return socialLink

    async def delete(self, socialLink: SocialLink) -> None:
        """
        Deletes a SocialLink record from the database.
        """
        await self.session.delete(socialLink)
        await self.session.flush()
