# Owner: mousamdas156@gmail.com
# ================================================================================
# FILE: services/mediaVariantService.py — Media Variant Service
# ================================================================================
# Why this file is used:
#   - Manages cropped images or thumbnail variant files.
#
# What components are inside:
#   - MediaVariantService:
#       - createMediaVariant()  -> Maps variants, verifying duplicate variant names.
#       - getMediaVariant()     -> Resolves variant entities.
#       - listMediaVariants()   -> Returns variant mappings.
#       - updateMediaVariant()  -> Modifies properties.
#       - deleteMediaVariant()  -> Removes crop settings.
# ================================================================================
"""
================================================================================
MEDIA VARIANT SERVICE (mediaVariantService.py)
================================================================================
Why this file is used:
- This file contains the business logic layer for the `MediaVariant` entity.
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
from app.db.models.mediaVariant import MediaVariant
from app.repositories.mediaVariantRepository import MediaVariantRepository

# Pydantic schemas for data validation
from app.schemas.mediaVariant import MediaVariantCreate, MediaVariantUpdate


class MediaVariantService:
    """
    Service class orchestrating business processes for MediaVariants.
    """
    def __init__(self, session: AsyncSession):
        """
        Initializes the service with a repository instance and database session.
        
        Args:
            session (AsyncSession): The database session.
        """
        self.repo = MediaVariantRepository(session)
        self.session = session

    async def createMediaVariant(self, data: MediaVariantCreate) -> MediaVariant:
        """
        Validates and creates a new MediaVariant record linked to a parent MediaFile.
        
        Args:
            data (MediaVariantCreate): Input schema data.
            
        Returns:
            MediaVariant: The created database model instance.
            
        Raises:
            ConflictError: If a variant with that name already exists for the parent file.
        """
        if await self.repo.getByMediaFileAndVariant(data.mediaFileId, data.variantName):
            raise ConflictError(f"Variant '{data.variantName}' already exists for media file '{data.mediaFileId}'")

        variant = MediaVariant(**data.model_dump())
        result = await self.repo.create(variant)
        await self.session.commit()
        return result

    async def getMediaVariant(self, variantId: uuid.UUID) -> MediaVariant:
        """
        Retrieves a MediaVariant record, throwing NotFoundError if missing.
        
        Args:
            variantId (UUID): Unique ID of the variant record.
            
        Returns:
            MediaVariant: The found database model instance.
            
        Raises:
            NotFoundError: If the variant is not found.
        """
        variant = await self.repo.getById(variantId)
        if not variant:
            raise NotFoundError("MediaVariant", str(variantId))
        return variant

    async def listMediaVariants(self, mediaFileId: uuid.UUID | None = None) -> Sequence[MediaVariant]:
        """
        Lists media variants, optionally filtered by parent media file.
        
        Args:
            mediaFileId (UUID | None): Optional parent media file ID filter.
            
        Returns:
            Sequence[MediaVariant]: List of media variants.
        """
        return await self.repo.getAll(mediaFileId=mediaFileId)

    async def updateMediaVariant(self, variantId: uuid.UUID, data: MediaVariantUpdate) -> MediaVariant:
        """
        Updates fields on an existing MediaVariant, checking name uniqueness on parent file.
        
        Args:
            variantId (UUID): Unique ID of the variant to update.
            data (MediaVariantUpdate): Target update fields schema.
            
        Returns:
            MediaVariant: The updated model instance.
            
        Raises:
            NotFoundError: If the variant does not exist.
            ConflictError: If updating to an existing variant name of the parent file.
        """
        variant = await self.repo.getById(variantId)
        if not variant:
            raise NotFoundError("MediaVariant", str(variantId))

        updateData = data.model_dump(exclude_unset=True)

        # Validate unique combination if changing mediaFileId or variantName
        mediaFileId = updateData.get("mediaFileId", variant.mediaFileId)
        variantName = updateData.get("variantName", variant.variantName)
        if "mediaFileId" in updateData or "variantName" in updateData:
            existing = await self.repo.getByMediaFileAndVariant(mediaFileId, variantName)
            if existing and existing.id != variantId:
                raise ConflictError(f"Variant '{variantName}' already exists for media file '{mediaFileId}'")

        result = await self.repo.update(variant, updateData)
        await self.session.commit()
        return result

    async def deleteMediaVariant(self, variantId: uuid.UUID) -> None:
        """
        Deletes a MediaVariant record.
        
        Args:
            variantId (UUID): Unique ID of the variant to delete.
            
        Raises:
            NotFoundError: If the variant does not exist.
        """
        variant = await self.repo.getById(variantId)
        if not variant:
            raise NotFoundError("MediaVariant", str(variantId))
        await self.repo.delete(variant)
        await self.session.commit()