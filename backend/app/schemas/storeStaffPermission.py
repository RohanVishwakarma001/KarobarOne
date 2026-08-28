# Owner: mousamdas156@gmail.com
"""
Pydantic schema schemas for storeStaffPermission.
Defines the request validation schemas, response serialization schemas, and Type checking for storeStaffPermission.
"""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class StoreStaffPermissionCreate(BaseModel):
    storeId: uuid.UUID
    permissionId: uuid.UUID
    grantedBy: uuid.UUID | None = None


class StoreStaffPermissionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    userId: uuid.UUID
    storeId: uuid.UUID
    permissionId: uuid.UUID
    grantedBy: uuid.UUID | None
    createdAt: datetime
