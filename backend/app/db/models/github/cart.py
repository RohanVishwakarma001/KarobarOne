import uuid

from sqlalchemy import Column, DateTime, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.db.baseGithub import BaseGithub


class Cart(BaseGithub):

    __tablename__ = "carts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    tenant_id = Column(UUID(as_uuid=True), nullable=False)

    store_id = Column(UUID(as_uuid=True), nullable=False)

    customer_id = Column(UUID(as_uuid=True))

    session_id = Column(String(255))

    cart_status = Column(String(20), nullable=False)

    subtotal_amount = Column(Numeric(12, 2), nullable=False)

    discount_amount = Column(Numeric(12, 2), nullable=False)

    tax_amount = Column(Numeric(12, 2), nullable=False)

    shipping_amount = Column(Numeric(12, 2), nullable=False)

    total_amount = Column(Numeric(12, 2), nullable=False)

    currency_code = Column(String(3), nullable=False)

    last_activity_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    expires_at = Column(DateTime(timezone=True))

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )