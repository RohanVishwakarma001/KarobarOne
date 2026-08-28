from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CustomerCreate(BaseModel):

    tenant_id: UUID
    store_id: UUID

    customer_code: str = Field(max_length=30)

    first_name: str = Field(max_length=100)
    last_name: Optional[str] = Field(default=None, max_length=100)

    email: EmailStr

    mobile: str = Field(
        pattern=r"^\+[1-9]\d{1,14}$"
    )

    password: Optional[str] = None


class CustomerResponse(BaseModel):

    id: UUID

    tenant_id: UUID
    store_id: UUID

    customer_code: str

    first_name: str
    last_name: Optional[str]

    email: EmailStr
    mobile: str

    status: str

    is_guest_customer: bool
    is_email_verified: bool
    is_mobile_verified: bool

    registered_at: Optional[datetime]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    model_config = ConfigDict(
        from_attributes=True
    )