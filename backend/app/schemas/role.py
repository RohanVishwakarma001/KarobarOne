# Owner: mousamdas156@gmail.com
"""
Pydantic schema schemas for role.
Defines the request validation schemas, response serialization schemas, and Type checking for role.
"""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class RoleCreate(BaseModel):
    roleName: str = Field(..., max_length=100)
    roleCode: str = Field(..., max_length=50)
    description: str | None = Field(None, max_length=255)
    isSystemRole: bool = False


class RoleUpdate(BaseModel):
    roleName: str | None = Field(None, max_length=100)
    description: str | None = Field(None, max_length=255)
    isSystemRole: bool | None = None


class RoleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    roleName: str
    roleCode: str
    description: str | None
    isSystemRole: bool
    createdAt: datetime
    updatedAt: datetime
