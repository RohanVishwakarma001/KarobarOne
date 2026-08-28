from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):

    first_name: str
    last_name: Optional[str] = None
    email: EmailStr
    mobile: Optional[str] = None
    whatsapp_mobile: Optional[str] = None
    password: str


class UserLogin(BaseModel):

    email: EmailStr
    password: str


class UserResponse(BaseModel):

    id: UUID
    first_name: str
    last_name: Optional[str]
    email: EmailStr
    mobile: Optional[str]
    whatsapp_mobile: Optional[str]
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )