# Owner: mousamdas156@gmail.com
"""
Pydantic schema schemas for user.
Defines the request validation schemas, response serialization schemas, and Type checking for user.
"""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# --------------------------------------------------------------------------------
# UserCreate
# Payload for registering a new user. Password is accepted as plaintext here;
# the service layer is responsible for hashing it before persistence.
# --------------------------------------------------------------------------------
class UserCreate(BaseModel):
    firstName: str = Field(..., max_length=100)
    lastName: str | None = Field(None, max_length=100)
    email: EmailStr
    mobile: str = Field(..., max_length=15)
    whatsappMobile: str | None = Field(None, max_length=15)
    password: str = Field(..., min_length=8, max_length=128)


# --------------------------------------------------------------------------------
# UserUpdate
# Payload for updating mutable profile fields of an existing user.
# All fields optional to support partial updates.
# --------------------------------------------------------------------------------
class UserUpdate(BaseModel):
    firstName: str | None = Field(None, max_length=100)
    lastName: str | None = Field(None, max_length=100)
    email: EmailStr | None = None
    mobile: str | None = Field(None, max_length=15)
    whatsappMobile: str | None = Field(None, max_length=15)
    isActive: bool | None = None


# --------------------------------------------------------------------------------
# UserResponse
# Outbound representation of a user. Excludes 'passwordHash' for security.
# --------------------------------------------------------------------------------
class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    firstName: str
    lastName: str | None
    email: str
    mobile: str
    whatsappMobile: str | None
    isActive: bool
    isEmailVerified: bool
    isMobileVerified: bool
    lastLoginAt: datetime | None
    # NOTE: 'createdAt'/'updatedAt' stay snake_case here because they are
    # inherited as-is from app.db.models.baseModel.BaseModelWithUpdate, which was
    # not part of this refactor.
    createdAt: datetime
    updatedAt: datetime
