# Owner: mousamdas156@gmail.com
"""
================================================================================
SOCIAL LINK MODEL
================================================================================
Yeh file dukaano ke social media accounts (Instagram, Facebook handles) ko connect karti hai.
This model maps to the 'social_links' table, acting as a junction entity that maps
a Store to a specific SocialPlatform along with their profile URL.

Why it is used:
- Stores the social media links of a store so they can be rendered on the website footer.
- Ensures a store doesn't map multiple handles for the same social platform.
================================================================================
"""

import uuid
from sqlalchemy import Boolean, ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import BaseModelCreated as BaseModel


class SocialLink(BaseModel):
    """
    ORM Model representing a store's specific social media handle.
    Inherits from BaseModel, getting 'id' and 'createdAt'.
    """
    __tablename__ = "social_links"

    # ── Database Constraints ──────────────────────────────────────────
    __table_args__ = (
        # Ensure a store has at most one social link mapping per social platform (e.g. exactly one Instagram link)
        UniqueConstraint(
            "store_id",
            "platform_id",
            name="uq_social_links_store_platform",
        ),
    )

    # Foreign key referencing the parent Store
    storeId: Mapped[uuid.UUID] = mapped_column(
        "store_id",
        UUID(as_uuid=True),
        ForeignKey("stores.id"),
        nullable=False,
    )

    # Foreign key referencing the targeted Social Platform
    platformId: Mapped[uuid.UUID] = mapped_column(
        "platform_id",
        UUID(as_uuid=True),
        ForeignKey("social_platforms.id"),
        nullable=False,
    )

    # Complete URL link to the profile (e.g., "https://instagram.com/mybrand")
    profileUrl: Mapped[str] = mapped_column(
        "profile_url",
        String(255),
        nullable=False,
    )

    # Flag to toggle rendering of this social link on the frontend website
    isActive: Mapped[bool] = mapped_column(
        "is_active",
        Boolean,
        default=True,
        nullable=False,
    )

    # ── Relationships ──────────────────────────────────────────────────
    # Link back to the parent Store model
    store = relationship("Store", back_populates="socialLinks")
    # Link to the shared SocialPlatform metadata model
    platform = relationship("SocialPlatform", back_populates="socialLinks")
