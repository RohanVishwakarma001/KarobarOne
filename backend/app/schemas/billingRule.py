# Owner: mousamdas156@gmail.com
"""
Pydantic schemas for Plan Billing Rules.
"""
# Import uuid for validating UUID fields
import uuid
# Import datetime for timestamp fields
from datetime import datetime
# Import Decimal for numeric representations
from decimal import Decimal
# Import Pydantic base classes for data schemas
from pydantic import BaseModel, Field


class BillingRuleCreate(BaseModel):
    """
    Schema for validating BillingRule creation payloads.
    """
    ruleName: str = Field(..., max_length=100)
    ruleCode: str = Field(..., max_length=50)
    ruleType: str = Field(default="PERCENTAGE", max_length=20)
    ruleValue: Decimal = Field(default=Decimal("0.00"), ge=0)
    isActive: bool = Field(default=True)
    appliesTo: str = Field(default="ORDER", max_length=50)


class BillingRuleUpdate(BaseModel):
    """
    Schema for validating BillingRule partial update/patch payloads.
    """
    ruleName: str | None = Field(default=None, max_length=100)
    ruleCode: str | None = Field(default=None, max_length=50)
    ruleType: str | None = Field(default=None, max_length=20)
    ruleValue: Decimal | None = Field(default=None, ge=0)
    isActive: bool | None = Field(default=None)
    appliesTo: str | None = Field(default=None, max_length=50)


class BillingRuleRead(BaseModel):
    """
    Schema representing serialized BillingRule responses.
    """
    id: uuid.UUID
    planId: uuid.UUID
    ruleName: str
    ruleCode: str
    ruleType: str
    ruleValue: Decimal
    isActive: bool
    appliesTo: str
    createdAt: datetime
    model_config = {"from_attributes": True}
