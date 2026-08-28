from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class PaymentMethodCreate(BaseModel):

    method_code: str
    method_name: str
    is_online: bool = True
    is_active: bool = True


class PaymentMethodUpdate(BaseModel):

    method_name: Optional[str] = None
    is_online: Optional[bool] = None
    is_active: Optional[bool] = None


class PaymentMethodResponse(BaseModel):

    id: UUID
    method_code: str
    method_name: str
    is_online: bool
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )