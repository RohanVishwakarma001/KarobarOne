import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.db.baseGithub import BaseGithub


class ShipmentRequest(BaseGithub):

    __tablename__ = "shipment_requests"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    order_id = Column(
        UUID(as_uuid=True),
        ForeignKey("orders.id"),
        nullable=False
    )

    shipping_profile_id = Column(
    UUID(as_uuid=True),
    ForeignKey("shipping_profiles.id"),
    nullable=True
)
    

    request_status = Column(
        String(50),
        nullable=False,
        default="PENDING"
    )

    requested_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )