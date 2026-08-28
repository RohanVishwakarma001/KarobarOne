# Owner: mousamdas156@gmail.com
"""
================================================================================
SCHEMAS: Tenant Status Definition Codes
================================================================================
This file is used to define Pydantic validation schemas for subscription status keys 
(e.g., ACTIVE, SUSPENDED, PENDING_VERIFICATION). It maps system definitions.
"""

from datetime import datetime
from pydantic import BaseModel, Field


class StatusCreate(BaseModel):
    """
    Schema used when creating a new billing status lookup key.
    """
    # Name of the status (e.g. 'ACTIVE')
    statusName: str = Field(..., max_length=50, description="Name code of status (e.g., ACTIVE, SUSPENDED)")
    
    # Description explaining what this status code is for
    statusDescription: str | None = Field(None, max_length=255, description="Explanation description of the state")


class StatusRead(BaseModel):
    """
    Schema used to read and serialize status lookup records.
    """
    # Database autoincrement ID representing the status code
    id: int
    
    statusName: str
    statusDescription: str | None = None
    
    # When this status representation key was first created
    createdAt: datetime

    # ORM integration config
    model_config = {"from_attributes": True}
