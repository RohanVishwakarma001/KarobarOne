# Owner: mousamdas156@gmail.com
"""
================================================================================
SEO METADATA SCHEMAS (seoMetadata.py)
================================================================================
Why this file is used:
- This file contains the Pydantic validation models for creating, updating, and 
  representing `SeoMetadata` database records.
- It validates search indexes configurations, meta tags, and seo score values.
================================================================================
"""

# Standard library imports for UUIDs, datetimes, and Decimals
import uuid
from datetime import datetime
from decimal import Decimal

# Third-party Pydantic components for data validation and schema creation
from pydantic import BaseModel, ConfigDict, Field


class SeoMetadataCreate(BaseModel):
    """
    Schema for validating input when creating a new SeoMetadata entry.
    """
    tenantId: uuid.UUID
    entityType: str = Field(..., max_length=50)
    entityId: uuid.UUID
    metaTitle: str | None = Field(None, max_length=255)
    metaDescription: str | None = Field(None, max_length=500)
    canonicalUrl: str | None = Field(None, max_length=1000)
    slug: str = Field(..., max_length=255)
    robotsIndex: bool = True
    robotsFollow: bool = True
    seoScore: Decimal | None = None


class SeoMetadataUpdate(BaseModel):
    """
    Schema for validating input when updating an existing SeoMetadata.
    """
    metaTitle: str | None = Field(None, max_length=255)
    metaDescription: str | None = Field(None, max_length=500)
    canonicalUrl: str | None = Field(None, max_length=1000)
    slug: str | None = Field(None, max_length=255)
    robotsIndex: bool | None = None
    robotsFollow: bool | None = None
    seoScore: Decimal | None = None


class SeoMetadataResponse(BaseModel):
    """
    Schema representing the structure of a SeoMetadata returned in API responses.
    """
    # Configure Pydantic to read ORM models automatically
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    tenantId: uuid.UUID
    entityType: str
    entityId: uuid.UUID
    metaTitle: str | None
    metaDescription: str | None
    canonicalUrl: str | None
    slug: str
    robotsIndex: bool
    robotsFollow: bool
    seoScore: Decimal | None
    createdAt: datetime
    updatedAt: datetime

class SeoScoreRequest(BaseModel):
    """
    Request schema for SEO score calculation.
    """
    metaTitle: str | None = Field(None, max_length=255)
    metaDescription: str | None = Field(None, max_length=500)
    canonicalUrl: str | None = Field(None, max_length=1000)
    slug: str | None = Field(None, max_length=255)
    content: str | None = None
    robotsIndex: bool = True
    robotsFollow: bool = True


class SeoScoreResponse(BaseModel):
    """
    Response schema for SEO score calculation.
    """
    seoScore: int
    grade: str
    suggestions: list[str]

class SeoScoreRequest(BaseModel):
    """
    Request schema for SEO score calculation.
    """
    metaTitle: str | None = Field(None, max_length=255)
    metaDescription: str | None = Field(None, max_length=500)
    canonicalUrl: str | None = Field(None, max_length=1000)
    slug: str | None = Field(None, max_length=255)
    content: str | None = None
    robotsIndex: bool = True
    robotsFollow: bool = True


class SeoScoreResponse(BaseModel):
    """
    Response schema for SEO score calculation.
    """
    seoScore: int
    grade: str
    suggestions: list[str]


class AiSeoSuggestionRequest(BaseModel):
    metaTitle: str | None = None
    metaDescription: str | None = None
    content: str | None = None


class AiSeoSuggestionResponse(BaseModel):
    improvedTitle: str
    improvedDescription: str
    keywords: list[str]


class SeoAuditRequest(BaseModel):
    metaTitle: str | None = None
    metaDescription: str | None = None
    canonicalUrl: str | None = None
    slug: str | None = None
    content: str | None = None
    robotsIndex: bool = True
    robotsFollow: bool = True


class SeoAuditResponse(BaseModel):
    seoScore: int
    grade: str

    titleLength: int
    descriptionLength: int
    contentLength: int
    wordCount: int

    keywordDensity: float
    readability: str

    canonical: bool
    robots: bool

    issues: list[str]
    recommendations: list[str]


class KeywordDensityRequest(BaseModel):
    content: str
    targetKeyword: str


class KeywordDensityResponse(BaseModel):
    keyword: str
    count: int
    totalWords: int
    density: float
    status: str
    recommendation: str
