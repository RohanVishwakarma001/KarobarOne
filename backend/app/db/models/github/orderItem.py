import uuid

from sqlalchemy import Column, DateTime, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.db.baseGithub import BaseGithub


class OrderItem(BaseGithub):

    __tablename__ = "order_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    order_id = Column(UUID(as_uuid=True), nullable=False)

    product_id = Column(UUID(as_uuid=True), nullable=False)

    product_variant_id = Column(UUID(as_uuid=True))

    sku = Column(String(100), nullable=False)

    product_name = Column(String(255), nullable=False)

    variant_name = Column(String(255))

    hsn_code = Column(String(20))

    gst_rate = Column(Numeric(5, 2))

    quantity = Column(Integer, nullable=False)

    unit_price = Column(Numeric(12, 2), nullable=False)

    discount_amount = Column(Numeric(12, 2))

    tax_amount = Column(Numeric(12, 2))

    shipping_amount = Column(Numeric(12, 2))

    line_total = Column(Numeric(12, 2), nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )