# Owner - pradhansaikat123@gmail.com
# SQLAlchemy database models for Category Management. Defines tables, relationships,
# indexes, and constraints for categories.

import uuid  # Standard UUID generation library
from sqlalchemy import (  # SQLAlchemy core schema elements and types
    Boolean,
    CheckConstraint,
    Column,
    ForeignKey,
    Index,
    SmallInteger,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID  # PostgreSQL specific UUID type
from sqlalchemy.orm import relationship  # Relationship builder for SQLAlchemy models
from sqlalchemy.sql import func  # SQL functions like func.now()
from sqlalchemy.types import TIMESTAMP  # Timestamp data type for database columns

from app.db.base import Base  # Declarative base class for models



# ─────────────────────────────────────────────
# categories
# ─────────────────────────────────────────────
class Category(Base):
    __tablename__ = "categories"
    __table_args__ = (
        CheckConstraint(
            "category_type IN ('PRODUCT', 'SERVICE', 'BOTH')",
            name="ck_categories_category_type",
        ),
        CheckConstraint(
            "approval_status IN ('PENDING', 'APPROVED', 'REJECTED')",
            name="ck_categories_approval_status",
        ),
        # Unique constraints for categories within the same store
        UniqueConstraint("store_id", "category_name", name="uq_categories_store_name"),
        UniqueConstraint("store_id", "category_slug", name="uq_categories_store_slug"),
        # Partial unique indexes for platform categories (where store_id is NULL)
        Index(
            "uq_categories_platform_name",
            "category_name",
            unique=True,
            postgresql_where="store_id IS NULL AND deleted_at IS NULL",
        ),
        Index(
            "uq_categories_platform_slug",
            "category_slug",
            unique=True,
            postgresql_where="store_id IS NULL AND deleted_at IS NULL",
        ),
        # Recommended indexes for performance
        Index("idx_categories_store_id", "store_id"),
        Index("idx_categories_tenant_id", "tenant_id"),
        Index("idx_categories_parent_id", "parent_category_id"),
        Index("idx_categories_is_active", "is_active"),
        Index("idx_categories_category_type", "category_type"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenantId = Column("tenant_id", UUID(as_uuid=True), nullable=True)  # FK → tenants_details.id
    storeId = Column("store_id", UUID(as_uuid=True), nullable=True)  # FK → stores.id
    parentCategoryId = Column("parent_category_id", UUID(as_uuid=True), ForeignKey("categories.id"), nullable=True)  # FK → categories.id
    categoryType = Column("category_type", String(20), nullable=False)  # PRODUCT / SERVICE / BOTH
    categoryName = Column("category_name", String(150), nullable=False)
    categorySlug = Column("category_slug", String(180), nullable=False)
    shortDescription = Column("short_description", String(500), nullable=True)
    longDescription = Column("long_description", Text, nullable=True)
    imageMediaId = Column("image_media_id", UUID(as_uuid=True), nullable=True)  # FK → media_files.id
    iconMediaId = Column("icon_media_id", UUID(as_uuid=True), nullable=True)  # FK → media_files.id
    displayOrder = Column("display_order", SmallInteger, default=0, nullable=False)
    levelNumber = Column("level_number", SmallInteger, default=1, nullable=False)
    approvalStatus = Column("approval_status", String(20), nullable=False, default="PENDING")  # PENDING / APPROVED / REJECTED
    isSystemCategory = Column("is_system_category", Boolean, default=False, nullable=False)
    isActive = Column("is_active", Boolean, default=True, nullable=False)
    createdBy = Column("created_by", UUID(as_uuid=True), nullable=False)  # FK → users.id
    approvedBy = Column("approved_by", UUID(as_uuid=True), nullable=True)  # FK → users.id
    approvedAt = Column("approved_at", TIMESTAMP, nullable=True)
    createdAt = Column("created_at", TIMESTAMP, server_default=func.now(), nullable=False)
    updatedAt = Column(
        "updated_at",
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    deletedAt = Column("deleted_at", TIMESTAMP, nullable=True)

    # Self-referential relationship to support hierarchy
    parent = relationship("Category", remote_side=[id], back_populates="subcategories")
    subcategories = relationship("Category", back_populates="parent", cascade="all, delete-orphan")
