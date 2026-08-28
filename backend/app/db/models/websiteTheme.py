# Owner: mousamdas156@gmail.com
"""
================================================================================
WEBSITE THEME MODEL
================================================================================
Yeh file website builder ke available design themes aur styles ko store karti hai.
This model maps to the 'website_themes' table, containing configuration blueprints 
for site themes.

Why it is used:
- Provides predefined visual templates (fonts, colors, structure) that merchants can 
  apply to their storefronts.
================================================================================
"""

import uuid
from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import BaseModelCreated as BaseModel


class WebsiteTheme(BaseModel):
    """
    ORM Model representing a theme layout preset.
    Inherits UUID and createdAt.
    """
    __tablename__ = "website_themes"

    # Human-readable name of the theme (e.g., "Vintage Pastel")
    themeName: Mapped[str] = mapped_column(
        "theme_name",
        String(100),
        nullable=False,
    )

    # Unique code name of the theme used internally (e.g., "VINTAGE_PASTEL")
    themeCode: Mapped[str] = mapped_column(
        "theme_code",
        String(50),
        unique=True,
        nullable=False,
    )

    # Foreign key referencing a preview image of the theme in media files
    previewImageId: Mapped[uuid.UUID | None] = mapped_column(
        "preview_image_id",
        UUID(as_uuid=True),
        ForeignKey("media_files.id"),
        nullable=True,
    )

    # JSONSchema/dictionary detailing the custom options (like allowable fonts, primary colors, layouts)
    configSchema: Mapped[dict | list | None] = mapped_column(
        "config_schema",
        JSONB,
        nullable=True,
    )

    # Flag indicating whether this theme layout is available for selection
    isActive: Mapped[bool] = mapped_column(
        "is_active",
        Boolean,
        default=True,
        nullable=False,
    )
