# Owner: mousamdas156@gmail.com
# ================================================================================
# FILE: services/sectionService.py — Website Section Service
# ================================================================================
# Why this file is used:
#   - Manages webpage custom block configurations.
#
# What components are inside:
#   - SectionService:
#       - createSection()  -> Adds page sections, checking sort indices.
#       - getSection()     -> Resolves webpage blocks.
#       - listSections()   -> Returns webpage blocks.
#       - updateSection()  -> Modifies section parameters.
#       - deleteSection()  -> Removes section blocks.
# ================================================================================
"""
================================================================================
SECTION SERVICE
================================================================================
Yeh file sections ke business rules validation aur database transactions manage karti hai.
This service layer module implements all business logic validation rules for 
website sections, such as verifying uniqueness constraints before writing to DB.

Why it is used:
- Coordinates repository calls and ensures database commits/rollbacks are done cleanly.
- Implements validations that cannot easily be checked at the DB constraint level.
================================================================================
"""

import uuid
from typing import Sequence
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptionsCompat import ConflictError, NotFoundError
from app.db.models.section import Section
from app.repositories.sectionRepository import SectionRepository
from app.schemas.section import SectionCreate, SectionUpdate


class SectionService:
    """
    Service class containing business rules for managing page Sections.
    """

    def __init__(self, session: AsyncSession):
        """
        Initializes the service with the database session and constructs the repository helper.
        """
        self.repo = SectionRepository(session)
        self.session = session

    async def createSection(self, data: SectionCreate) -> Section:
        """
        Creates a new page Section after validating that:
        1. The section code is unique for this store.
        2. The display sort order is unique for this store.
        
        Commits the transaction to save changes to PostgreSQL.
        """
        # Validate that the store doesn't already have a section with this code
        if await self.repo.getByCode(data.storeId, data.sectionCode):
            raise ConflictError(
                f"Section with code '{data.sectionCode}' already exists for this store"
            )

        # Validate that the sort sequence number isn't already taken by another block in this store
        if await self.repo.getBySortOrder(data.storeId, data.sortOrder):
            raise ConflictError(
                f"Section with sort order '{data.sortOrder}' already exists for this store"
            )

        # Instantiate ORM model from the schema payload and persist it
        section = Section(**data.model_dump())
        result = await self.repo.create(section)
        # Commit the transaction permanently to PostgreSQL
        await self.session.commit()
        return result

    async def getSection(self, sectionId: uuid.UUID) -> Section:
        """
        Retrieves a section by ID, raising NotFoundError if it does not exist.
        """
        section = await self.repo.getById(sectionId)
        if not section:
            raise NotFoundError("Section", str(sectionId))
        return section

    async def listSections(self, storeId: uuid.UUID) -> Sequence[Section]:
        """
        Retrieves a list of sections filtered by storeId.
        """
        return await self.repo.getAll(storeId=storeId)

    async def updateSection(self, sectionId: uuid.UUID, data: SectionUpdate) -> Section:
        """
        Updates an existing Section. Verifies code and sortOrder uniqueness rules if 
        they are changed in the update payload.
        """
        # Ensure the section actually exists first
        section = await self.repo.getById(sectionId)
        if not section:
            raise NotFoundError("Section", str(sectionId))

        updateData = data.model_dump(exclude_unset=True)
        
        # If the code is changing, check that the new code does not conflict with another section
        if "sectionCode" in updateData:
            existing = await self.repo.getByCode(section.storeId, updateData["sectionCode"])
            if existing and existing.id != sectionId:
                raise ConflictError(
                    f"Section with code '{updateData['sectionCode']}' already exists for this store"
                )

        # If the display sequence order is changing, check that the new position is free
        if "sortOrder" in updateData:
            existing = await self.repo.getBySortOrder(section.storeId, updateData["sortOrder"])
            if existing and existing.id != sectionId:
                raise ConflictError(
                    f"Section with sort order '{updateData['sortOrder']}' already exists for this store"
                )

        result = await self.repo.update(section, updateData)
        await self.session.commit()
        return result

    async def deleteSection(self, sectionId: uuid.UUID) -> None:
        """
        Removes a page section block from the store website.
        """
        section = await self.repo.getById(sectionId)
        if not section:
            raise NotFoundError("Section", str(sectionId))
        await self.repo.delete(section)
        await self.session.commit()