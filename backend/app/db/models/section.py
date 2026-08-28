# Owner: mousamdas156@gmail.com
"""
================================================================================
SECTION MODEL
================================================================================
Yeh file website pages ke sections (jaise Hero banner, About us, Contact form) ko manage karti hai.
This model maps to the 'sections' table, representing UI components of a storefront.

Why it is used:
- Allows merchants to dynamically construct website page layouts by adding, 
  ordering, and configuring different block types.
================================================================================
"""

import uuid
from sqlalchemy import Boolean, CheckConstraint, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import BaseModelWithUpdate


class Section(BaseModelWithUpdate):
    """
    ORM Model representing a visual section block on a store's website.
    Inherits UUID and full timestamps (created_at, updated_at).
    """
    __tablename__ = "sections"

    # ── Database Constraints ──────────────────────────────────────────
    __table_args__ = (
        # Prevent a store from having multiple sections with the same semantic code (e.g. two HERO sections)
        UniqueConstraint(
            "store_id",
            "section_code",
            name="uq_sections_store_section_code",
        ),
        # Prevent two sections in the same store from sharing the same visual sort order position
        UniqueConstraint(
            "store_id",
            "sort_order",
            name="uq_sections_store_sort_order",
        ),
        # Validate that the section type falls within the allowed UI component types
        CheckConstraint(
            "section_type IN ('HERO', 'ABOUT', 'USP', 'PRODUCTS', 'SERVICES', 'BLOGS', 'CONTACT')",
            name="ck_sections_section_type",
        ),
    )

    # Foreign key referencing the parent Store
    storeId: Mapped[uuid.UUID] = mapped_column(
        "store_id",
        UUID(as_uuid=True),
        ForeignKey("stores.id"),
        nullable=False,
    )

    # Unique code name of the section block (e.g., 'BANNER_MAIN')
    sectionCode: Mapped[str] = mapped_column(
        "section_code",
        String(50),
        nullable=False,
    )

    # Display name of the section block shown in the editor (e.g., "Main Header slider")
    sectionName: Mapped[str] = mapped_column(
        "section_name",
        String(100),
        nullable=False,
    )

    # Semantic type of the section layout (must match the check constraint list)
    sectionType: Mapped[str] = mapped_column(
        "section_type",
        String(50),
        nullable=False,
    )

    # Sequence number determining where this section renders on the page (lower numbers display first)
    sortOrder: Mapped[int] = mapped_column(
        "sort_order",
        Integer,
        nullable=False,
    )

    # Flag to hide/show the section block on the live website
    isActive: Mapped[bool] = mapped_column(
        "is_active",
        Boolean,
        default=True,
        nullable=False,
    )

    # Flexible JSON structure storing component-specific configurations (titles, button links, text, cards)
    configData: Mapped[dict | list | None] = mapped_column(
        "config_data",
        JSONB,
        nullable=True,
    )

    # ── Relationships ──────────────────────────────────────────────────
    # Bidirectional back-populates relationship link back to the parent Store model
    store = relationship("Store", back_populates="sections")

