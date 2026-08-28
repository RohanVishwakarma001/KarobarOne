# Owner: mousamdas156@gmail.com
"""
================================================================================
SECTION DATABASE REPOSITORY
================================================================================
Yeh file sections table ke liye database queries (CRUD) handles karti hai.
This repository class decouples database access from business logic, centralizing 
all Section-related SQL operations.

Why it is used:
- Separates database concerns from services, allowing queries to be easily mockable or optimized.
- Adheres to the Repository Pattern for cleaner architecture.
================================================================================
"""

import uuid
from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.section import Section


class SectionRepository:
    """
    Handles standard CRUD and custom database query operations for the Section model.
    """

    def __init__(self, session: AsyncSession):
        """
        Initializes the repository with an active database session.
        """
        self.session = session

    async def getById(self, sectionId: uuid.UUID) -> Section | None:
        """
        Retrieves a specific Section by its unique UUID.
        
        Why it is used:
        - Used when editing, deleting, or fetching details of a single section block.
        """
        result = await self.session.execute(
            select(Section).where(Section.id == sectionId)
        )
        return result.scalar_one_or_none()

    async def getByCode(self, storeId: uuid.UUID, sectionCode: str) -> Section | None:
        """
        Retrieves a Section for a specific store using its semantic identifier (sectionCode).
        
        Why it is used:
        - Used to check duplicate section codes before adding a new section.
        """
        result = await self.session.execute(
            select(Section).where(
                Section.storeId == storeId,
                Section.sectionCode == sectionCode
            )
        )
        return result.scalar_one_or_none()

    async def getBySortOrder(self, storeId: uuid.UUID, sortOrder: int) -> Section | None:
        """
        Retrieves a Section in a store with a specific display sequence number.
        
        Why it is used:
        - Verifies that two sections do not conflict on visual sorting order during creation or updates.
        """
        result = await self.session.execute(
            select(Section).where(
                Section.storeId == storeId,
                Section.sortOrder == sortOrder
            )
        )
        return result.scalar_one_or_none()

    async def getAll(self, storeId: uuid.UUID) -> Sequence[Section]:
        """
        Fetches all sections for a given storeId, ordered by sortOrder ascending (lower numbers show first).
        
        Why it is used:
        - Renders the storefront page blocks in their correct sequence on the frontend for a specific store tenant.
        """
        stmt = select(Section).where(Section.storeId == storeId).order_by(Section.sortOrder.asc())
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(self, section: Section) -> Section:
        """
        Persists a new Section record to the database.
        
        What it does:
        - Adds the section object to the session.
        - Calls 'flush()' to execute SQL statement in the transaction, generating UUID / defaults.
        - Refreshes the instance to populate DB-generated values (like createdAt, default active flags).
        """
        self.session.add(section)
        await self.session.flush()
        await self.session.refresh(section)
        return section

    async def update(self, section: Section, data: dict) -> Section:
        """
        Updates fields of an existing Section model using incoming dictionary data.
        
        Why it is used:
        - Allows flexible partial updates of section data (e.g. toggling isActive, or editing configData).
        """
        for key, value in data.items():
            setattr(section, key, value)
        await self.session.flush()
        await self.session.refresh(section)
        return section

    async def delete(self, section: Section) -> None:
        """
        Removes a Section record from the database.
        Changes are flushed immediately to update database state in the current transaction.
        """
        await self.session.delete(section)
        await self.session.flush()
