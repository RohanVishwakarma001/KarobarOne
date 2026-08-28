# Owner: mousamdas156@gmail.com
# ================================================================================
# FILE: services/mediaFileService.py — Media File Service
# ================================================================================
# Why this file is used:
#   - Manages media asset configuration and checksum validation.
#
# What components are inside:
#   - MediaFileService:
#       - createMediaFile()  -> Registers uploads, verifying content checksums.
#       - getMediaFile()     -> Resolves uploads.
#       - listMediaFiles()   -> Returns file references.
#       - updateMediaFile()  -> Modifies file references.
#       - deleteMediaFile()  -> Removes file references.
# ================================================================================
"""
================================================================================
MEDIA FILE SERVICE (mediaFileService.py)
================================================================================
Why this file is used:
- This file contains the business logic layer for the `MediaFile` entity.
- It mediates between the controllers (routers) and the database repositories,
  applying validations, throwing domain errors (ConflictError, NotFoundError),
  and handling transactional commits.
================================================================================
"""

# Standard library imports for UUIDs and sequences
import uuid
from typing import Sequence

# Third-party database context
from sqlalchemy.ext.asyncio import AsyncSession

# Domain exceptions
from app.core.exceptionsCompat import ConflictError, NotFoundError

# Database ORM model and repository
from app.db.models.mediaFile import MediaFile
from app.repositories.mediaFileRepository import MediaFileRepository

# Pydantic schemas for data validation
from app.schemas.mediaFile import MediaFileCreate, MediaFileUpdate


class MediaFileService:
    """
    Service class orchestrating business processes for MediaFiles.
    """
    def __init__(self, session: AsyncSession):
        """
        Initializes the service with a repository instance and database session.
        
        Args:
            session (AsyncSession): The database session.
        """
        self.repo = MediaFileRepository(session)
        self.session = session

    async def createMediaFile(self, data: MediaFileCreate) -> MediaFile:
        """
        Validates and creates a new MediaFile record, checking for duplicate checksum.
        
        Args:
            data (MediaFileCreate): Input schema data.
            
        Returns:
            MediaFile: The created database model instance.
            
        Raises:
            ConflictError: If a file with the same checksum exists.
        """
        # Check duplicate checksum hash
        if await self.repo.getByChecksum(data.checksumHash):
            raise ConflictError(f"Media file with checksum hash '{data.checksumHash}' already exists")

        mediaFile = MediaFile(**data.model_dump())
        result = await self.repo.create(mediaFile)
        await self.session.commit()
        return result

    async def getMediaFile(self, mediaFileId: uuid.UUID) -> MediaFile:
        """
        Retrieves a MediaFile record, throwing NotFoundError if missing.
        
        Args:
            mediaFileId (UUID): Unique ID of the media file.
            
        Returns:
            MediaFile: The found database model instance.
            
        Raises:
            NotFoundError: If the media file is not found.
        """
        mediaFile = await self.repo.getById(mediaFileId)
        if not mediaFile:
            raise NotFoundError("MediaFile", str(mediaFileId))
        return mediaFile

    async def listMediaFiles(self, tenantId: uuid.UUID | None = None) -> Sequence[MediaFile]:
        """
        Lists media files in the database, optionally filtered by tenant.
        
        Args:
            tenantId (UUID | None): Optional tenant filter ID.
            
        Returns:
            Sequence[MediaFile]: List of media files.
        """
        return await self.repo.getAll(tenantId=tenantId)

    async def updateMediaFile(self, mediaFileId: uuid.UUID, data: MediaFileUpdate) -> MediaFile:
        """
        Validates and updates fields on an existing MediaFile.
        
        Args:
            mediaFileId (UUID): Unique ID of the media file to update.
            data (MediaFileUpdate): Target update fields schema.
            
        Returns:
            MediaFile: The updated model instance.
            
        Raises:
            NotFoundError: If the media file does not exist.
            ConflictError: If updating to an existing checksum hash of another file.
        """
        mediaFile = await self.repo.getById(mediaFileId)
        if not mediaFile:
            raise NotFoundError("MediaFile", str(mediaFileId))

        updateData = data.model_dump(exclude_unset=True)

        if "checksumHash" in updateData:
            existing = await self.repo.getByChecksum(updateData["checksumHash"])
            if existing and existing.id != mediaFileId:
                raise ConflictError(f"Media file with checksum hash '{updateData['checksumHash']}' already exists")

        result = await self.repo.update(mediaFile, updateData)
        await self.session.commit()
        return result

    async def deleteMediaFile(self, mediaFileId: uuid.UUID, soft: bool = True) -> None:
        """
        Deletes a MediaFile record (soft delete by default).
        
        Args:
            mediaFileId (UUID): Unique ID of the media file to delete.
            soft (bool): Flag indicating if delete is a soft delete. Defaults to True.
            
        Raises:
            NotFoundError: If the media file does not exist.
        """
        mediaFile = await self.repo.getById(mediaFileId)
        if not mediaFile:
            raise NotFoundError("MediaFile", str(mediaFileId))
        await self.repo.delete(mediaFile, soft=soft)
        await self.session.commit()