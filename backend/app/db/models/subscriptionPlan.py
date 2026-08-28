# Owner: mousamdas156@gmail.com
import uuid
from decimal import Decimal

from sqlalchemy import Boolean, CheckConstraint, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import BaseModelCreated as BaseModel


# --------------------------------------------------------------------------------
# SubscriptionPlan Model
# Represents a SaaS billing tier (e.g., STARTER, PREMIUM) with custom pricing.
# Uses 'BaseModel' to automatically include a 'createdAt' timestamp.
# --------------------------------------------------------------------------------
class SubscriptionPlan(BaseModel):
    __tablename__ = "subscription_plans"

    # check_monthly_price_positive: Monthly price cannot be negative.
    # check_transaction_commission_percent: Commission must be between 0% and 100%.
    __table_args__ = (
        CheckConstraint(
            "monthlyPrice >= 0",
            name="ck_monthly_price_positive",
        ),
        CheckConstraint(
            "transactionCommissionPercent >= 0 AND transactionCommissionPercent <= 100",
            name="ck_transaction_commission_percent",
        ),
    )

    # planCode: Unique system code for the plan (e.g. 'FREE_TIER', 'STARTER')
    planCode: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    # planName: User-friendly plan name (e.g. 'Premium Growth Plan')
    planName: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    # monthlyPrice: Flat recurrent fee charged to the tenant per month
    monthlyPrice: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    # transactionCommissionPercent: Percentage commission charged on every order transaction
    transactionCommissionPercent: Mapped[Decimal] = mapped_column(
        Numeric(5, 2),
        nullable=False,
    )

    # isActive: Toggle to enable/disable subscription enrollment for new tenants
    isActive: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    # features: Relationship mapping to the specific feature keys/limits allowed in this plan
    # cascade="all, delete-orphan" removes all nested features when plan is deleted.
    features = relationship(
        "PlanFeature",
        back_populates="plan",
        cascade="all, delete-orphan",
    )

    # tenantMappings: Track which active tenants are currently mapped/subscribed to this plan
    tenantMappings = relationship(
        "TenantPlanMapping",
        back_populates="plan",
    )