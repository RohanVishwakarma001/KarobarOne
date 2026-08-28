# Owner: mousamdas156@gmail.com

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import BaseModelCreated


class WebsiteDeployment(BaseModelCreated):
    """
    Tracks deployment attempts and the current deployment state
    of a store website.
    """

    __tablename__ = "website_deployments"

    storeId: Mapped[uuid.UUID] = mapped_column(
        "store_id",
        UUID(as_uuid=True),
        ForeignKey("stores.id", ondelete="CASCADE"),
        nullable=False,
    )

    deploymentId: Mapped[str | None] = mapped_column(
        "deployment_id",
        String(255),
        nullable=True,
    )

    provider: Mapped[str] = mapped_column(
        "provider",
        String(50),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        "status",
        String(30),
        nullable=False,
        default="PENDING",
    )

    deploymentUrl: Mapped[str | None] = mapped_column(
        "deployment_url",
        Text,
        nullable=True,
    )

    errorMessage: Mapped[str | None] = mapped_column(
        "error_message",
        Text,
        nullable=True,
    )

    startedAt: Mapped[datetime | None] = mapped_column(
        "started_at",
        DateTime(timezone=True),
        nullable=True,
    )

    completedAt: Mapped[datetime | None] = mapped_column(
        "completed_at",
        DateTime(timezone=True),
        nullable=True,
    )

    store = relationship(
        "Store",
        back_populates="deployments",
    )
