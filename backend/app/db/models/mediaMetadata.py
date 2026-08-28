# Owner: mousamdas156@gmail.com
"""
================================================================================
MEDIA METADATA ORM MODEL (mediaMetadata.py)
================================================================================
Why this file is used:
- This file defines the `MediaMetadata` database model mapping to the 'media_metadata' table.
- It stores user-defined or generated semantic details for media files, such as 
  ALT text for accessibility, captions, SEO friendly titles, slugs, and long descriptions.
================================================================================
"""

# Standard library import for UUID generation
import uuid

# Third-party SQLAlchemy model fields and relationship mapping utilities
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Custom base model that provides ID, createdAt, and updatedAt fields
from app.db.base import BaseModelWithUpdate


class MediaMetadata(BaseModelWithUpdate):
    """
    ORM Model representing metadata attributes of an uploaded asset.
    Inherits primary key UUID and timestamps from BaseModelWithUpdate.
    """
    __tablename__ = "media_metadata"

    # Reference to the parent MediaFile (One-to-One relationship)
    mediaFileId: Mapped[uuid.UUID] = mapped_column(
        "media_file_id",
        UUID(as_uuid=True),
        ForeignKey("media_files.id"),
        unique=True,
        nullable=False,
    )

    # Accessibility alternative text (ALT attribute)
    altText: Mapped[str | None] = mapped_column(
        "alt_text",
        String(255),
        nullable=True,
    )

    # Display caption associated with the image/document
    caption: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    # Descriptive header/title of the media asset
    title: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    # Long text description of the media asset
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # URL-friendly slug referencing this media asset
    slug: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    # ── ORM Relationships ──────────────────────────────────────────────────
    
    # Bidirectional relationship back to parent MediaFile
    mediaFile = relationship(
        "MediaFile",
        back_populates="metadataRecord",
    )
