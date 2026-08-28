import uuid

from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.db.baseGithub import BaseGithub


class PaymentReconciliationItem(BaseGithub):

    __tablename__ = "payment_reconciliation_items"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    batch_id = Column(
        UUID(as_uuid=True),
        nullable=False
    )

    payment_id = Column(
        UUID(as_uuid=True),
        nullable=False
    )

    gateway_payment_id = Column(
        String(150)
    )

    reconciliation_status = Column(
        String(20),
        nullable=False,
        default="MATCHED"
    )

    notes = Column(
        String(500)
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )