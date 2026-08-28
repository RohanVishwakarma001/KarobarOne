import uuid

from sqlalchemy import Column, Date, DateTime, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.db.baseGithub import BaseGithub


class GatewaySettlement(BaseGithub):

    __tablename__ = "gateway_settlements"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    settlement_reference = Column(
        String(150),
        unique=True,
        nullable=False
    )

    gateway_name = Column(
        String(50),
        nullable=False
    )

    settlement_amount = Column(
        Numeric(10, 2),
        nullable=False
    )

    settlement_date = Column(
        Date,
        nullable=False
    )

    settlement_status = Column(
        String(20),
        nullable=False,
        default="PENDING"
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )