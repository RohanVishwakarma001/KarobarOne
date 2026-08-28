import uuid

from sqlalchemy import Boolean, Column, DateTime, Integer, Numeric, SmallInteger, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.db.baseGithub import BaseGithub


class Product(BaseGithub):

    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    tenant_id = Column(UUID(as_uuid=True), nullable=False)

    store_id = Column(UUID(as_uuid=True), nullable=False)

    category_id = Column(UUID(as_uuid=True))

    product_type_id = Column(SmallInteger)

    brand_id = Column(UUID(as_uuid=True))

    product_name = Column(String(255), nullable=False)

    product_slug = Column(String(255))

    short_description = Column(String(500))

    long_description = Column(Text)

    sku_prefix = Column(String(50))

    quantity_constraint = Column(Integer)

    returnable = Column(Boolean)

    cod_available = Column(Boolean)

    gst_rate = Column(Numeric(5, 2))

    hsn_code = Column(String(20))

    status = Column(String(20))

    approval_status = Column(String(20))

    published_version_id = Column(UUID(as_uuid=True))

    created_by = Column(UUID(as_uuid=True))

    approved_by = Column(UUID(as_uuid=True))

    approved_at = Column(DateTime(timezone=True))

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    deleted_at = Column(DateTime(timezone=True))