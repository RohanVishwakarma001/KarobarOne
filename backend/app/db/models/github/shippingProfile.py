import uuid

from sqlalchemy import Boolean, Column, DateTime, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.db.baseGithub import BaseGithub


class ShippingProfile(BaseGithub):

    __tablename__ = "shipping_profiles"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    tenant_id = Column(
        UUID(as_uuid=True),
        nullable=False
    )

    profile_name = Column(
        String(255),
        nullable=False
    )

    description = Column(
        String(500)
    )

    free_shipping_threshold = Column(
        Numeric(10, 2)
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )