import uuid

from sqlalchemy import Column, DateTime, ForeignKey, Numeric, SmallInteger
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.db.baseGithub import BaseGithub


class ShippingRate(BaseGithub):

    __tablename__ = "shipping_rates"

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

    minimum_weight = Column(
        Numeric(10,2),
        nullable=False
    )

    maximum_weight = Column(
        Numeric(10,2),
        nullable=False
    )

    shipping_charge = Column(
        Numeric(10,2),
        nullable=False
    )

    estimated_days_min = Column(
        SmallInteger,
        nullable=False
    )

    estimated_days_max = Column(
        SmallInteger,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )