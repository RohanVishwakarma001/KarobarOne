import uuid

from sqlalchemy import ForeignKey, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import BaseModelCreated


class WebsiteMedia(BaseModelCreated):
    __tablename__ = "website_media"

    websiteId: Mapped[uuid.UUID] = mapped_column(
        "website_id",
        UUID(as_uuid=True),
        ForeignKey("website.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    logo: Mapped[str | None] = mapped_column(
        "logo",
        Text,
        nullable=True,
    )

    banner: Mapped[str | None] = mapped_column(
        "banner",
        Text,
        nullable=True,
    )

    gallery: Mapped[list | None] = mapped_column(
        "gallery",
        JSONB,
        nullable=True,
    )
