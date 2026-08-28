# Owner: mousamdas156@gmail.com
import uuid

from typing import Any
from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import BaseModelCreated as BaseModel


# --------------------------------------------------------------------------------
# PlanFeature Model
# Defines a specific permission or resource limit associated with a subscription plan.
# Uses 'BaseModel' to automatically include a 'createdAt' timestamp.
# --------------------------------------------------------------------------------
class PlanFeature(BaseModel):
    __tablename__ = "plan_features"

    # UniqueConstraint: Prevents having duplicate featureCodes under the same planId.
    __table_args__ = (
        UniqueConstraint(
            "planId",
            "featureCode",
            name="uq_plan_feature_code",
        ),
    )

    # planId: Foreign Key linking to the parent subscription plan.
    # ondelete="CASCADE" deletes features automatically when the parent plan is deleted.
    planId: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "subscription_plans.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    # featureName: User-friendly name of the feature (e.g. 'Max Products')
    featureName: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    # featureCode: Unique code used to check authorization programmatically (e.g. 'max_products')
    featureCode: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    # featureValue: Value of the configuration limit (e.g., {"limit": 100}, true/false, or 50)
    # Stored using PostgreSQL JSONB format for maximum flexibility and performance.
    featureValue: Mapped[Any | None] = mapped_column(
        JSONB,
        nullable=True,
    )

    # plan: Back-reference to the parent SubscriptionPlan object.
    plan = relationship(
        "SubscriptionPlan",
        back_populates="features",
    )