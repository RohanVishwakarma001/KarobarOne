# Owner: mousamdas156@gmail.com
"""
================================================================================
MEDIA VARIANT ORM MODEL (mediaVariant.py)
================================================================================
Why this file is used:
- This file defines the `MediaVariant` database model mapping to the 'media_variants' table.
- It stores references to different resized or optimized versions (e.g. mobile,
  tablet, thumbnail sizes) generated from a primary `MediaFile`.
================================================================================
"""

# Standard library import for UUID generation
import uuid

# Third-party SQLAlchemy model fields, constraints, and relationships
from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint, BigInteger
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Custom base model that provides ID and createdAt fields
from app.db.base import BaseModelCreated as BaseModel


class MediaVariant(BaseModel):
    """
    ORM Model representing an optimized child variant (e.g. thumbnail) of a MediaFile.
    Inherits primary key UUID and createdAt timestamp from BaseModel.
    """
    __tablename__ = "media_variants"

    # Enforce uniqueness on the variant name per parent media file
    __table_args__ = (
        UniqueConstraint(
            "media_file_id",
            "variant_name",
            name="uq_media_variants_media_file_id_variant_name",
        ),
    )

    # Reference to the parent MediaFile record
    mediaFileId: Mapped[uuid.UUID] = mapped_column(
        "media_file_id",
        UUID(as_uuid=True),
        ForeignKey("media_files.id"),
        nullable=False,
    )

    # Label key identifying the variant type (e.g., 'thumbnail', 'desktop_compressed')
    variantName: Mapped[str] = mapped_column(
        "variant_name",
        String(50),
        nullable=False,
    )

    # Output width of the variant image in pixels
    width: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    # Output height of the variant image in pixels
    height: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    # Size of the variant file in bytes
    fileSizeBytes: Mapped[int] = mapped_column(
        "file_size_bytes",
        BigInteger,
        nullable=False,
    )

    # Exact storage location path or object key for this variant
    storagePath: Mapped[str] = mapped_column(
        "storage_path",
        String(500),
        nullable=False,
    )

    # Fully qualified URL to access this specific variant publicly
    publicUrl: Mapped[str] = mapped_column(
        "public_url",
        String(1000),
        nullable=False,
    )

    # ── ORM Relationships ──────────────────────────────────────────────────
    
    # Reference back to the parent MediaFile record
    mediaFile = relationship(
        "MediaFile",
        back_populates="variants",
    )
