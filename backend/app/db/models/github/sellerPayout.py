import uuid

from sqlalchemy import Column, DateTime, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.db.baseGithub import BaseGithub


class SellerPayout(BaseGithub):

    __tablename__ = "seller_payouts"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    tenant_id = Column(
        UUID(as_uuid=True),
        nullable=False
    )

    payment_id = Column(
        UUID(as_uuid=True),
        nullable=False
    )

    payout_reference = Column(
        String(150),
        unique=True
    )

    gross_amount = Column(
        Numeric(10, 2),
        nullable=False
    )

    gateway_fee = Column(
        Numeric(10, 2),
        default=0
    )

    gateway_tax = Column(
        Numeric(10, 2),
        default=0
    )

    platform_commission = Column(
        Numeric(10, 2),
        default=0
    )

    net_payout_amount = Column(
        Numeric(10, 2),
        nullable=False
    )

    payout_status = Column(
        String(20),
        nullable=False,
        default="PENDING"
    )

    payout_date = Column(
        DateTime
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )