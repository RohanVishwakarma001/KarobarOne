import uuid

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.db.baseGithub import BaseGithub


class Shipment(BaseGithub):

    __tablename__ = "shipments"

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

    shipment_request_id = Column(
        UUID(as_uuid=True),
        ForeignKey("shipment_requests.id"),
        nullable=False
    )

    shipping_partner_id = Column(
    UUID(as_uuid=True),
    ForeignKey("shipping_partners.id"),
    nullable=True
)

    shipment_number = Column(
    String(50),
    nullable=False
)

    tracking_number = Column(
    String(150)
)

    tracking_url = Column(
    String(1000)
)

    shipment_status = Column(
        String(50),
        default="PENDING"
    )

    shipped_at = Column(
        DateTime(timezone=True)
    )

    delivered_at = Column(
        DateTime(timezone=True)
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )