# Owner: mousamdas156@gmail.com

import uuid

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import BaseModelWithUpdate


class WebsiteAIContent(BaseModelWithUpdate):
    """
    Stores AI-generated website content for a store.
    """

    __tablename__ = "website_ai_contents"

    storeId: Mapped[uuid.UUID] = mapped_column(
        "store_id",
        UUID(as_uuid=True),
        ForeignKey("stores.id", ondelete="CASCADE"),
        nullable=False,
    )

    contentType: Mapped[str] = mapped_column(
        "content_type",
        String(50),
        nullable=False,
    )

    content: Mapped[str | None] = mapped_column(
        "content",
        Text,
        nullable=True,
    )

    contentMetadata: Mapped[dict | list | None] = mapped_column(
        "metadata",
        JSONB,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        "status",
        String(30),
        nullable=False,
        default="GENERATED",
    )

    store = relationship(
        "Store",
        back_populates="aiContents",
    )
