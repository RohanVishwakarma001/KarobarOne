# Owner: mousamdas156@gmail.com
"""
================================================================================
MEDIA VARIANT DATABASE REPOSITORY (mediaVariantRepository.py)
================================================================================
Why this file is used:
- This file handles data access queries and operations for the `MediaVariant` entity.
- It abstracts the underlying SQLAlchemy database actions, providing query methods to fetch
  and write resized/scaled versions of assets.
================================================================================
"""

# Standard library imports for UUIDs and sequences
import uuid
from typing import Sequence

# Third-party database modules
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# Associated database ORM model
from app.db.models.mediaVariant import MediaVariant


class MediaVariantRepository:
    """
    Repository class encapsulating database operations for the MediaVariant model.
    """
    def __init__(self, session: AsyncSession):
        """
        Initializes the repository with an asynchronous database session.
        
        Args:
            session (AsyncSession): The database session.
        """
        self.session = session

    async def getById(self, variantId: uuid.UUID) -> MediaVariant | None:
        """
        Retrieves a MediaVariant record by its unique UUID.
        
        Args:
            variantId (UUID): Unique ID of the variant record.
            
        Returns:
            MediaVariant | None: The found variant record, or None.
        """
        result = await self.session.execute(
            select(MediaVariant).where(MediaVariant.id == variantId)
        )
        return result.scalar_one_or_none()

    async def getByMediaFileAndVariant(self, mediaFileId: uuid.UUID, variantName: str) -> MediaVariant | None:
        """
        Retrieves a MediaVariant record matching a specific name on a Media File ID.
        
        Args:
            mediaFileId (UUID): Unique ID of the parent media file.
            variantName (str): Name label of the variant (e.g. 'thumbnail').
            
        Returns:
            MediaVariant | None: The found variant record, or None.
        """
        result = await self.session.execute(
            select(MediaVariant).where(
                MediaVariant.mediaFileId == mediaFileId,
                MediaVariant.variantName == variantName
            )
        )
        return result.scalar_one_or_none()

    async def getAll(self, mediaFileId: uuid.UUID | None = None) -> Sequence[MediaVariant]:
        """
        Fetches all MediaVariant records, optionally filtered by parent media file ID.
        
        Args:
            mediaFileId (UUID | None): Optional parent media file ID filter.
            
        Returns:
            Sequence[MediaVariant]: List of variant records.
        """
        stmt = select(MediaVariant).order_by(MediaVariant.createdAt.desc())
        if mediaFileId:
            stmt = stmt.where(MediaVariant.mediaFileId == mediaFileId)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(self, variant: MediaVariant) -> MediaVariant:
        """
        Persists a new MediaVariant entity to the database session.
        
        Args:
            variant (MediaVariant): The unsaved variant model instance.
            
        Returns:
            MediaVariant: The persisted variant model with database-assigned attributes.
        """
        self.session.add(variant)
        await self.session.flush()
        await self.session.refresh(variant)
        return variant

    async def update(self, variant: MediaVariant, data: dict) -> MediaVariant:
        """
        Updates fields of an existing MediaVariant record dynamically.
        
        Args:
            variant (MediaVariant): The variant model instance to update.
            data (dict): Dictionary mapping attributes to update values.
            
        Returns:
            MediaVariant: The updated and refreshed model instance.
        """
        for key, value in data.items():
            setattr(variant, key, value)
        await self.session.flush()
        await self.session.refresh(variant)
        return variant

    async def delete(self, variant: MediaVariant) -> None:
        """
        Removes a MediaVariant record from the database.
        
        Args:
            variant (MediaVariant): The variant model instance to delete.
        """
        await self.session.delete(variant)
        await self.session.flush()
