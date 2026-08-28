from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid

from app.db.baseGithub import BaseGithub


class ShippingPartner(BaseGithub):
    __tablename__ = "shipping_partners"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    partner_code = Column(
        String(50),
        nullable=False,
        unique=True
    )

    partner_name = Column(
        String(255),
        nullable=False
    )

    website_url = Column(
        String(255),
        nullable=True
    )

    tracking_url_template = Column(
        String(500),
        nullable=True
    )

    api_enabled = Column(
        Boolean,
        default=False,
        nullable=False
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