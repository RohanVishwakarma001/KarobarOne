# Owner: mousamdas156@gmail.com
"""
Pydantic schema schemas for userSession.
Defines the request validation schemas, response serialization schemas, and Type checking for userSession.
"""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class UserSessionCreate(BaseModel):
    refreshTokenId: uuid.UUID
    loginAt: datetime
    ipAddress: str | None = Field(None, max_length=45)
    userAgent: str | None = None


class UserSessionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    userId: uuid.UUID
    refreshTokenId: uuid.UUID
    loginAt: datetime
    logoutAt: datetime | None
    ipAddress: str | None
    userAgent: str | None
    isActive: bool
