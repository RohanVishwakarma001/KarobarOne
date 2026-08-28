# Owner: mousamdas156@gmail.com
"""
================================================================================
MEDIA METADATA DATABASE REPOSITORY (mediaMetadataRepository.py)
================================================================================
Why this file is used:
- This file handles data access queries and operations for the `MediaMetadata` entity.
- It abstracts the underlying SQLAlchemy database actions, providing queries to fetch
  and write ALT text, captions, and slugs linked to media files.
================================================================================
"""

# Standard library imports for UUIDs and sequences
import uuid
from typing import Sequence

# Third-party database modules
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# Associated database ORM model
from app.db.models.mediaMetadata import MediaMetadata


class MediaMetadataRepository:
    """
    Repository class encapsulating database operations for the MediaMetadata model.
    """
    def __init__(self, session: AsyncSession):
        """
        Initializes the repository with an asynchronous database session.
        
        Args:
            session (AsyncSession): The database session.
        """
        self.session = session

    async def getById(self, metadataId: uuid.UUID) -> MediaMetadata | None:
        """
        Retrieves a MediaMetadata record by its unique UUID.
        
        Args:
            metadataId (UUID): Unique ID of the metadata record.
            
        Returns:
            MediaMetadata | None: The found metadata record, or None.
        """
        result = await self.session.execute(
            select(MediaMetadata).where(MediaMetadata.id == metadataId)
        )
        return result.scalar_one_or_none()

    async def getByMediaFile(self, mediaFileId: uuid.UUID) -> MediaMetadata | None:
        """
        Retrieves a MediaMetadata record by its associated Media File ID.
        
        Args:
            mediaFileId (UUID): Unique ID of the parent media file.
            
        Returns:
            MediaMetadata | None: The found metadata record, or None.
        """
        result = await self.session.execute(
            select(MediaMetadata).where(MediaMetadata.mediaFileId == mediaFileId)
        )
        return result.scalar_one_or_none()

    async def getAll(self) -> Sequence[MediaMetadata]:
        """
        Fetches all MediaMetadata records ordered by creation date.
        
        Returns:
            Sequence[MediaMetadata]: List of metadata records.
        """
        result = await self.session.execute(
            select(MediaMetadata).order_by(MediaMetadata.createdAt.desc())
        )
        return result.scalars().all()

    async def create(self, metadata: MediaMetadata) -> MediaMetadata:
        """
        Persists a new MediaMetadata entity in the database session.
        
        Args:
            metadata (MediaMetadata): The unsaved model instance.
            
        Returns:
            MediaMetadata: The persisted model with generated ID and attributes.
        """
        self.session.add(metadata)
        await self.session.flush()
        await self.session.refresh(metadata)
        return metadata

    async def update(self, metadata: MediaMetadata, data: dict) -> MediaMetadata:
        """
        Updates fields of an existing MediaMetadata record dynamically.
        
        Args:
            metadata (MediaMetadata): The model instance to update.
            data (dict): Dictionary mapping attributes to update values.
            
        Returns:
            MediaMetadata: The updated and refreshed model instance.
        """
        for key, value in data.items():
            setattr(metadata, key, value)
        await self.session.flush()
        await self.session.refresh(metadata)
        return metadata

    async def delete(self, metadata: MediaMetadata) -> None:
        """
        Removes a MediaMetadata record from the database.
        
        Args:
            metadata (MediaMetadata): The model instance to delete.
        """
        await self.session.delete(metadata)
        await self.session.flush()
