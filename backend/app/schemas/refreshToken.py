# Owner: mousamdas156@gmail.com
"""
Pydantic schema schemas for refreshToken.
Defines the request validation schemas, response serialization schemas, and Type checking for refreshToken.
"""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class RefreshTokenCreate(BaseModel):
    tokenHash: str = Field(..., max_length=255)
    deviceName: str | None = Field(None, max_length=100)
    deviceType: str | None = Field(None, max_length=50)
    ipAddress: str | None = Field(None, max_length=45)
    expiresAt: datetime


class RefreshTokenResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    userId: uuid.UUID
    deviceName: str | None
    deviceType: str | None
    ipAddress: str | None
    expiresAt: datetime
    revokedAt: datetime | None
    createdAt: datetime
