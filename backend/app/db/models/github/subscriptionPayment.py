import uuid

from sqlalchemy import Column, DateTime, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.db.baseGithub import BaseGithub


class SubscriptionPayment(BaseGithub):

    __tablename__ = "subscription_payments"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    tenant_id = Column(
        UUID(as_uuid=True),
        nullable=False
    )

    invoice_id = Column(
        UUID(as_uuid=True),
        nullable=False
    )

    payment_reference = Column(
        String(150),
        unique=True
    )

    payment_gateway = Column(
        String(50),
        nullable=False
    )

    subscription_revenue = Column(
        Numeric(10, 2),
        nullable=False
    )

    payment_status = Column(
        String(20),
        nullable=False
    )

    paid_at = Column(
        DateTime
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )