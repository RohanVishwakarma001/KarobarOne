# Owner: mousamdas156@gmail.com
import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import BaseUUID


# --------------------------------------------------------------------------------
# TenantPlanHistory Model
# Stores an immutable history log of all plan subscription changes (upgrades/downgrades/churn).
# Uses 'BaseUUID' for primary key index representation.
# --------------------------------------------------------------------------------
class TenantPlanHistory(BaseUUID):
    __tablename__ = "tenant_plan_history"

    # tenantId: The tenant associated with this audit entry.
    # ondelete="CASCADE" automatically clears history logs if the parent tenant is deleted.
    tenantId: Mapped[uuid.UUID] = mapped_column(
        "tenant_id",
        UUID(as_uuid=True),
        ForeignKey(
            "tenants_details.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    # oldPlanId: The previous plan ID (nullable, e.g. when subscribing for the first time).
    oldPlanId: Mapped[uuid.UUID | None] = mapped_column(
        "old_plan_id",
        UUID(as_uuid=True),
        ForeignKey("subscription_plans.id"),
        nullable=True,
    )

    # newPlanId: The new subscription plan ID (nullable, e.g. when cancelling subscription).
    newPlanId: Mapped[uuid.UUID | None] = mapped_column(
        "new_plan_id",
        UUID(as_uuid=True),
        ForeignKey("subscription_plans.id"),
        nullable=True,
    )

    # changedBy: UUID of the actor (user/agent) who triggered this change
    changedBy: Mapped[uuid.UUID] = mapped_column(
        "changed_by",
        UUID(as_uuid=True),
        nullable=False,
    )

    # changeReason: Text explanation of the upgrade, downgrade, or cancellation
    changeReason: Mapped[str | None] = mapped_column(
        "change_reason",
        String(255),
        nullable=True,
    )

    # changedAt: Audit timestamp tracked automatically on record creation
    changedAt: Mapped[datetime] = mapped_column(
        "changed_at",
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # tenant: Relationship back to the related Tenant record.
    tenant = relationship(
        "Tenant",
        back_populates="planHistory",
    )

    # oldPlan: Relationship to retrieve old subscription details for comparison.
    oldPlan = relationship(
        "SubscriptionPlan",
        foreign_keys=[oldPlanId],
    )

    # newPlan: Relationship to retrieve new subscription details for comparison.
    newPlan = relationship(
        "SubscriptionPlan",
        foreign_keys=[newPlanId],
    )