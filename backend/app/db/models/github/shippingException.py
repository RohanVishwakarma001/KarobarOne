import uuid

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Text
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.db.baseGithub import BaseGithub


class ShippingException(BaseGithub):

    __tablename__ = "shipping_exceptions"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    shipment_id = Column(
        UUID(as_uuid=True),
        ForeignKey("shipments.id"),
        nullable=False
    )

    exception_type = Column(
        Text,
        nullable=False
    )

    description = Column(
        Text
    )

    resolved = Column(
        Boolean,
        default=False
    )

    resolved_at = Column(
        DateTime(timezone=True)
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )