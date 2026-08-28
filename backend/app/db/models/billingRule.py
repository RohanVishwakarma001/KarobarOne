# Owner: mousamdas156@gmail.com
# ================================================================================
# FILE: db/models/billingRule.py — Billing Rule Database Model
# ================================================================================
# Why this file is used:
#   - Houses rules for commission calculations and transaction flat fees per billing plan.
#
# What components are inside:
#   - BillingRule (SQLAlchemy model class)
# ================================================================================
# Import uuid for validating UUID fields
import uuid
# Import Decimal for numeric representations
from decimal import Decimal

# Import column types and constraints from SQLAlchemy
from sqlalchemy import (
    Boolean,
    ForeignKey,
    Numeric,
    String,
    UniqueConstraint,
)
# Import Postgres-specific UUID column type
from sqlalchemy.dialects.postgresql import UUID
# Import ORM mappings and relationships
from sqlalchemy.orm import Mapped, mapped_column, relationship
# Import Base Model Stub
from app.db.base import BaseModelCreated as BaseModel


class BillingRule(BaseModel):
    """
    BillingRule database entity.
    Stores pricing and calculation criteria associated with individual subscription plans.
    """
    __tablename__ = "billing_rules"

    # Unique constraint ensuring only one specific rule code is mapped per plan
    __table_args__ = (
        UniqueConstraint("planId", "ruleCode", name="uq_plan_billing_rule_code"),
    )

    # Link to the associated Subscription Plan tier
    planId: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("subscription_plans.id", ondelete="CASCADE"),
        nullable=False,
    )

    # Human-readable descriptive name of the billing rule
    ruleName: Mapped[str] = mapped_column(String(100), nullable=False)
    # Programmatic identifier code of the rule (e.g. 'commission_percentage', 'commission_flat_fee')
    ruleCode: Mapped[str] = mapped_column(String(50), nullable=False)
    # Type classification of rule values (e.g. 'COMMISSION', 'FLAT_FEE', 'PERCENTAGE')
    ruleType: Mapped[str] = mapped_column(String(20), default="PERCENTAGE", server_default="PERCENTAGE", nullable=False)
    # Numeric value criteria used for processing the rule (e.g. commission rate or flat price)
    ruleValue: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0.00"), server_default="0.00", nullable=False)
    # Flag to enable/disable rule applicability at runtime
    isActive: Mapped[bool] = mapped_column(Boolean, default=True, server_default="true", nullable=False)
    # Scope of applicability for the rule (e.g. applied on 'ORDER' transactions)
    appliesTo: Mapped[str] = mapped_column(String(50), default="ORDER", server_default="ORDER", nullable=False)

    # Relationship linking back to the parent SubscriptionPlan
    plan = relationship("SubscriptionPlan")
