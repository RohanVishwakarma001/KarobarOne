from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class GatewayWebhookEventCreate(BaseModel):

    gateway_name: str
    event_type: str
    event_id: str
    payload: Dict[str, Any]


class GatewayWebhookEventUpdate(BaseModel):

    processed: Optional[bool] = None
    processed_at: Optional[datetime] = None


class GatewayWebhookEventResponse(BaseModel):

    id: UUID
    gateway_name: str
    event_type: str
    event_id: str
    payload: Dict[str, Any]
    processed: bool
    processed_at: Optional[datetime]
    received_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )