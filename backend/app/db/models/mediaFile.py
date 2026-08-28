# Owner: mousamdas156@gmail.com
"""
================================================================================
MEDIA FILE ORM MODEL (mediaFile.py)
================================================================================
Why this file is used:
- This file defines the `MediaFile` database model mapping to the 'media_files' table.
- It stores central metadata for uploaded assets (images, documents, etc.), 
  including storage paths, MIME types, sizes, uploaders, and approval states.
================================================================================
"""

# Standard library imports for UUIDs and timestamps
import uuid
from datetime import datetime

# Third-party SQLAlchemy model elements, constraints, and relationships
from sqlalchemy import Boolean, CheckConstraint, DateTime, ForeignKey, Index, String, BigInteger
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Custom base model that provides ID, createdAt, and updatedAt fields
from app.db.base import BaseModelWithUpdate


class MediaFile(BaseModelWithUpdate):
    """
    ORM Model representing a uploaded file asset.
    Inherits primary key UUID and timestamps from BaseModelWithUpdate.
    """
    __tablename__ = "media_files"

    # Define CHECK constraints and table indexes for performant querying
    __table_args__ = (
        CheckConstraint(
            "approval_status IN ('PENDING', 'APPROVED', 'REJECTED')",
            name="ck_media_files_approval_status",
        ),
        Index("idx_media_files_tenant_id", "tenant_id"),
        Index("idx_media_files_uploaded_by", "uploaded_by"),
        Index("idx_media_files_created_at", "created_at"),
    )

    # Reference to the TenantDetails owner of this media file
    tenantId: Mapped[uuid.UUID] = mapped_column(
        "tenant_id",
        UUID(as_uuid=True),
        ForeignKey("tenants_details.id"),
        nullable=False,
    )

    # Optional virtual folder/bucket prefix name
    folderName: Mapped[str | None] = mapped_column(
        "folder_name",
        String(100),
        nullable=True,
    )

    # Generated filename stored in cloud storage (usually with a suffix)
    fileName: Mapped[str] = mapped_column(
        "file_name",
        String(255),
        nullable=False,
    )

    # Original filename uploaded by the client
    originalFileName: Mapped[str] = mapped_column(
        "original_file_name",
        String(255),
        nullable=False,
    )

    # File format extension (e.g. "png", "jpg")
    fileExtension: Mapped[str] = mapped_column(
        "file_extension",
        String(20),
        nullable=False,
    )

    # Standard Internet media type (MIME type)
    mimeType: Mapped[str] = mapped_column(
        "mime_type",
        String(100),
        nullable=False,
    )

    # File size in bytes
    fileSizeBytes: Mapped[int] = mapped_column(
        "file_size_bytes",
        BigInteger,
        nullable=False,
    )

    # Host provider (e.g. "S3", "LOCAL")
    storageProvider: Mapped[str] = mapped_column(
        "storage_provider",
        String(50),
        nullable=False,
    )

    # Exact storage location path or object key
    storagePath: Mapped[str] = mapped_column(
        "storage_path",
        String(500),
        nullable=False,
    )

    # Fully qualified URL for public rendering
    publicUrl: Mapped[str] = mapped_column(
        "public_url",
        String(1000),
        nullable=False,
    )

    # Unique checksum identifier hash to prevent duplicate uploads
    checksumHash: Mapped[str] = mapped_column(
        "checksum_hash",
        String(128),
        unique=True,
        nullable=False,
    )

    # Current approval status (PENDING, APPROVED, REJECTED)
    approvalStatus: Mapped[str] = mapped_column(
        "approval_status",
        String(20),
        default="PENDING",
        nullable=False,
    )

    # Reference to the user ID who changed approval status
    approvalStatusChangeBy: Mapped[uuid.UUID | None] = mapped_column(
        "approval_status_change_by",
        UUID(as_uuid=True),
        nullable=True,
    )

    # Timestamp when approval status changed
    approvalStatusChangeAt: Mapped[datetime | None] = mapped_column(
        "approval_status_change_at",
        DateTime(timezone=True),
        nullable=True,
    )

    # Reference to the User ID who uploaded the file
    uploadedBy: Mapped[uuid.UUID] = mapped_column(
        "uploaded_by",
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
    )

    # Active flag for soft deletion checks
    isActive: Mapped[bool] = mapped_column(
        "is_active",
        Boolean,
        default=True,
        nullable=False,
    )

    # Soft deletion timestamp
    deletedAt: Mapped[datetime | None] = mapped_column(
        "deleted_at",
        DateTime(timezone=True),
        nullable=True,
    )

    # ── ORM Relationships ──────────────────────────────────────────────────
    
    # Associated variant images (e.g. thumbnails, compressed assets)
    variants = relationship(
        "MediaVariant",
        back_populates="mediaFile",
        cascade="all, delete-orphan",
    )

    # Associated description, caption, and SEO tags
    metadataRecord = relationship(
        "MediaMetadata",
        back_populates="mediaFile",
        uselist=False,
        cascade="all, delete-orphan",
    )

    # Multi-part file upload chunk tracking history
    uploadLogs = relationship(
        "MediaUploadLog",
        back_populates="mediaFile",
        cascade="all, delete-orphan",
    )
