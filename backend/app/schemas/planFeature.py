# Owner: mousamdas156@gmail.com
"""
================================================================================
SCHEMAS: Plan Feature Definition Validations
================================================================================
This file is used to define Pydantic schemas for plan features. It validates 
and structures the specific limits or permissions (e.g. max_products = 100) 
assigned to subscription plans.
"""

import uuid
from datetime import datetime
from typing import Any
from pydantic import BaseModel, Field


class FeatureCreate(BaseModel):
    """
    Schema used when creating a new feature capability configuration for a plan.
    """
    # Name of the feature (e.g., 'Max Products', 'SMS Integration')
    featureName: str = Field(..., max_length=100, description="Display name of the feature")
    
    # Code key used in the code to perform feature authorization checks (e.g., 'max_products')
    featureCode: str = Field(..., max_length=50, description="System key code for validation checks")
    
    # Value limit of the configuration (can be an integer like 100, a boolean, or JSON configs)
    featureValue: Any | None = Field(None, description="Detailed settings value (boolean, integer, or custom JSON)")


class FeatureUpdate(BaseModel):
    """
    Schema used to modify an existing plan feature's options.
    """
    featureName: str | None = Field(None, max_length=100, description="Updated display name")
    featureCode: str | None = Field(None, max_length=50, description="Updated system key code")
    featureValue: Any | None = Field(None, description="Updated settings limit value")


class FeatureRead(BaseModel):
    """
    Schema used to serialize and return the plan feature details in JSON format.
    """
    # ID of the plan feature configuration record
    id: uuid.UUID
    
    # ID of the parent subscription plan tier
    planId: uuid.UUID
    
    featureName: str
    featureCode: str
    featureValue: Any | None = None
    
    # When this feature config was first defined
    createdAt: datetime

    # Enable ORM attributes compatibility
    model_config = {"from_attributes": True}
