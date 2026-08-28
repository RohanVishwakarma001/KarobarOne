import uuid

from sqlalchemy import Column, DateTime, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.db.baseGithub import BaseGithub


class PaymentRefund(BaseGithub):

    __tablename__ = "payment_refunds"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    payment_id = Column(
        UUID(as_uuid=True),
        nullable=False
    )

    refund_reference = Column(
        String(150),
        unique=True
    )

    refund_amount = Column(
        Numeric(10, 2),
        nullable=False
    )

    refund_reason = Column(
        String(500)
    )

    refund_status = Column(
        String(20),
        nullable=False,
        default="PENDING"
    )

    refunded_at = Column(
        DateTime
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )