from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class PaymentAuditLogCreate(BaseModel):

    payment_id: UUID
    action_type: str
    old_value: Optional[Dict[str, Any]] = None
    new_value: Optional[Dict[str, Any]] = None
    performed_by: UUID


class PaymentAuditLogUpdate(BaseModel):

    action_type: Optional[str] = None
    old_value: Optional[Dict[str, Any]] = None
    new_value: Optional[Dict[str, Any]] = None


class PaymentAuditLogResponse(BaseModel):

    id: UUID
    payment_id: UUID
    action_type: str
    old_value: Optional[Dict[str, Any]]
    new_value: Optional[Dict[str, Any]]
    performed_by: UUID
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )