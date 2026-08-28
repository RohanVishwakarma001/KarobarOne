# Owner: mousamdas156@gmail.com
"""
================================================================================
SEO METADATA ORM MODEL (seoMetadata.py)
================================================================================
Why this file is used:
- This file defines the `SeoMetadata` database model mapping to the 'seo_metadata' table.
- It stores SEO tag preferences (titles, descriptions, canonical URLs, robots meta rules,
  and seo scores) dynamically linked to other business models via entity types and IDs.
================================================================================
"""

# Standard library imports for UUIDs and Decimals
import uuid
from decimal import Decimal

# Third-party SQLAlchemy model fields, constraints
from sqlalchemy import Boolean, CheckConstraint, ForeignKey, Numeric, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

# Custom base model that provides ID, createdAt, and updatedAt fields
from app.db.base import BaseModelWithUpdate


class SeoMetadata(BaseModelWithUpdate):
    """
    ORM Model representing the SEO metadata tags for any database resource (e.g. products, blog posts).
    Inherits primary key UUID and timestamps from BaseModelWithUpdate.
    """
    __tablename__ = "seo_metadata"

    # Enforce CHECK constraint on entity_type and uniqueness on entity_id and slug
    __table_args__ = (
        CheckConstraint(
            "entity_type IN ('STORE', 'PRODUCT', 'SERVICE', 'BLOG', 'CATEGORY', 'OFFER', 'POLICY', 'FORM')",
            name="ck_seo_metadata_entity_type",
        ),
        UniqueConstraint(
            "entity_type",
            "entity_id",
            name="uq_seo_metadata_entity_type_entity_id",
        ),
        UniqueConstraint(
            "entity_type",
            "slug",
            name="uq_seo_metadata_entity_type_slug",
        ),
    )

    # Reference to the TenantDetails owner of this SEO record
    tenantId: Mapped[uuid.UUID] = mapped_column(
        "tenant_id",
        UUID(as_uuid=True),
        ForeignKey("tenants_details.id"),
        nullable=False,
    )

    # Identifies the type of entity (e.g. 'PRODUCT')
    entityType: Mapped[str] = mapped_column(
        "entity_type",
        String(50),
        nullable=False,
    )

    # Foreign key referencing the actual entity row (generic UUID identifier)
    entityId: Mapped[uuid.UUID] = mapped_column(
        "entity_id",
        UUID(as_uuid=True),
        nullable=False,
    )

    # Page title tag for search engines (meta title)
    metaTitle: Mapped[str | None] = mapped_column(
        "meta_title",
        String(255),
        nullable=True,
    )

    # Page description tag for search engines (meta description)
    metaDescription: Mapped[str | None] = mapped_column(
        "meta_description",
        String(500),
        nullable=True,
    )

    # Canonical URL tag to avoid duplicate content penalties
    canonicalUrl: Mapped[str | None] = mapped_column(
        "canonical_url",
        String(1000),
        nullable=True,
    )

    # URL-friendly slug representing the route path for this entity
    slug: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # Dictates if search engine bots should index this page (true = index)
    robotsIndex: Mapped[bool] = mapped_column(
        "robots_index",
        Boolean,
        default=True,
        nullable=False,
    )

    # Dictates if search engine bots should follow links on this page (true = follow)
    robotsFollow: Mapped[bool] = mapped_column(
        "robots_follow",
        Boolean,
        default=True,
        nullable=False,
    )

    # Numerical rating representing SEO optimization health score (scale up to 100.00)
    seoScore: Mapped[Decimal | None] = mapped_column(
        "seo_score",
        Numeric(5, 2),
        nullable=True,
    )
