import uuid

from sqlalchemy import Boolean, Column, DateTime, String, JSON
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.sql import func

from app.db.baseGithub import BaseGithub


class GatewayWebhookEvent(BaseGithub):

    __tablename__ = "gateway_webhook_events"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    gateway_name = Column(
        String(50),
        nullable=False
    )

    event_type = Column(
        String(150),
        nullable=False
    )

    event_id = Column(
        String(150),
        unique=True,
        nullable=False
    )

    payload = Column(
        JSONB().with_variant(JSON(), "sqlite"),
        nullable=False
    )

    processed = Column(
        Boolean,
        default=False
    )

    processed_at = Column(
        DateTime,
        nullable=True
    )

    received_at = Column(
        DateTime,
        server_default=func.now()
    )