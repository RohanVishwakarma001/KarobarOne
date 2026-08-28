# Owner: mousamdas156@gmail.com
"""
================================================================================
MEDIA UPLOAD LOG DATABASE REPOSITORY (mediaUploadLogRepository.py)
================================================================================
Why this file is used:
- This file handles data access queries and operations for the `MediaUploadLog` entity.
- It abstracts the underlying SQLAlchemy database actions, providing query methods to fetch
  and write logs associated with file upload history and mutations.
================================================================================
"""

# Standard library imports for UUIDs and sequences
import uuid
from typing import Sequence

# Third-party database modules
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# Associated database ORM model
from app.db.models.mediaUploadLog import MediaUploadLog


class MediaUploadLogRepository:
    """
    Repository class encapsulating database operations for the MediaUploadLog model.
    """
    def __init__(self, session: AsyncSession):
        """
        Initializes the repository with an asynchronous database session.
        
        Args:
            session (AsyncSession): The database session.
        """
        self.session = session

    async def getById(self, logId: uuid.UUID) -> MediaUploadLog | None:
        """
        Retrieves a MediaUploadLog record by its unique UUID.
        
        Args:
            logId (UUID): Unique ID of the log record.
            
        Returns:
            MediaUploadLog | None: The found log record, or None.
        """
        result = await self.session.execute(
            select(MediaUploadLog).where(MediaUploadLog.id == logId)
        )
        return result.scalar_one_or_none()

    async def getAll(self, mediaFileId: uuid.UUID | None = None) -> Sequence[MediaUploadLog]:
        """
        Fetches all MediaUploadLog records, optionally filtered by media file ID.
        
        Args:
            mediaFileId (UUID | None): Optional media file ID filter.
            
        Returns:
            Sequence[MediaUploadLog]: List of log records.
        """
        stmt = select(MediaUploadLog).order_by(MediaUploadLog.createdAt.desc())
        if mediaFileId:
            stmt = stmt.where(MediaUploadLog.mediaFileId == mediaFileId)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(self, log: MediaUploadLog) -> MediaUploadLog:
        """
        Persists a new MediaUploadLog entity to the database session.
        
        Args:
            log (MediaUploadLog): The unsaved log model instance.
            
        Returns:
            MediaUploadLog: The persisted log model with database-assigned attributes.
        """
        self.session.add(log)
        await self.session.flush()
        await self.session.refresh(log)
        return log

    async def update(self, log: MediaUploadLog, data: dict) -> MediaUploadLog:
        """
        Updates fields of an existing MediaUploadLog record dynamically.
        
        Args:
            log (MediaUploadLog): The log model instance to update.
            data (dict): Dictionary mapping attributes to update values.
            
        Returns:
            MediaUploadLog: The updated and refreshed model instance.
        """
        for key, value in data.items():
            setattr(log, key, value)
        await self.session.flush()
        await self.session.refresh(log)
        return log

    async def delete(self, log: MediaUploadLog) -> None:
        """
        Removes a MediaUploadLog record from the database.
        
        Args:
            log (MediaUploadLog): The log model instance to delete.
        """
        await self.session.delete(log)
        await self.session.flush()
