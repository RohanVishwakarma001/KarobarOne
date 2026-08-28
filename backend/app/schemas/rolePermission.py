# Owner: mousamdas156@gmail.com
"""
Pydantic schema schemas for rolePermission.
Defines the request validation schemas, response serialization schemas, and Type checking for rolePermission.
"""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class RolePermissionCreate(BaseModel):
    permissionId: uuid.UUID


class RolePermissionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    roleId: uuid.UUID
    permissionId: uuid.UUID
    createdAt: datetime
