# Owner: mousamdas156@gmail.com
"""
================================================================================
MEDIA FILE DATABASE REPOSITORY (mediaFileRepository.py)
================================================================================
Why this file is used:
- This file handles data access queries and operations for the `MediaFile` entity.
- It abstracts the underlying SQLAlchemy database actions, providing clean async CRUD
  operations including soft and hard deletes.
================================================================================
"""

# Standard library imports for UUIDs, sequences, and datetime
import uuid
from datetime import datetime
from typing import Sequence

# Third-party database modules
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# Associated database ORM model
from app.db.models.mediaFile import MediaFile


class MediaFileRepository:
    """
    Repository class encapsulating database operations for the MediaFile model.
    """
    def __init__(self, session: AsyncSession):
        """
        Initializes the repository with an asynchronous database session.
        
        Args:
            session (AsyncSession): The database session.
        """
        self.session = session

    async def getById(self, mediaFileId: uuid.UUID, includeDeleted: bool = False) -> MediaFile | None:
        """
        Retrieves a MediaFile record by its unique UUID.
        
        Args:
            mediaFileId (UUID): Unique ID of the media file.
            includeDeleted (bool): If True, returns soft-deleted files. Default is False.
            
        Returns:
            MediaFile | None: The found media file, or None.
        """
        stmt = select(MediaFile).where(MediaFile.id == mediaFileId)
        if not includeDeleted:
            stmt = stmt.where(MediaFile.deletedAt.is_(None))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def getByChecksum(self, checksumHash: str, includeDeleted: bool = False) -> MediaFile | None:
        """
        Retrieves a MediaFile record by its checksum hash to prevent duplicates.
        
        Args:
            checksumHash (str): The calculated file checksum hash.
            includeDeleted (bool): If True, returns soft-deleted files. Default is False.
            
        Returns:
            MediaFile | None: The found media file, or None.
        """
        stmt = select(MediaFile).where(MediaFile.checksumHash == checksumHash)
        if not includeDeleted:
            stmt = stmt.where(MediaFile.deletedAt.is_(None))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def getAll(self, tenantId: uuid.UUID | None = None, includeDeleted: bool = False) -> Sequence[MediaFile]:
        """
        Fetches all MediaFile records, optionally filtered by tenant ID.
        
        Args:
            tenantId (UUID | None): Optional tenant ID filter.
            includeDeleted (bool): If True, returns soft-deleted files. Default is False.
            
        Returns:
            Sequence[MediaFile]: List of media files.
        """
        stmt = select(MediaFile).order_by(MediaFile.createdAt.desc())
        if not includeDeleted:
            stmt = stmt.where(MediaFile.deletedAt.is_(None))
        if tenantId:
            stmt = stmt.where(MediaFile.tenantId == tenantId)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(self, mediaFile: MediaFile) -> MediaFile:
        """
        Persists a new MediaFile entity to the database session.
        
        Args:
            mediaFile (MediaFile): The unsaved model instance.
            
        Returns:
            MediaFile: The persisted model with generated ID and default attributes.
        """
        self.session.add(mediaFile)
        await self.session.flush()
        await self.session.refresh(mediaFile)
        return mediaFile

    async def update(self, mediaFile: MediaFile, data: dict) -> MediaFile:
        """
        Updates fields of an existing MediaFile record dynamically.
        
        Args:
            mediaFile (MediaFile): The model instance to update.
            data (dict): Dictionary mapping attributes to update values.
            
        Returns:
            MediaFile: The updated and refreshed model instance.
        """
        for key, value in data.items():
            setattr(mediaFile, key, value)
        await self.session.flush()
        await self.session.refresh(mediaFile)
        return mediaFile

    async def delete(self, mediaFile: MediaFile, soft: bool = True) -> None:
        """
        Removes a MediaFile record, supporting soft deletion or hard removal.
        
        Args:
            mediaFile (MediaFile): The model instance to delete.
            soft (bool): If True, sets deletedAt instead of removing the row. Default is True.
        """
        if soft:
            mediaFile.deletedAt = datetime.now()
            self.session.add(mediaFile)
        else:
            await self.session.delete(mediaFile)
        await self.session.flush()
