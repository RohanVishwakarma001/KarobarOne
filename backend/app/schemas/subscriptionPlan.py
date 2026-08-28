# Owner: mousamdas156@gmail.com
"""
================================================================================
SCHEMAS: Subscription Plan Packages & Tiers
================================================================================
This file is used to define Pydantic validation schemas for subscription plans. 
It governs billing tiers (e.g. STARTER, PREMIUM) and controls transaction fees 
and pricing attributes.
"""

import uuid
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field
from app.schemas.planFeature import FeatureRead


class PlanCreate(BaseModel):
    """
    Schema used when creating a new subscription plan package level.
    """
    # System code for the plan tier (e.g., 'FREE_TIER', 'ENTERPRISE_GOLD')
    planCode: str = Field(..., max_length=50, description="Unique code key for the subscription level")
    
    # User facing display name (e.g. 'Premium Growth Plan')
    planName: str = Field(..., max_length=100, description="Descriptive display name of the plan tier")
    
    # Recurring monthly flat subscription fee
    monthlyPrice: Decimal = Field(..., ge=0, decimal_places=2, description="Flat monthly recurrence charge fee")
    
    # Percentage commission fee charged on every order transaction
    transactionCommissionPercent: Decimal = Field(
        ..., ge=0, le=100, decimal_places=2, description="Commission percentage rate per transaction"
    )
    
    # Toggle to enable/disable subscriptions to this plan level
    isActive: bool = Field(True, description="Enables or disables signups to this plan")


class PlanUpdate(BaseModel):
    """
    Schema used to update parameters of an existing plan level configuration.
    """
    planName: str | None = Field(None, max_length=100, description="Updated display name")
    monthlyPrice: Decimal | None = Field(None, ge=0, decimal_places=2, description="Updated monthly flat fee")
    transactionCommissionPercent: Decimal | None = Field(
        None, ge=0, le=100, decimal_places=2, description="Updated transaction commission percentage"
    )
    isActive: bool | None = Field(None, description="Change signup active status")


class PlanRead(BaseModel):
    """
    Schema representing the complete plan configuration including all feature capabilities.
    """
    # Database UUID PK ID for this subscription tier
    id: uuid.UUID
    
    planCode: str
    planName: str
    monthlyPrice: Decimal
    transactionCommissionPercent: Decimal
    isActive: bool
    
    # Nested list of feature permission boundaries allowed under this subscription level
    features: list[FeatureRead] = []
    
    # Creation timestamp
    createdAt: datetime

    # ORM settings integration
    model_config = {"from_attributes": True}


class PlanReadCompact(BaseModel):
    """
    Compact version of the plan details without including nested feature details.
    Optimizes serialization size for listing endpoints.
    """
    id: uuid.UUID
    planCode: str
    planName: str
    monthlyPrice: Decimal
    transactionCommissionPercent: Decimal
    isActive: bool
    createdAt: datetime

    # ORM configuration integration
    model_config = {"from_attributes": True}
