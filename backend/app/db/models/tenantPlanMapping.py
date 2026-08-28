# Owner: mousamdas156@gmail.com
import uuid
from datetime import date, datetime

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    String,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import BaseUUID


# --------------------------------------------------------------------------------
# TenantPlanMapping Model
# Stores the active subscription assignment mapping for a tenant.
# Inherits BaseUUID (primary key is UUID, no automatic default timestamps).
# --------------------------------------------------------------------------------
class TenantPlanMapping(BaseUUID):
    __tablename__ = "tenant_plan_mapping"

    # UniqueConstraint: Restricts a tenant to having exactly ONE active plan mapping.
    __table_args__ = (
        UniqueConstraint(
            "tenant_id",
            name="uq_tenant_active_plan",
        ),
    )

    # tenantId: The tenant associated with this subscription mapping.
    # ondelete="CASCADE" ensures mappings are removed automatically when a tenant is deleted.
    tenantId: Mapped[uuid.UUID] = mapped_column(
        "tenant_id",
        UUID(as_uuid=True),
        ForeignKey(
            "tenants_details.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    # planId: Reference to the currently active SubscriptionPlan.
    planId: Mapped[uuid.UUID] = mapped_column(
        "plan_id",
        UUID(as_uuid=True),
        ForeignKey(
            "subscription_plans.id",
        ),
        nullable=False,
    )

    # planStartDate: Activation date of the subscription
    planStartDate: Mapped[date] = mapped_column(
        "plan_start_date",
        Date,
        nullable=False,
    )

    # planEndDate: Expiration or cancellation date (null means infinite / ongoing)
    planEndDate: Mapped[date | None] = mapped_column(
        "plan_end_date",
        Date,
        nullable=True,
    )

    # planUpdateAt: Timestamp when this mapping was last modified (e.g. upgraded or auto-renew toggled)
    planUpdateAt: Mapped[datetime | None] = mapped_column(
        "plan_update_at",
        DateTime(timezone=True),
        nullable=True,
    )

    # autoRenew: If true, billing continues and renewals process automatically
    autoRenew: Mapped[bool] = mapped_column(
        "auto_renew",
        Boolean,
        default=True,
        nullable=False,
    )

    # planChange: True if the tenant's plan has been modified from its original tier
    planChange: Mapped[bool] = mapped_column(
        "plan_change",
        Boolean,
        default=False,
        nullable=False,
    )

    # changeReason: Optional textual reason for plan upgrades, downgrades, or cancellations
    changeReason: Mapped[str | None] = mapped_column(
        "change_reason",
        String(255),
        nullable=True,
    )

    # statusId: Foreign key pointing to TenantStatus (e.g., 1 for ACTIVE)
    statusId: Mapped[int] = mapped_column(
        "status_id",
        ForeignKey("tenant_status.id"),
        nullable=False,
    )

    # statusUpdateAt: When the billing status was last modified
    statusUpdateAt: Mapped[datetime | None] = mapped_column(
        "status_update_at",
        DateTime(timezone=True),
        nullable=True,
    )

    # statusUpdateBy: UUID tracking the staff member who changed the status manually (optional)
    statusUpdateBy: Mapped[uuid.UUID | None] = mapped_column(
        "status_update_by",
        UUID(as_uuid=True),
        nullable=True,
    )

    # tenant: Back-reference to the mapped Tenant object (1-to-1)
    tenant = relationship(
        "Tenant",
        back_populates="planMapping",
    )

    # plan: Back-reference to the SubscriptionPlan object
    plan = relationship(
        "SubscriptionPlan",
        back_populates="tenantMappings",
    )

    # status: Back-reference to the TenantStatus object
    status = relationship(
        "TenantStatus",
        back_populates="tenantMappings",
    )