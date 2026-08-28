# Owner: mousamdas156@gmail.com

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import BaseModelCreated


class WebsitePublishLog(BaseModelCreated):
    """
    Stores the history of website publish actions.
    """

    __tablename__ = "website_publish_logs"

    storeId: Mapped[uuid.UUID] = mapped_column(
        "store_id",
        UUID(as_uuid=True),
        ForeignKey("stores.id", ondelete="CASCADE"),
        nullable=False,
    )

    deploymentId: Mapped[uuid.UUID | None] = mapped_column(
        "deployment_id",
        UUID(as_uuid=True),
        ForeignKey("website_deployments.id", ondelete="SET NULL"),
        nullable=True,
    )

    action: Mapped[str] = mapped_column(
        "action",
        String(30),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        "status",
        String(30),
        nullable=False,
    )

    version: Mapped[str | None] = mapped_column(
        "version",
        String(100),
        nullable=True,
    )

    message: Mapped[str | None] = mapped_column(
        "message",
        Text,
        nullable=True,
    )

    publishedAt: Mapped[datetime | None] = mapped_column(
        "published_at",
        DateTime(timezone=True),
        nullable=True,
    )

    store = relationship(
        "Store",
        back_populates="publishLogs",
    )

    deployment = relationship(
        "WebsiteDeployment",
    )
