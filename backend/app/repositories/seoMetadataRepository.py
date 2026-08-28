# Owner: mousamdas156@gmail.com
"""
================================================================================
SEO METADATA DATABASE REPOSITORY (seoMetadataRepository.py)
================================================================================
Why this file is used:
- This file handles data access queries and operations for the `SeoMetadata` entity.
- It abstracts the underlying SQLAlchemy database actions, providing query methods to fetch
  and write SEO metadata based on entity ID, type, slug, or tenant ID.
================================================================================
"""

# Standard library imports for UUIDs and sequences
import uuid
from typing import Sequence

# Third-party database modules
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# Associated database ORM model
from app.db.models.seoMetadata import SeoMetadata


class SeoMetadataRepository:
    """
    Repository class encapsulating database operations for the SeoMetadata model.
    """
    def __init__(self, session: AsyncSession):
        """
        Initializes the repository with an asynchronous database session.
        
        Args:
            session (AsyncSession): The database session.
        """
        self.session = session

    async def getById(self, seoId: uuid.UUID) -> SeoMetadata | None:
        """
        Retrieves an SEO record by its unique UUID.
        
        Args:
            seoId (UUID): Unique ID of the SEO record.
            
        Returns:
            SeoMetadata | None: The found SEO metadata, or None.
        """
        result = await self.session.execute(
            select(SeoMetadata).where(SeoMetadata.id == seoId)
        )
        return result.scalar_one_or_none()

    async def getByEntity(self, entityType: str, entityId: uuid.UUID) -> SeoMetadata | None:
        """
        Retrieves an SEO record associated with a specific entity type and entity ID.
        
        Args:
            entityType (str): Type of entity (e.g. 'PRODUCT').
            entityId (UUID): Unique ID of the target entity instance.
            
        Returns:
            SeoMetadata | None: The found SEO metadata, or None.
        """
        result = await self.session.execute(
            select(SeoMetadata).where(
                SeoMetadata.entityType == entityType,
                SeoMetadata.entityId == entityId
            )
        )
        return result.scalar_one_or_none()

    async def getBySlug(self, entityType: str, slug: str) -> SeoMetadata | None:
        """
        Retrieves an SEO record associated with an entity type and URL-friendly slug.
        
        Args:
            entityType (str): Type of entity (e.g. 'BLOG').
            slug (str): Unique URL slug identifier.
            
        Returns:
            SeoMetadata | None: The found SEO metadata, or None.
        """
        result = await self.session.execute(
            select(SeoMetadata).where(
                SeoMetadata.entityType == entityType,
                SeoMetadata.slug == slug
            )
        )
        return result.scalar_one_or_none()

    async def getAll(self, tenantId: uuid.UUID | None = None) -> Sequence[SeoMetadata]:
        """
        Fetches all SEO metadata records, optionally filtered by tenant.
        
        Args:
            tenantId (UUID | None): Optional tenant ID filter.
            
        Returns:
            Sequence[SeoMetadata]: List of SEO records.
        """
        stmt = select(SeoMetadata).order_by(SeoMetadata.createdAt.desc())
        if tenantId:
            stmt = stmt.where(SeoMetadata.tenantId == tenantId)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(self, seo: SeoMetadata) -> SeoMetadata:
        """
        Persists a new SeoMetadata entity to the database session.
        
        Args:
            seo (SeoMetadata): The unsaved SEO model instance.
            
        Returns:
            SeoMetadata: The persisted model with generated ID and attributes.
        """
        self.session.add(seo)
        await self.session.flush()
        await self.session.refresh(seo)
        return seo

    async def update(self, seo: SeoMetadata, data: dict) -> SeoMetadata:
        """
        Updates fields of an existing SeoMetadata record dynamically.
        
        Args:
            seo (SeoMetadata): The SEO model instance to update.
            data (dict): Dictionary mapping attributes to update values.
            
        Returns:
            SeoMetadata: The updated and refreshed model instance.
        """
        for key, value in data.items():
            setattr(seo, key, value)
        await self.session.flush()
        await self.session.refresh(seo)
        return seo

    async def delete(self, seo: SeoMetadata) -> None:
        """
        Removes an SEO metadata record from the database.
        
        Args:
            seo (SeoMetadata): The SEO model instance to delete.
        """
        await self.session.delete(seo)
        await self.session.flush()
