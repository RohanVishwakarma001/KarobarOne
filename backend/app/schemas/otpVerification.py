# Owner: mousamdas156@gmail.com
"""
Pydantic schema schemas for otpVerification.
Defines the request validation schemas, response serialization schemas, and Type checking for otpVerification.
"""

import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict


class OtpRequest(BaseModel):
    """Payload to generate a new OTP for a given user and purpose."""
    userId: uuid.UUID
    purpose: Literal["LOGIN", "SIGNUP", "RESET", "TRANSACTION"]


class OtpVerify(BaseModel):
    """Payload to verify a raw OTP code against a pending record."""
    otpId: uuid.UUID
    code: str


class OtpVerificationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    userId: uuid.UUID
    purpose: str
    expiresAt: datetime
    verifiedAt: datetime | None
    attempts: int
    createdAt: datetime
