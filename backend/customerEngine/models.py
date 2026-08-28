# Owner - pradhansaikat123@gmail.com

import uuid
from datetime import datetime
from sqlalchemy import (
    Column,
    String,
    Boolean,
    Numeric,
    ForeignKey,
    DateTime,
    UniqueConstraint,
    TypeDecorator,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from app.db.base import Base

# Import the existing Customer and CustomerAddress models as aliases to avoid SQLAlchemy metadata table duplication conflicts
from app.db.models.customers import (
    Customer as EngineCustomer,
    CustomerAddress as EngineCustomerAddress,
)

# 1. Add isActive and profileImage hybrid properties to EngineCustomer (Customer)
@hybrid_property
def customer_is_active(self):
    return self.status == "ACTIVE"

@customer_is_active.setter
def customer_is_active(self, value):
    self.status = "ACTIVE" if value else "INACTIVE"

EngineCustomer.isActive = customer_is_active

@hybrid_property
def customer_profile_image(self):
    return getattr(self, "_profileImage", None)

@customer_profile_image.setter
def customer_profile_image(self, value):
    self._profileImage = value

EngineCustomer.profileImage = customer_profile_image

# Monkeypatch EngineCustomer.__init__ to support isActive and profileImage in constructor
original_customer_init = EngineCustomer.__init__

def custom_customer_init(self, **kwargs):
    is_active_val = kwargs.pop("isActive", None)
    profile_image_val = kwargs.pop("profileImage", None)
    original_customer_init(self, **kwargs)
    if is_active_val is not None:
        self.isActive = is_active_val
    if profile_image_val is not None:
        self.profileImage = profile_image_val

EngineCustomer.__init__ = custom_customer_init


# 2. Add isActive hybrid property to EngineCustomerAddress (CustomerAddress)
@hybrid_property
def address_is_active(self):
    return getattr(self, "_isActive", True)

@address_is_active.setter
def address_is_active(self, value):
    self._isActive = value

EngineCustomerAddress.isActive = address_is_active

# Monkeypatch EngineCustomerAddress.__init__ to support isActive in constructor
original_address_init = EngineCustomerAddress.__init__

def custom_address_init(self, **kwargs):
    is_active_val = kwargs.pop("isActive", None)
    original_address_init(self, **kwargs)
    if is_active_val is not None:
        self.isActive = is_active_val

EngineCustomerAddress.__init__ = custom_address_init


class OrderStatusDecorator(TypeDecorator):
    impl = String
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value == "SUCCESS":
            return "CONFIRMED"
        return value

    def process_result_value(self, value, dialect):
        if value == "CONFIRMED":
            return "SUCCESS"
        return value


class EngineCustomerOrder(Base):
    """
    SQLAlchemy model representing a Customer Order for guest mapping verification.
    """
    __tablename__ = "orders"
    __table_args__ = (
        {"extend_existing": True}
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenantId = Column("tenant_id", UUID(as_uuid=True), nullable=False)
    storeId = Column("store_id", UUID(as_uuid=True), nullable=False)
    customerId = Column("customer_id", UUID(as_uuid=True), ForeignKey("customers.id", ondelete="CASCADE"), nullable=False)
    orderNumber = Column("order_number", String(100), unique=True, nullable=False)
    totalAmount = Column("total_amount", Numeric(10, 2), nullable=False)
    status = Column("order_status", OrderStatusDecorator, default="PENDING", nullable=False)
    createdAt = Column("created_at", DateTime(timezone=True), server_default=func.now(), nullable=False)
    updatedAt = Column("updated_at", DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Required DB columns mapped with default values to satisfy database constraints
    billingAddressId = Column("billing_address_id", UUID(as_uuid=True), nullable=False, default=uuid.uuid4)
    shippingAddressId = Column("shipping_address_id", UUID(as_uuid=True), nullable=False, default=uuid.uuid4)
    paymentStatus = Column("payment_status", String(50), nullable=False, default="PAID")
    fulfillmentStatus = Column("fulfillment_status", String(50), nullable=False, default="UNFULFILLED")
    subtotalAmount = Column("subtotal_amount", Numeric(10, 2), nullable=False, default=0.0)
    discountAmount = Column("discount_amount", Numeric(10, 2), nullable=False, default=0.0)
    taxAmount = Column("tax_amount", Numeric(10, 2), nullable=False, default=0.0)
    shippingAmount = Column("shipping_amount", Numeric(10, 2), nullable=False, default=0.0)
    currencyCode = Column("currency_code", String(10), nullable=False, default="INR")
    placedAt = Column("placed_at", DateTime(timezone=True), nullable=False, server_default=func.now())

    # Relationships
    customer = relationship("Customer")
