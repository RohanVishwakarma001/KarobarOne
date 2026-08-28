# Owner: mousamdas156@gmail.com
"""
Pydantic schema schemas for loginHistory.
Defines the request validation schemas, response serialization schemas, and Type checking for loginHistory.
"""

import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class LoginHistoryCreate(BaseModel):
    userId: uuid.UUID | None = None
    email: EmailStr
    ipAddress: str | None = Field(None, max_length=45)
    userAgent: str | None = None
    loginStatus: Literal["SUCCESS", "FAILED"]
    failureReason: str | None = Field(None, max_length=255)


class LoginHistoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    userId: uuid.UUID | None
    email: str
    ipAddress: str | None
    userAgent: str | None
    loginStatus: str
    failureReason: str | None
    createdAt: datetime
