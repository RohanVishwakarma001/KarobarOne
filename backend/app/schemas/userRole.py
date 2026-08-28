# Owner: mousamdas156@gmail.com
"""
Pydantic schema schemas for userRole.
Defines the request validation schemas, response serialization schemas, and Type checking for userRole.
"""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserRoleAssign(BaseModel):
    roleId: uuid.UUID
    tenantId: uuid.UUID | None = None
    assignedBy: uuid.UUID | None = None


class UserRoleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    userId: uuid.UUID
    roleId: uuid.UUID
    tenantId: uuid.UUID | None
    assignedBy: uuid.UUID | None
    assignedAt: datetime
