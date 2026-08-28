import uuid

from sqlalchemy import Column, Date, DateTime, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.db.baseGithub import BaseGithub


class PaymentReconciliationBatch(BaseGithub):

    __tablename__ = "payment_reconciliation_batches"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    batch_number = Column(
        String(50),
        unique=True,
        nullable=False
    )

    reconciliation_date = Column(
        Date,
        nullable=False
    )

    total_payments = Column(
        Integer,
        default=0
    )

    total_amount = Column(
        Numeric(10, 2),
        default=0
    )

    status = Column(
        String(20),
        nullable=False,
        default="PENDING"
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )