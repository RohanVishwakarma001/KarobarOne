import uuid
from datetime import datetime

from sqlalchemy import DateTime, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import BaseModelCreated


class Website(BaseModelCreated):
    __tablename__ = "website"

    tenantId: Mapped[uuid.UUID] = mapped_column(
        "tenant_id",
        UUID(as_uuid=True),
        nullable=False,
    )

    companyName: Mapped[str] = mapped_column(
        "company_name",
        String(255),
        nullable=False,
    )

    slug: Mapped[str] = mapped_column(
        "slug",
        String(255),
        unique=True,
        nullable=False,
    )

    businessType: Mapped[str] = mapped_column(
        "business_type",
        String(100),
        nullable=False,
    )

    theme: Mapped[str | None] = mapped_column(
        "theme",
        String(100),
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        "status",
        String(30),
        nullable=False,
        default="DRAFT",
    )

    plan: Mapped[str] = mapped_column(
        "plan",
        String(30),
        nullable=False,
        default="FREE",
    )

    domain: Mapped[str | None] = mapped_column(
        "domain",
        String(255),
        nullable=True,
    )
