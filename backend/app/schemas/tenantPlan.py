# Owner: mousamdas156@gmail.com
"""
================================================================================
SCHEMAS: Tenant Active Subscription Assignments
================================================================================
This file defines Pydantic schemas validating subscription plans mappings assigned 
to specific active SaaS tenants.
"""

import uuid
from datetime import date, datetime
from pydantic import BaseModel, Field
from app.schemas.subscriptionPlan import PlanReadCompact


class TenantPlanAssign(BaseModel):
    """
    Schema used when assigning a subscription plan level to a tenant.
    """
    # The subscription plan tier UUID to assign
    planId: uuid.UUID = Field(..., description="Target plan configuration model identifier")
    
    # Activation date for billing limits to take effect
    planStartDate: date = Field(..., description="Date the plan tier begins validation rules")
    
    # Expiration date of the subscription mapping (None if infinite ongoing)
    planEndDate: date | None = Field(None, description="Expiration date limit of the current assignment")
    
    # Toggle to decide if billing renewals should trigger automatically
    autoRenew: bool = Field(True, description="Enables or disables automatic subscription renewals")


class TenantPlanUpdate(BaseModel):
    """
    Schema used when modifying details of an active subscription mapping (e.g. tier upgrade/downgrade).
    """
    planId: uuid.UUID | None = Field(None, description="Updated target plan configuration ID")
    planEndDate: date | None = Field(None, description="Updated end date for the plan mapping")
    autoRenew: bool | None = Field(None, description="Toggle auto renew billing status")
    
    # Audit comment explanation detailing why the tenant plan mapping was changed
    changeReason: str | None = Field(None, max_length=255, description="Audit reason explanation log for modifications")


class TenantPlanRead(BaseModel):
    """
    Schema used to serialize and read details of active subscription assignments.
    """
    # Unique record mapping ID
    id: uuid.UUID
    
    # Target tenant owner ID
    tenantId: uuid.UUID
    
    # Currently assigned plan configuration ID
    planId: uuid.UUID
    
    planStartDate: date
    planEndDate: date | None = None
    planUpdateAt: datetime | None = None
    autoRenew: bool
    planChange: bool
    changeReason: str | None = None
    statusId: int | None = None
    statusUpdateAt: datetime | None = None
    statusUpdateBy: uuid.UUID | None = None
    
    # Details of the referenced subscription plan tier configuration
    plan: PlanReadCompact | None = None

    # ORM settings integration
    model_config = {"from_attributes": True}
