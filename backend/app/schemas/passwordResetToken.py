# Owner: mousamdas156@gmail.com
"""
Pydantic schema schemas for passwordResetToken.
Defines the request validation schemas, response serialization schemas, and Type checking for passwordResetToken.
"""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class PasswordResetRequest(BaseModel):
    """Payload to initiate a password reset flow (looked up by email)."""
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    """Payload to complete a password reset using the raw token sent to the user."""
    token: str
    newPassword: str


class PasswordResetTokenResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    userId: uuid.UUID
    expiresAt: datetime
    usedAt: datetime | None
    createdAt: datetime
