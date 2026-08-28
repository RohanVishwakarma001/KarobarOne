import uuid

from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.db.baseGithub import BaseGithub


class PaymentMethod(BaseGithub):

    __tablename__ = "payment_methods"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    method_code = Column(
        String(100),
        unique=True,
        nullable=False
    )

    method_name = Column(
        String(255),
        nullable=False
    )

    is_online = Column(
        Boolean,
        default=True
    )

    is_active = Column(
        Boolean,
        default=True
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )