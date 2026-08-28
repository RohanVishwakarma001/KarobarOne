# Owner: mousamdas156@gmail.com
# ================================================================================
# FILE: services/mediaUploadLogService.py — Media Upload Audit Log Service
# ================================================================================
# Why this file is used:
#   - Logs transaction logs and status markers for upload processes.
#
# What components are inside:
#   - MediaUploadLogService:
#       - createMediaUploadLog()  -> Logs uploads.
#       - getMediaUploadLog()     -> Resolves session metrics.
#       - listMediaUploadLogs()   -> Returns upload events.
#       - updateMediaUploadLog()  -> Modifies status values.
#       - deleteMediaUploadLog()  -> Removes session audit logs.
# ================================================================================
"""
================================================================================
MEDIA UPLOAD LOG SERVICE (mediaUploadLogService.py)
================================================================================
Why this file is used:
- This file contains the business logic layer for audit logs (`MediaUploadLog`).
- It processes logging operations during file upload sessions, history tracking, 
  and handles transactional commits.
================================================================================
"""

# Standard library imports for UUIDs and sequences
import uuid
from typing import Sequence

# Third-party database context
from sqlalchemy.ext.asyncio import AsyncSession

# Domain exceptions
from app.core.exceptionsCompat import NotFoundError

# Database ORM model and repository
from app.db.models.mediaUploadLog import MediaUploadLog
from app.repositories.mediaUploadLogRepository import MediaUploadLogRepository

# Pydantic schemas for data validation
from app.schemas.mediaUploadLog import MediaUploadLogCreate, MediaUploadLogUpdate


class MediaUploadLogService:
    """
    Service class orchestrating business processes for MediaUploadLogs.
    """
    def __init__(self, session: AsyncSession):
        """
        Initializes the service with a repository instance and database session.
        
        Args:
            session (AsyncSession): The database session.
        """
        self.repo = MediaUploadLogRepository(session)
        self.session = session

    async def createMediaUploadLog(self, data: MediaUploadLogCreate) -> MediaUploadLog:
        """
        Creates a new MediaUploadLog entry.
        
        Args:
            data (MediaUploadLogCreate): Input schema data.
            
        Returns:
            MediaUploadLog: The created database model instance.
        """
        log = MediaUploadLog(**data.model_dump())
        result = await self.repo.create(log)
        await self.session.commit()
        return result

    async def getMediaUploadLog(self, logId: uuid.UUID) -> MediaUploadLog:
        """
        Retrieves a MediaUploadLog record, throwing NotFoundError if missing.
        
        Args:
            logId (UUID): Unique ID of the log record.
            
        Returns:
            MediaUploadLog: The found database model instance.
            
        Raises:
            NotFoundError: If the log record is not found.
        """
        log = await self.repo.getById(logId)
        if not log:
            raise NotFoundError("MediaUploadLog", str(logId))
        return log

    async def listMediaUploadLogs(self, mediaFileId: uuid.UUID | None = None) -> Sequence[MediaUploadLog]:
        """
        Lists upload logs, optionally filtered by media file.
        
        Args:
            mediaFileId (UUID | None): Optional media file filter ID.
            
        Returns:
            Sequence[MediaUploadLog]: List of upload logs.
        """
        return await self.repo.getAll(mediaFileId=mediaFileId)

    async def updateMediaUploadLog(self, logId: uuid.UUID, data: MediaUploadLogUpdate) -> MediaUploadLog:
        """
        Updates fields on an existing MediaUploadLog record.
        
        Args:
            logId (UUID): Unique ID of the log record to update.
            data (MediaUploadLogUpdate): Target update fields schema.
            
        Returns:
            MediaUploadLog: The updated model instance.
            
        Raises:
            NotFoundError: If the log record does not exist.
        """
        log = await self.repo.getById(logId)
        if not log:
            raise NotFoundError("MediaUploadLog", str(logId))

        updateData = data.model_dump(exclude_unset=True)
        result = await self.repo.update(log, updateData)
        await self.session.commit()
        return result

    async def deleteMediaUploadLog(self, logId: uuid.UUID) -> None:
        """
        Deletes a MediaUploadLog record.
        
        Args:
            logId (UUID): Unique ID of the log record to delete.
            
        Raises:
            NotFoundError: If the log record does not exist.
        """
        log = await self.repo.getById(logId)
        if not log:
            raise NotFoundError("MediaUploadLog", str(logId))
        await self.repo.delete(log)
        await self.session.commit()