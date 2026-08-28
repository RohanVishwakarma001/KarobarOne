import uuid

from sqlalchemy import Column, DateTime, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.db.baseGithub import BaseGithub


class GatewaySettlementItem(BaseGithub):

    __tablename__ = "gateway_settlement_items"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    settlement_id = Column(
        UUID(as_uuid=True),
        nullable=False
    )

    payment_id = Column(
        UUID(as_uuid=True),
        nullable=False
    )

    settlement_amount = Column(
        Numeric(10, 2),
        nullable=False
    )

    fee_amount = Column(
        Numeric(10, 2),
        default=0
    )

    tax_amount = Column(
        Numeric(10, 2),
        default=0
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )