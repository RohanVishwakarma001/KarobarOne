import uuid

from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.db.baseGithub import BaseGithub


class ShippingProfileZone(BaseGithub):

    __tablename__ = "shipping_profile_zones"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    shipping_profile_id = Column(
        UUID(as_uuid=True),
        ForeignKey("shipping_profiles.id"),
        nullable=False
    )

    shipping_zone_id = Column(
        UUID(as_uuid=True),
        ForeignKey("shipping_zones.id"),
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )