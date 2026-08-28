import uuid

from sqlalchemy import Column, DateTime, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.db.baseGithub import BaseGithub


class Order(BaseGithub):

    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    tenant_id = Column(UUID(as_uuid=True), nullable=False)

    store_id = Column(UUID(as_uuid=True), nullable=False)

    customer_id = Column(UUID(as_uuid=True), nullable=False)

    cart_id = Column(UUID(as_uuid=True))

    order_number = Column(
        String(30),
        nullable=False
    )

    payment_id = Column(UUID(as_uuid=True))

    shipping_profile_id = Column(UUID(as_uuid=True))

    billing_address_id = Column(UUID(as_uuid=True), nullable=False)

    shipping_address_id = Column(UUID(as_uuid=True), nullable=False)

    order_status = Column(
        String(25),
        nullable=False
    )

    payment_status = Column(
        String(25),
        nullable=False
    )

    fulfillment_status = Column(
        String(25),
        nullable=False
    )

    subtotal_amount = Column(
        Numeric(12, 2),
        nullable=False
    )

    discount_amount = Column(
        Numeric(12, 2),
        nullable=False
    )

    tax_amount = Column(
        Numeric(12, 2),
        nullable=False
    )

    shipping_amount = Column(
        Numeric(12, 2),
        nullable=False
    )

    total_amount = Column(
        Numeric(12, 2),
        nullable=False
    )

    currency_code = Column(
        String(3),
        nullable=False
    )

    customer_note = Column(
        String(1000)
    )

    placed_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
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