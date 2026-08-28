# Owner: mousamdas156@gmail.com
"""
================================================================================
SOCIAL PLATFORM MODEL
================================================================================
Yeh file available social platforms (jaise Instagram, Facebook, YouTube) ki master details store karti hai.
This model maps to the 'social_platforms' table, containing platform metadata like
base URLs and icons.

Why it is used:
- Acts as a master list of supported platforms.
- Stores the icon images and base patterns so individual stores don't duplicate them.
================================================================================
"""

import uuid
from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import BaseModelCreated as BaseModel


class SocialPlatform(BaseModel):
    """
    ORM Model representing a supported social media platform (e.g. Twitter, YouTube).
    Inherits from BaseModel, getting 'id' and 'createdAt'.
    """
    __tablename__ = "social_platforms"

    # Unique code name identifying the platform (e.g., 'INSTAGRAM', 'FACEBOOK')
    platformCode: Mapped[str] = mapped_column(
        "platform_code",
        String(50),
        unique=True,
        nullable=False,
    )

    # Human-readable name of the platform (e.g. "Instagram", "Facebook")
    platformName: Mapped[str] = mapped_column(
        "platform_name",
        String(100),
        nullable=False,
    )

    # Base URL website path of the platform (e.g., "https://instagram.com/")
    baseUrl: Mapped[str | None] = mapped_column(
        "base_url",
        String(255),
        nullable=True,
    )

    # Foreign key referencing the platform's official logo icon in media files
    iconMediaId: Mapped[uuid.UUID | None] = mapped_column(
        "icon_media_id",
        UUID(as_uuid=True),
        ForeignKey("media_files.id"),
        nullable=True,
    )

    # Flag to toggle whether this platform is currently active and selectable
    isActive: Mapped[bool] = mapped_column(
        "is_active",
        Boolean,
        default=True,
        nullable=False,
    )

    # ── Relationships ──────────────────────────────────────────────────
    # Cascade link to all store-specific social link mapping records.
    # If a platform is deleted, all associated links are cascade deleted ('delete-orphan').
    socialLinks = relationship(
        "SocialLink",
        back_populates="platform",
        cascade="all, delete-orphan",
    )
