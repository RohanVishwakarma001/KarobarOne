# Owner: mousamdas156@gmail.com
# ================================================================================
# FILE: repositories/entityVersionRepository.py — Repository for Entity Versions
# ================================================================================
# Why this file is used:
#   - Encapsulates database queries for entity snapshots and version control.
#   - Isolates version tracking business rules (like published vs unpublished flags)
#     from the services layer.
#
# What components are inside:
#   - EntityVersionRepository:
#       - getLatestVersionNumber() -> Retrieve highest version number for entity
#       - getPublishedVersion()    -> Fetch currently active published snapshot
#       - getDraftByEntity()       -> Fetch latest unpublished draft snapshot
#       - unpublishAllForEntity()  -> Reset isPublished flags before new publish
# ================================================================================
"""
Repository layer for EntityVersion queries and version control.
"""

# Import standard uuid class for validating unique database identifiers
import uuid
# Import select query builder, update utility, and max/coalesce functions from SQLAlchemy
from sqlalchemy import select, update, func
# Import async session for transaction context control
from sqlalchemy.ext.asyncio import AsyncSession

# Import generic BaseRepository class containing base CRUD operations
from app.repositories.base import BaseRepository
# Import database model definition for EntityVersion
from app.db.models.approvals import EntityVersion


class EntityVersionRepository(BaseRepository[EntityVersion]):
    """
    Data-access repository for managing EntityVersion queries and version snapshot sequences.
    """

    def __init__(self, model: type[EntityVersion], session: AsyncSession):
        """
        What it does:
            Initializes the repository with the model class and active db session.
        Why it is used:
            Binds the repository to the database context for execution.
        """
        super().__init__(model, session)

    async def getLatestVersionNumber(self, entityType: str, entityId: uuid.UUID) -> int:
        """
        What it does:
            Queries the maximum versionNumber value from the EntityVersion table
            matching the specific entity type and ID. Returns 0 if no version exists.
        Why it is used:
            Determines the next sequential version number when saving drafts or
            submitting new change requests, avoiding manually querying version histories.
        """
        # Build query using func.max and func.coalesce for fallback
        stmt = (
            select(func.coalesce(func.max(self.model.versionNumber), 0))
            .where(self.model.entityType == entityType)
            .where(self.model.entityId == entityId)
        )
        # Execute query against active async session
        result = await self.session.execute(stmt)
        return result.scalar() or 0

    async def getPublishedVersion(self, entityType: str, entityId: uuid.UUID) -> EntityVersion | None:
        """
        What it does:
            Queries the database to fetch the EntityVersion snapshot marked with
            isPublished=True for the specified entityType and entityId.
        Why it is used:
            Required during workflow validations and audit log generation to retrieve
            the currently active, live state of a record.
        """
        # Query matching entity fields and published filter
        stmt = (
            select(self.model)
            .where(self.model.entityType == entityType)
            .where(self.model.entityId == entityId)
            .where(self.model.isPublished == True)
        )
        # Execute query against active async session
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def getDraftByEntity(self, entityType: str, entityId: uuid.UUID) -> EntityVersion | None:
        """
        What it does:
            Queries the EntityVersion table to fetch the latest unpublished version
            (isPublished=False) for the specified entity.
        Why it is used:
            Used in draft management to retrieve or modify pending modifications
            that have not been committed or approved yet.
        """
        # Order by version number descending to get the latest draft state
        stmt = (
            select(self.model)
            .where(self.model.entityType == entityType)
            .where(self.model.entityId == entityId)
            .where(self.model.isPublished == False)
            .order_by(self.model.versionNumber.desc())
            .limit(1)
        )
        # Execute query against active async session
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def unpublishAllForEntity(self, entityType: str, entityId: uuid.UUID) -> None:
        """
        What it does:
            Executes a bulk update statement in the database setting isPublished=False
            for all versions of a specific entity.
        Why it is used:
            Used right before a new version is approved/published. Clears previous active
            published flags to ensure only one version snapshot is marked active at any time.
        """
        # Build bulk update statement resetting published flag
        stmt = (
            update(self.model)
            .where(self.model.entityType == entityType)
            .where(self.model.entityId == entityId)
            .values(isPublished=False)
        )
        # Execute update query and flush changes
        await self.session.execute(stmt)
        await self.session.flush()
