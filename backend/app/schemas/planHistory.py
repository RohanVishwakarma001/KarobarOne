# Owner: mousamdas156@gmail.com
"""
================================================================================
SCHEMAS: Subscription Plan History Audit Logs
================================================================================
This file defines Pydantic schemas for the audit log history of tenant plans. 
It ensures historical transitions (upgrades, downgrades, and cancellations) 
can be serialized safely when querying audit records.
"""

import uuid
from datetime import datetime
from pydantic import BaseModel, Field
from app.schemas.subscriptionPlan import PlanReadCompact


class PlanHistoryRead(BaseModel):
    """
    Schema representing a read-only subscription plan history entry.
    Used to show who changed what plan mapping, when, and for what reason.
    """
    # Unique audit history record ID
    id: uuid.UUID
    
    # ID of the tenant whose subscription changed
    tenantId: uuid.UUID
    
    # Previous plan ID (None if first time subscription)
    oldPlanId: uuid.UUID | None = Field(None, description="Previous plan identifier")
    
    # Newly selected plan ID (None if fully canceled)
    newPlanId: uuid.UUID | None = Field(None, description="New subscription plan identifier")
    
    # Staff / admin user UUID who triggered the modification
    changedBy: uuid.UUID | None = Field(None, description="UUID of user/staff who performed change")
    
    # Description of why the plan status was modified (e.g. 'Upgrade requests')
    changeReason: str | None = Field(None, description="Reason stated for the transition")
    
    # Log timestamp of the state transition
    changedAt: datetime
    
    # Details of the older plan (compact version)
    oldPlan: PlanReadCompact | None = None
    
    # Details of the new plan (compact version)
    newPlan: PlanReadCompact | None = None

    # ORM compatibility
    model_config = {"from_attributes": True}
