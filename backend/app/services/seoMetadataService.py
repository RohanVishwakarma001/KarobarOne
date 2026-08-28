# Owner: mousamdas156@gmail.com
# ================================================================================
# FILE: services/seoMetadataService.py — SEO Metadata Service
# ================================================================================
# Why this file is used:
#   - Coordinates search indices and web crawls mapped to catalog entities.
#
# What components are inside:
#   - ALLOWED_ENTITY_TYPES -> Set of supported entity codes.
#   - SeoMetadataService:
#       - _validateEntityType()      -> Validates entity configurations.
#       - createSeoMetadata()        -> Creates SEO logs.
#       - getSeoMetadata()           -> Resolves details.
#       - getSeoMetadataByEntity()   -> Finds records matching catalog entities.
#       - getSeoMetadataBySlug()     -> Finds records matching URL slugs.
#       - listSeoMetadata()          -> Returns SEO records.
#       - updateSeoMetadata()        -> Modifies crawl settings.
#       - deleteSeoMetadata()        -> Removes crawl settings.
# ================================================================================
"""
================================================================================
SEO METADATA SERVICE (seoMetadataService.py)
================================================================================
Why this file is used:
- This file contains the business logic layer for the `SeoMetadata` entity.
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
from app.core.exceptionsCompat import ConflictError, NotFoundError, BusinessValidationError

# Database ORM model and repository
from app.db.models.seoMetadata import SeoMetadata
from app.repositories.seoMetadataRepository import SeoMetadataRepository

# Pydantic schemas for data validation
from app.schemas.seoMetadata import SeoMetadataCreate, SeoMetadataUpdate

# Allowed entity types matching check constraints on DB schema
ALLOWED_ENTITY_TYPES = {
    'STORE', 'PRODUCT', 'SERVICE', 'BLOG', 'CATEGORY', 'OFFER', 'POLICY', 'FORM'
}


class SeoMetadataService:
    """
    Service class orchestrating business processes for SeoMetadata.
    """
    def __init__(self, session: AsyncSession):
        """
        Initializes the service with a repository instance and database session.
        
        Args:
            session (AsyncSession): The database session.
        """
        self.repo = SeoMetadataRepository(session)
        self.session = session

    def _validateEntityType(self, entityType: str) -> None:
        """
        Helper method to validate if an entityType is supported.
        
        Args:
            entityType (str): The entity type string to validate.
            
        Raises:
            BusinessValidationError: If the entity type is invalid.
        """
        if entityType not in ALLOWED_ENTITY_TYPES:
            raise BusinessValidationError(
                f"Entity type '{entityType}' is invalid. Allowed types are: {', '.join(ALLOWED_ENTITY_TYPES)}"
            )

    async def createSeoMetadata(self, data: SeoMetadataCreate) -> SeoMetadata:
        """
        Validates and creates a new SeoMetadata record.
        
        Args:
            data (SeoMetadataCreate): Input schema data.
            
        Returns:
            SeoMetadata: The created database model instance.
            
        Raises:
            ConflictError: If SEO metadata already exists for the entity ID or slug.
        """
        self._validateEntityType(data.entityType)

        # Check unique constraint (entity_type, entity_id)
        if await self.repo.getByEntity(data.entityType, data.entityId):
            raise ConflictError(
                f"SEO metadata already exists for entity type '{data.entityType}' with ID '{data.entityId}'"
            )

        # Check unique constraint (entity_type, slug)
        if await self.repo.getBySlug(data.entityType, data.slug):
            raise ConflictError(
                f"SEO metadata with slug '{data.slug}' already exists for entity type '{data.entityType}'"
            )

        seo = SeoMetadata(**data.model_dump())
        result = await self.repo.create(seo)
        await self.session.commit()
        return result

    async def getSeoMetadata(self, seoId: uuid.UUID) -> SeoMetadata:
        """
        Retrieves a SeoMetadata record, throwing NotFoundError if missing.
        
        Args:
            seoId (UUID): Unique ID of the SEO record.
            
        Returns:
            SeoMetadata: The found database model instance.
            
        Raises:
            NotFoundError: If the SEO record is not found.
        """
        seo = await self.repo.getById(seoId)
        if not seo:
            raise NotFoundError("SeoMetadata", str(seoId))
        return seo

    async def getSeoMetadataByEntity(self, entityType: str, entityId: uuid.UUID) -> SeoMetadata:
        """
        Retrieves a SeoMetadata record by its entity type and entity ID.
        
        Args:
            entityType (str): Type of entity.
            entityId (UUID): Unique ID of the target resource.
            
        Returns:
            SeoMetadata: The found database model instance.
            
        Raises:
            NotFoundError: If the SEO record does not exist.
        """
        self._validateEntityType(entityType)
        seo = await self.repo.getByEntity(entityType, entityId)
        if not seo:
            raise NotFoundError(f"SeoMetadata for entity {entityType}", str(entityId))
        return seo

    async def getSeoMetadataBySlug(self, entityType: str, slug: str) -> SeoMetadata:
        """
        Retrieves a SeoMetadata record by its entity type and URL slug.
        
        Args:
            entityType (str): Type of entity.
            slug (str): Route slug.
            
        Returns:
            SeoMetadata: The found database model instance.
            
        Raises:
            NotFoundError: If the SEO record does not exist.
        """
        self._validateEntityType(entityType)
        seo = await self.repo.getBySlug(entityType, slug)
        if not seo:
            raise NotFoundError(f"SeoMetadata for entity {entityType} with slug", slug)
        return seo

    async def listSeoMetadata(self, tenantId: uuid.UUID | None = None) -> Sequence[SeoMetadata]:
        """
        Lists all SeoMetadata records, optionally filtered by tenant.
        
        Args:
            tenantId (UUID | None): Optional tenant ID filter parameter.
            
        Returns:
            Sequence[SeoMetadata]: List of SEO records.
        """
        return await self.repo.getAll(tenantId=tenantId)

    async def updateSeoMetadata(self, seoId: uuid.UUID, data: SeoMetadataUpdate) -> SeoMetadata:
        """
        Updates fields on an existing SeoMetadata record, checking slug uniqueness.
        
        Args:
            seoId (UUID): Unique ID of the SEO record to update.
            data (SeoMetadataUpdate): Target update fields schema.
            
        Returns:
            SeoMetadata: The updated model instance.
            
        Raises:
            NotFoundError: If the SEO record does not exist.
            ConflictError: If updating to a slug that already exists for that entity type.
        """
        seo = await self.repo.getById(seoId)
        if not seo:
            raise NotFoundError("SeoMetadata", str(seoId))

        updateData = data.model_dump(exclude_unset=True)

        entityType = seo.entityType
        entityId = seo.entityId

        # Check unique constraint (entity_type, slug) if slug is updated
        if "slug" in updateData:
            slug = updateData["slug"]
            existing = await self.repo.getBySlug(entityType, slug)
            if existing and existing.id != seoId:
                raise ConflictError(
                    f"SEO metadata with slug '{slug}' already exists for entity type '{entityType}'"
                )

        result = await self.repo.update(seo, updateData)
        await self.session.commit()
        return result

    async def deleteSeoMetadata(self, seoId: uuid.UUID) -> None:
        """
        Deletes a SeoMetadata record.
        
        Args:
            seoId (UUID): Unique ID of the SEO record to delete.
            
        Raises:
            NotFoundError: If the SEO record does not exist.
        """
        seo = await self.repo.getById(seoId)
        if not seo:
            raise NotFoundError("SeoMetadata", str(seoId))
        await self.repo.delete(seo)
        await self.session.commit()
    def _generateGrade(self, score: int) -> str:
        if score >= 90:
            return "A"
        elif score >= 75:
            return "B"
        elif score >= 60:
            return "C"
        elif score >= 40:
            return "D"
        return "F"

    async def calculateSeoScore(self, data):
        score = 100
        suggestions = []

        if not data.metaTitle:
            score -= 15
            suggestions.append("Meta title is missing.")
        elif len(data.metaTitle) < 30 or len(data.metaTitle) > 60:
            score -= 5
            suggestions.append("Meta title should be between 30 and 60 characters.")

        if not data.metaDescription:
            score -= 15
            suggestions.append("Meta description is missing.")
        elif len(data.metaDescription) < 120 or len(data.metaDescription) > 160:
            score -= 5
            suggestions.append("Meta description should be between 120 and 160 characters.")

        if not data.slug:
            score -= 10
            suggestions.append("Slug is missing.")

        if not data.canonicalUrl:
            score -= 10
            suggestions.append("Canonical URL is missing.")

        if not data.content or len(data.content) < 300:
            score -= 20
            suggestions.append("Content should contain at least 300 characters.")

        if not data.robotsIndex:
            score -= 10
            suggestions.append("Robots index is disabled.")

        if not data.robotsFollow:
            score -= 10
            suggestions.append("Robots follow is disabled.")

        score = max(score, 0)

        return {
            "seoScore": score,
            "grade": self._generateGrade(score),
            "suggestions": suggestions,
        }


    async def generateAiSeoSuggestions(self, data):
        """
        Generate AI-like SEO suggestions.
        Currently rule-based.
        Future: Replace with OpenAI/Gemini call.
        """

        title = data.metaTitle or ""
        description = data.metaDescription or ""
        content = data.content or ""

        improvedTitle = title
        if len(title) < 30:
            improvedTitle = f"{title} | Complete Guide"

        improvedDescription = description
        if len(description) < 120:
            improvedDescription = (
                description +
                " Learn everything you need to know with detailed information, tips, and best practices."
            )

        keywords = []

        words = (
            content.lower()
            .replace(".", "")
            .replace(",", "")
            .split()
        )

        for word in words:
            if len(word) > 4 and word not in keywords:
                keywords.append(word)

            if len(keywords) == 5:
                break

        return {
            "improvedTitle": improvedTitle,
            "improvedDescription": improvedDescription,
            "keywords": keywords,
        }


    async def auditSeo(self, data):
        """
        Complete SEO Audit
        """

        issues = []
        recommendations = []
        score = 100

        titleLength = len(data.metaTitle or "")
        descriptionLength = len(data.metaDescription or "")
        contentLength = len(data.content or "")

        words = (data.content or "").split()
        wordCount = len(words)

        keywordDensity = round(min(wordCount / 100, 5.0), 2) if wordCount else 0

        readability = (
            "Excellent"
            if wordCount > 600
            else "Good"
            if wordCount > 300
            else "Needs Improvement"
        )

        if titleLength < 30 or titleLength > 60:
            score -= 10
            issues.append("Meta title should be between 30 and 60 characters.")
            recommendations.append("Optimize the title length.")

        if descriptionLength < 120 or descriptionLength > 160:
            score -= 10
            issues.append("Meta description should be between 120 and 160 characters.")
            recommendations.append("Optimize the meta description.")

        if contentLength < 300:
            score -= 20
            issues.append("Content is too short.")
            recommendations.append("Increase the content length.")

        if not data.canonicalUrl:
            score -= 10
            issues.append("Canonical URL missing.")
            recommendations.append("Add a canonical URL.")

        if not data.robotsIndex:
            score -= 5
            issues.append("Robots index disabled.")
            recommendations.append("Enable robots index.")

        if not data.robotsFollow:
            score -= 5
            issues.append("Robots follow disabled.")
            recommendations.append("Enable robots follow.")

        score = max(score, 0)

        return {
            "seoScore": score,
            "grade": self._generateGrade(score),
            "titleLength": titleLength,
            "descriptionLength": descriptionLength,
            "contentLength": contentLength,
            "wordCount": wordCount,
            "keywordDensity": keywordDensity,
            "readability": readability,
            "canonical": bool(data.canonicalUrl),
            "robots": data.robotsIndex and data.robotsFollow,
            "issues": issues,
            "recommendations": recommendations,
        }


    async def analyzeKeywordDensity(self, data):
        """
        Analyze keyword density for SEO.
        """

        import re

        content = (data.content or "").lower()
        keyword = (data.targetKeyword or "").lower().strip()

        # Remove punctuation
        words = re.findall(r"\b\w+\b", content)

        totalWords = len(words)

        count = sum(1 for word in words if word == keyword)

        density = round((count / totalWords) * 100, 2) if totalWords else 0.0

        if density == 0:
            status = "Keyword Missing"
            recommendation = "Include the target keyword naturally in the content."
        elif density < 1:
            status = "Under Optimized"
            recommendation = "Increase keyword usage to around 1–3%."
        elif density <= 3:
            status = "Well Optimized"
            recommendation = "Keyword density is within the recommended range."
        else:
            status = "Over Optimized"
            recommendation = "Reduce keyword usage to avoid keyword stuffing."

        return {
            "keyword": keyword,
            "count": count,
            "totalWords": totalWords,
            "density": density,
            "status": status,
            "recommendation": recommendation,
        }

