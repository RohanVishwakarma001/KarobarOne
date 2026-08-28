# Owner: mousamdas156@gmail.com
"""
Pydantic schema schemas for permission.
Defines the request validation schemas, response serialization schemas, and Type checking for permission.
"""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PermissionCreate(BaseModel):
    permissionName: str = Field(..., max_length=150)
    permissionCode: str = Field(..., max_length=100)
    description: str | None = Field(None, max_length=255)


class PermissionUpdate(BaseModel):
    permissionName: str | None = Field(None, max_length=150)
    description: str | None = Field(None, max_length=255)


class PermissionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    permissionName: str
    permissionCode: str
    description: str | None
    createdAt: datetime
