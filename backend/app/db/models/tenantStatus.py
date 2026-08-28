# Owner: mousamdas156@gmail.com
from datetime import datetime

from sqlalchemy import DateTime, SmallInteger, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


# --------------------------------------------------------------------------------
# TenantStatus Model
# Represents the active/suspended/pending status of a tenant's plan subscription.
# Uses 'Base' instead of 'BaseUUID' because the PK is an auto-incrementing integer (id).
# --------------------------------------------------------------------------------
class TenantStatus(Base):
    __tablename__ = "tenant_status"

    # id: SmallInteger primary key (e.g. 1 for ACTIVE, 2 for SUSPENDED)
    id: Mapped[int] = mapped_column(
        SmallInteger,
        primary_key=True,
        autoincrement=True,
    )

    # statusName: Name of status (e.g. 'ACTIVE', 'SUSPENDED', 'PENDING_VERIFICATION')
    statusName: Mapped[str] = mapped_column(
        "status_name",
        String(50),
        unique=True,
        nullable=False,
    )

    # statusDescription: Optional description of what this status implies
    statusDescription: Mapped[str | None] = mapped_column(
        "status_description",
        String(255),
        nullable=True,
    )

    # createdAt: Timestamp when this status definition was created
    createdAt: Mapped[datetime] = mapped_column(
        "created_at",
        DateTime(timezone=True),
        server_default=func.now(),
    )

    # tenantMappings: One-to-many relationship tracking which active mappings are in this status
    tenantMappings = relationship(
        "TenantPlanMapping",
        back_populates="status",
    )