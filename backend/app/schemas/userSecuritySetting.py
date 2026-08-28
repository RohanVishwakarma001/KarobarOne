# Owner: mousamdas156@gmail.com
"""
Pydantic schema schemas for userSecuritySetting.
Defines the request validation schemas, response serialization schemas, and Type checking for userSecuritySetting.
"""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UserSecuritySettingUpdate(BaseModel):
    twoFactorEnabled: bool | None = None


class UserSecuritySettingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    userId: uuid.UUID
    twoFactorEnabled: bool
    failedLoginCount: int
    accountLockedUntil: datetime | None
    passwordChangedAt: datetime | None
    createdAt: datetime
    updatedAt: datetime
