# Owner - pradhansaikat123@gmail.com
# SQLAlchemy database models for Brands and Brand Approvals. Defines tables, relationships,
# and constraints for brands and request/review states.

# Import standard uuid library for generating unique IDs
import uuid
# Import standard SQLAlchemy columns, constraints, and column structures
from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    Date,
    ForeignKey,
    String,
    Text,
    UniqueConstraint,
)
# Import PostgreSQL-specific column types (database UUID)
from sqlalchemy.dialects.postgresql import UUID
# Import relationship construct to manage database mappings between related tables
from sqlalchemy.orm import relationship
# Import func to invoke SQL functions like NOW() dynamically
from sqlalchemy.sql import func
# Import TIMESTAMP column type for storing timestamps
from sqlalchemy.types import TIMESTAMP
# Import declarative Base class to associate models with a single metadata registry
from app.db.base import Base


# ─────────────────────────────────────────────
# brands
# ─────────────────────────────────────────────
class Brand(Base):
    __tablename__ = "brands"
    __table_args__ = (
        UniqueConstraint("brand_slug", name="uq_brands_brand_slug"),
        UniqueConstraint("owner_store_id", "brand_name", name="uq_brands_owner_store_brand_name"),
        CheckConstraint(
            "verification_status IN ('PENDING', 'APPROVED', 'REJECTED')",
            name="ck_brands_verification_status"
        ),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenantId = Column("tenant_id", UUID(as_uuid=True), nullable=True, index=True)
    ownerStoreId = Column("owner_store_id", UUID(as_uuid=True), nullable=True, index=True)
    brandName = Column("brand_name", String(150), nullable=False, index=True)
    brandSlug = Column("brand_slug", String(180), nullable=False)
    logoMediaId = Column("logo_media_id", UUID(as_uuid=True), nullable=True)
    websiteUrl = Column("website_url", String(500), nullable=True)
    supportEmail = Column("support_email", String(255), nullable=True)
    supportMobile = Column("support_mobile", String(15), nullable=True)
    description = Column("description", Text, nullable=True)
    countryOfOrigin = Column("country_of_origin", String(100), nullable=True)
    gstNumber = Column("gst_number", String(15), nullable=True)
    trademarkNumber = Column("trademark_number", String(100), nullable=True)
    trademarkDocumentMediaId = Column("trademark_document_media_id", UUID(as_uuid=True), nullable=True)
    verificationStatus = Column("verification_status", String(20), nullable=False, default="PENDING")
    isPlatformBrand = Column("is_platform_brand", Boolean, default=False, index=True)
    isActive = Column("is_active", Boolean, default=True, index=True)
    createdBy = Column("created_by", UUID(as_uuid=True), nullable=False)
    approvedBy = Column("approved_by", UUID(as_uuid=True), nullable=True)
    approvedAt = Column("approved_at", TIMESTAMP, nullable=True)
    createdAt = Column("created_at", TIMESTAMP, nullable=False, server_default=func.now())
    updatedAt = Column("updated_at", TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())
    deletedAt = Column("deleted_at", TIMESTAMP, nullable=True)

    approvals = relationship(
        "BrandApproval",
        back_populates="brand",
        cascade="all, delete-orphan",
        lazy="selectin",
    )


# ─────────────────────────────────────────────
# brand_approvals
# ─────────────────────────────────────────────
class BrandApproval(Base):
    __tablename__ = "brand_approvals"
    __table_args__ = (
        UniqueConstraint("brand_id", "requesting_store_id", name="uq_brandApprovals_brand_requesting_store"),
        CheckConstraint(
            "request_status IN ('PENDING', 'APPROVED', 'REJECTED', 'REVOKED', 'EXPIRED')",
            name="ck_brandApprovals_request_status"
        ),
        CheckConstraint(
            "approval_end_date IS NULL OR approval_start_date <= approval_end_date",
            name="ck_brandApprovals_date_range"
        ),
        CheckConstraint(
            "requesting_store_id <> brand_owner_store_id",
            name="ck_brandApprovals_different_stores"
        ),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    brandId = Column("brand_id", UUID(as_uuid=True), ForeignKey("brands.id"), nullable=False, index=True)
    requestingStoreId = Column("requesting_store_id", UUID(as_uuid=True), nullable=False, index=True)
    brandOwnerStoreId = Column("brand_owner_store_id", UUID(as_uuid=True), nullable=False, index=True)
    requestStatus = Column("request_status", String(20), nullable=False, default="PENDING", index=True)
    requestMessage = Column("request_message", String(1000), nullable=True)
    supportingDocumentMediaId = Column("supporting_document_media_id", UUID(as_uuid=True), nullable=True)
    reviewedBy = Column("reviewed_by", UUID(as_uuid=True), nullable=True)
    reviewedAt = Column("reviewed_at", TIMESTAMP, nullable=True)
    rejectionReason = Column("rejection_reason", String(1000), nullable=True)
    approvalStartDate = Column("approval_start_date", Date, nullable=True)
    approvalEndDate = Column("approval_end_date", Date, nullable=True, index=True)
    revokedAt = Column("revoked_at", TIMESTAMP, nullable=True)
    revokedBy = Column("revoked_by", UUID(as_uuid=True), nullable=True)
    createdAt = Column("created_at", TIMESTAMP, nullable=False, server_default=func.now())
    updatedAt = Column("updated_at", TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())

    brand = relationship("Brand", back_populates="approvals")
