import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import BaseModelCreated


class WebsiteSection(BaseModelCreated):
    __tablename__ = "website_sections"

    websiteId: Mapped[uuid.UUID] = mapped_column(
        "website_id",
        UUID(as_uuid=True),
        ForeignKey("website.id", ondelete="CASCADE"),
        nullable=False,
    )

    sectionName: Mapped[str] = mapped_column(
        "section_name",
        String(100),
        nullable=False,
    )

    content: Mapped[dict | list | None] = mapped_column(
        "content",
        JSONB,
        nullable=True,
    )
