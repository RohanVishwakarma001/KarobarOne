import uuid

from sqlalchemy import Column, DateTime, String, JSON
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.sql import func

from app.db.baseGithub import BaseGithub


class PaymentAuditLog(BaseGithub):

    __tablename__ = "payment_audit_logs"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    payment_id = Column(
        UUID(as_uuid=True),
        nullable=False
    )

    action_type = Column(
        String(50),
        nullable=False
    )

    old_value = Column(
        JSONB().with_variant(JSON(), "sqlite")
    )

    new_value = Column(
        JSONB().with_variant(JSON(), "sqlite")
    )

    performed_by = Column(
        UUID(as_uuid=True),
        nullable=False
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )