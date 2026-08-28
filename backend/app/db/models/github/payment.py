import uuid

from sqlalchemy import Column, DateTime, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.db.baseGithub import BaseGithub


class Payment(BaseGithub):

    __tablename__ = "payments"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    tenant_id = Column(
        UUID(as_uuid=True),
        nullable=False
    )

    store_id = Column(
        UUID(as_uuid=True),
        nullable=False
    )

    entity_type = Column(
        String(50),
        nullable=False
    )

    entity_id = Column(
        UUID(as_uuid=True),
        nullable=False
    )

    payment_method_id = Column(
        UUID(as_uuid=True),
        nullable=False
    )

    payment_reference_number = Column(
        String(255),
        unique=True
    )

    amount = Column(
        Numeric(10, 2),
        nullable=False
    )

    currency = Column(
        String(3),
        default="INR"
    )

    payment_status = Column(
        String(50),
        nullable=False,
        default="PENDING"
    )

    payment_date = Column(
        DateTime
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )

    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )