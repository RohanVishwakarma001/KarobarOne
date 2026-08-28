# Owner - pradhansaikat123@gmail.com
# SQLAlchemy database models for Tag Management. Defines tables, relationships,
# indexes, and constraints for tags and tag mappings.

import uuid
from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    ForeignKey,
    Index,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.types import TIMESTAMP

from app.db.base import Base


# ─────────────────────────────────────────────
# tags
# ─────────────────────────────────────────────
class Tag(Base):
    __tablename__ = "tags"
    __table_args__ = (
        CheckConstraint(
            "tag_type IN ('PRODUCT', 'SERVICE', 'CUSTOMER', 'ORDER', 'BOOKING', 'BLOG', 'OFFER', 'CATEGORY', 'BRAND', 'GENERAL')",
            name="ck_tags_tag_type",
        ),
        CheckConstraint(
            "color_code IS NULL OR length(color_code) = 7",
            name="ck_tags_color_code",
        ),
        # Unique constraints for tags within the same store
        UniqueConstraint("store_id", "tag_type", "tag_name", name="uq_tags_store_name"),
        UniqueConstraint("store_id", "tag_type", "tag_slug", name="uq_tags_store_slug"),
        # Partial unique indexes for platform tags (where store_id is NULL)
        Index(
            "uq_tags_platform_name",
            "tag_type",
            "tag_name",
            unique=True,
            postgresql_where="store_id IS NULL AND deleted_at IS NULL",
        ),
        Index(
            "uq_tags_platform_slug",
            "tag_type",
            "tag_slug",
            unique=True,
            postgresql_where="store_id IS NULL AND deleted_at IS NULL",
        ),
        # Extra indexes as recommended
        Index("idx_tags_store_id", "store_id"),
        Index("idx_tags_tenant_id", "tenant_id"),
        Index("idx_tags_tag_type", "tag_type"),
        Index("idx_tags_is_system_tag", "is_system_tag"),
        Index("idx_tags_is_active", "is_active"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenantId = Column("tenant_id", UUID(as_uuid=True), nullable=True)  # FK → tenants_details.id
    storeId = Column("store_id", UUID(as_uuid=True), nullable=True)  # FK → stores.id
    tagName = Column("tag_name", String(100), nullable=False)
    tagSlug = Column("tag_slug", String(120), nullable=False)
    tagType = Column("tag_type", String(30), nullable=False)
    description = Column("description", String(500), nullable=True)
    colorCode = Column("color_code", String(7), nullable=True)
    isSystemTag = Column("is_system_tag", Boolean, default=False, nullable=False)
    isActive = Column("is_active", Boolean, default=True, nullable=False)
    createdBy = Column("created_by", UUID(as_uuid=True), nullable=False)  # FK → users.id
    createdAt = Column("created_at", TIMESTAMP, server_default=func.now(), nullable=False)
    updatedAt = Column(
        "updated_at",
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    deletedAt = Column("deleted_at", TIMESTAMP, nullable=True)

    mappings = relationship("TagMapping", back_populates="tag", cascade="all, delete-orphan")


# ─────────────────────────────────────────────
# tag_mappings
# ─────────────────────────────────────────────
class TagMapping(Base):
    __tablename__ = "tag_mappings"
    __table_args__ = (
        CheckConstraint(
            "entity_type IN ('PRODUCT', 'SERVICE', 'CUSTOMER', 'ORDER', 'BOOKING', 'BLOG', 'OFFER', 'CATEGORY', 'BRAND')",
            name="ck_tagMappings_entity_type",
        ),
        UniqueConstraint("tag_id", "entity_type", "entity_id", name="uq_tagMappings_prevent_duplicate"),
        # Recommended indexes
        Index("idx_tagMappings_tag_id", "tag_id"),
        Index("idx_tagMappings_entity_type", "entity_type"),
        Index("idx_tagMappings_entity_id", "entity_id"),
        Index("idx_tagMappings_mapped_by", "mapped_by"),
        Index("idx_tagMappings_created_at", "created_at"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tagId = Column("tag_id", UUID(as_uuid=True), ForeignKey("tags.id"), nullable=False)
    entityType = Column("entity_type", String(30), nullable=False)
    entityId = Column("entity_id", UUID(as_uuid=True), nullable=False)
    mappedBy = Column("mapped_by", UUID(as_uuid=True), nullable=False)  # FK → users.id
    createdAt = Column("created_at", TIMESTAMP, server_default=func.now(), nullable=False)

    tag = relationship("Tag", back_populates="mappings")
