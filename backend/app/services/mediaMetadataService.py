# Owner: mousamdas156@gmail.com
# ================================================================================
# FILE: services/mediaMetadataService.py — Media Metadata Service
# ================================================================================
# Why this file is used:
#   - Manages accessibility descriptors and alt tags mapped to media files.
#
# What components are inside:
#   - MediaMetadataService:
#       - createMediaMetadata()        -> Registers metadata details.
#       - getMediaMetadata()           -> Resolves metadata values.
#       - getMediaMetadataByMediaFile()-> Returns metadata matching file IDs.
#       - listMediaMetadata()          -> Returns configured descriptors.
#       - updateMediaMetadata()        -> Modifies alt tags and dimensions.
#       - deleteMediaMetadata()        -> Removes descriptors.
# ================================================================================
"""
================================================================================
MEDIA METADATA SERVICE (mediaMetadataService.py)
================================================================================
Why this file is used:
- This file contains the business logic layer for managing `MediaMetadata` entities.
- It validates metadata uniqueness per parent file, updates description/alt attributes,
  and handles transactional commits.
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
from app.db.models.mediaMetadata import MediaMetadata
from app.repositories.mediaMetadataRepository import MediaMetadataRepository

# Pydantic schemas for data validation
from app.schemas.mediaMetadata import MediaMetadataCreate, MediaMetadataUpdate


class MediaMetadataService:
    """
    Service class orchestrating business processes for MediaMetadata.
    """
    def __init__(self, session: AsyncSession):
        """
        Initializes the service with a repository instance and database session.
        
        Args:
            session (AsyncSession): The database session.
        """
        self.repo = MediaMetadataRepository(session)
        self.session = session

    async def createMediaMetadata(self, data: MediaMetadataCreate) -> MediaMetadata:
        """
        Validates and creates a new MediaMetadata record.
        
        Args:
            data (MediaMetadataCreate): Input schema data.
            
        Returns:
            MediaMetadata: The created database model instance.
            
        Raises:
            ConflictError: If metadata already exists for the target file.
        """
        if await self.repo.getByMediaFile(data.mediaFileId):
            raise ConflictError(f"Metadata already exists for media file '{data.mediaFileId}'")

        metadata = MediaMetadata(**data.model_dump())
        result = await self.repo.create(metadata)
        await self.session.commit()
        return result

    async def getMediaMetadata(self, metadataId: uuid.UUID) -> MediaMetadata:
        """
        Retrieves a MediaMetadata record, throwing NotFoundError if missing.
        
        Args:
            metadataId (UUID): Unique ID of the metadata record.
            
        Returns:
            MediaMetadata: The found database model instance.
            
        Raises:
            NotFoundError: If the metadata record is not found.
        """
        metadata = await self.repo.getById(metadataId)
        if not metadata:
            raise NotFoundError("MediaMetadata", str(metadataId))
        return metadata

    async def getMediaMetadataByMediaFile(self, mediaFileId: uuid.UUID) -> MediaMetadata:
        """
        Retrieves a MediaMetadata record by its parent Media File ID.
        
        Args:
            mediaFileId (UUID): Unique ID of the parent media file.
            
        Returns:
            MediaMetadata: The found database model instance.
            
        Raises:
            NotFoundError: If the metadata record does not exist.
        """
        metadata = await self.repo.getByMediaFile(mediaFileId)
        if not metadata:
            raise NotFoundError("MediaMetadata for media file", str(mediaFileId))
        return metadata

    async def listMediaMetadata(self) -> Sequence[MediaMetadata]:
        """
        Lists all MediaMetadata records in the database.
        
        Returns:
            Sequence[MediaMetadata]: List of metadata records.
        """
        return await self.repo.getAll()

    async def updateMediaMetadata(self, metadataId: uuid.UUID, data: MediaMetadataUpdate) -> MediaMetadata:
        """
        Updates fields on an existing MediaMetadata record.
        
        Args:
            metadataId (UUID): Unique ID of the metadata record to update.
            data (MediaMetadataUpdate): Target update fields schema.
            
        Returns:
            MediaMetadata: The updated model instance.
            
        Raises:
            NotFoundError: If the metadata record does not exist.
        """
        metadata = await self.repo.getById(metadataId)
        if not metadata:
            raise NotFoundError("MediaMetadata", str(metadataId))

        updateData = data.model_dump(exclude_unset=True)
        result = await self.repo.update(metadata, updateData)
        await self.session.commit()
        return result

    async def deleteMediaMetadata(self, metadataId: uuid.UUID) -> None:
        """
        Deletes a MediaMetadata record.
        
        Args:
            metadataId (UUID): Unique ID of the metadata record to delete.
            
        Raises:
            NotFoundError: If the metadata record does not exist.
        """
        metadata = await self.repo.getById(metadataId)
        if not metadata:
            raise NotFoundError("MediaMetadata", str(metadataId))
        await self.repo.delete(metadata)
        await self.session.commit()