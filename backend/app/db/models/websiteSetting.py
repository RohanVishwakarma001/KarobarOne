# Owner: mousamdas156@gmail.com

import uuid

from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import BaseModelWithUpdate


class WebsiteSetting(BaseModelWithUpdate):
    """
    Stores configurable settings for a store website.
    """

    __tablename__ = "website_settings"

    storeId: Mapped[uuid.UUID] = mapped_column(
        "store_id",
        UUID(as_uuid=True),
        ForeignKey("stores.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    siteTitle: Mapped[str | None] = mapped_column(
        "site_title",
        String(150),
        nullable=True,
    )

    siteDescription: Mapped[str | None] = mapped_column(
        "site_description",
        Text,
        nullable=True,
    )

    faviconMediaId: Mapped[uuid.UUID | None] = mapped_column(
        "favicon_media_id",
        UUID(as_uuid=True),
        ForeignKey("media_files.id", ondelete="SET NULL"),
        nullable=True,
    )

    maintenanceMode: Mapped[bool] = mapped_column(
        "maintenance_mode",
        Boolean,
        default=False,
        nullable=False,
    )

    isPublic: Mapped[bool] = mapped_column(
        "is_public",
        Boolean,
        default=False,
        nullable=False,
    )

    store = relationship(
        "Store",
        back_populates="websiteSettings",
    )
