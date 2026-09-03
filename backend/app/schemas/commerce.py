# Pydantic schemas for the ACTIVE cart/order/payment routers
# (app/api/v1/endpoints/{cart,orders,payments}.py). These wrap the existing
# github-ported tables (carts, cart_items, orders, order_items, payments, ...)
# rather than new ones — see docs/api-mapping/commerce.md for why.

from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator

# ═══════════════════════════════════════════════
# CART
# ═══════════════════════════════════════════════
CartStatus = Literal["ACTIVE", "CONVERTED", "ABANDONED", "EXPIRED"]


class CartItemResponse(BaseModel):
    id: UUID
    productId: UUID = Field(validation_alias="product_id", serialization_alias="productId")
    productVariantId: Optional[UUID] = Field(default=None, validation_alias="product_variant_id", serialization_alias="productVariantId")
    quantity: int
    unitPrice: Decimal = Field(validation_alias="unit_price", serialization_alias="unitPrice")
    discountAmount: Decimal = Field(default=Decimal("0.00"), validation_alias="discount_amount", serialization_alias="discountAmount")
    taxAmount: Decimal = Field(default=Decimal("0.00"), validation_alias="tax_amount", serialization_alias="taxAmount")
    lineTotal: Decimal = Field(validation_alias="line_total", serialization_alias="lineTotal")

    model_config = {"from_attributes": True, "populate_by_name": True}


class CartResponse(BaseModel):
    id: UUID
    tenantId: UUID = Field(validation_alias="tenant_id", serialization_alias="tenantId")
    storeId: UUID = Field(validation_alias="store_id", serialization_alias="storeId")
    customerId: Optional[UUID] = Field(default=None, validation_alias="customer_id", serialization_alias="customerId")
    sessionId: Optional[str] = Field(default=None, validation_alias="session_id", serialization_alias="sessionId")
    status: CartStatus = Field(validation_alias="cart_status", serialization_alias="status")
    subtotalAmount: Decimal = Field(validation_alias="subtotal_amount", serialization_alias="subtotalAmount")
    discountAmount: Decimal = Field(validation_alias="discount_amount", serialization_alias="discountAmount")
    taxAmount: Decimal = Field(validation_alias="tax_amount", serialization_alias="taxAmount")
    shippingAmount: Decimal = Field(validation_alias="shipping_amount", serialization_alias="shippingAmount")
    totalAmount: Decimal = Field(validation_alias="total_amount", serialization_alias="totalAmount")
    currencyCode: str = Field(validation_alias="currency_code", serialization_alias="currencyCode")
    items: List[CartItemResponse] = []

    model_config = {"from_attributes": True, "populate_by_name": True}


class AddCartItemRequest(BaseModel):
    productId: UUID
    productVariantId: Optional[UUID] = None
    quantity: int = Field(default=1, ge=1, le=999)


class UpdateCartItemRequest(BaseModel):
    quantity: int = Field(..., ge=1, le=999)


class ApplyCouponRequest(BaseModel):
    couponCode: str = Field(..., min_length=1, max_length=100)
    customerId: UUID = Field(..., description="Required to enforce per-customer usage limits")


class ApplyCouponResponse(BaseModel):
    couponCode: str
    discountAmount: Decimal
    cart: CartResponse


# ═══════════════════════════════════════════════
# ORDERS
# ═══════════════════════════════════════════════

# The user-facing 6-state flow this module implements — a simplified,
# strictly-validated subset of the more granular states the older
# orderStatusService.py recognizes (PACKED, OUT_FOR_DELIVERY, etc.). See
# docs/api-mapping/commerce.md for the mapping and why this one was chosen.
OrderStatus = Literal["PENDING", "PAID", "PROCESSING", "SHIPPED", "DELIVERED", "CANCELLED"]

ORDER_STATUS_TRANSITIONS: Dict[str, set] = {
    "PENDING": {"PAID", "CANCELLED"},
    "PAID": {"PROCESSING", "CANCELLED"},
    "PROCESSING": {"SHIPPED", "CANCELLED"},
    "SHIPPED": {"DELIVERED"},
    "DELIVERED": set(),
    "CANCELLED": set(),
}


class OrderItemInput(BaseModel):
    productId: UUID
    productVariantId: Optional[UUID] = None
    sku: str = Field(..., max_length=100)
    productName: str = Field(..., max_length=255)
    variantName: Optional[str] = Field(default=None, max_length=255)
    quantity: int = Field(..., ge=1, le=999)
    unitPrice: Decimal = Field(..., ge=0)
    taxAmount: Decimal = Field(default=Decimal("0.00"), ge=0)
    discountAmount: Decimal = Field(default=Decimal("0.00"), ge=0)


class OrderItemResponse(BaseModel):
    id: UUID
    productId: UUID = Field(validation_alias="product_id", serialization_alias="productId")
    productVariantId: Optional[UUID] = Field(default=None, validation_alias="product_variant_id", serialization_alias="productVariantId")
    sku: str
    productName: str = Field(validation_alias="product_name", serialization_alias="productName")
    variantName: Optional[str] = Field(default=None, validation_alias="variant_name", serialization_alias="variantName")
    quantity: int
    unitPrice: Decimal = Field(validation_alias="unit_price", serialization_alias="unitPrice")
    discountAmount: Decimal = Field(default=Decimal("0.00"), validation_alias="discount_amount", serialization_alias="discountAmount")
    taxAmount: Decimal = Field(default=Decimal("0.00"), validation_alias="tax_amount", serialization_alias="taxAmount")
    lineTotal: Decimal = Field(validation_alias="line_total", serialization_alias="lineTotal")

    model_config = {"from_attributes": True, "populate_by_name": True}


class CreateOrderRequest(BaseModel):
    tenantId: UUID
    storeId: UUID
    customerId: UUID
    billingAddressId: UUID
    shippingAddressId: UUID
    items: List[OrderItemInput] = Field(..., min_length=1)
    shippingAmount: Decimal = Field(default=Decimal("0.00"), ge=0)
    customerNote: Optional[str] = Field(default=None, max_length=1000)
    cartId: Optional[UUID] = Field(default=None, description="If set, the cart is marked CONVERTED on success")


class OrderResponse(BaseModel):
    id: UUID
    tenantId: UUID = Field(validation_alias="tenant_id", serialization_alias="tenantId")
    storeId: UUID = Field(validation_alias="store_id", serialization_alias="storeId")
    customerId: UUID = Field(validation_alias="customer_id", serialization_alias="customerId")
    orderNumber: str = Field(validation_alias="order_number", serialization_alias="orderNumber")
    billingAddressId: UUID = Field(validation_alias="billing_address_id", serialization_alias="billingAddressId")
    shippingAddressId: UUID = Field(validation_alias="shipping_address_id", serialization_alias="shippingAddressId")
    orderStatus: OrderStatus = Field(validation_alias="order_status", serialization_alias="orderStatus")
    paymentStatus: str = Field(validation_alias="payment_status", serialization_alias="paymentStatus")
    fulfillmentStatus: str = Field(validation_alias="fulfillment_status", serialization_alias="fulfillmentStatus")
    subtotalAmount: Decimal = Field(validation_alias="subtotal_amount", serialization_alias="subtotalAmount")
    discountAmount: Decimal = Field(validation_alias="discount_amount", serialization_alias="discountAmount")
    taxAmount: Decimal = Field(validation_alias="tax_amount", serialization_alias="taxAmount")
    shippingAmount: Decimal = Field(validation_alias="shipping_amount", serialization_alias="shippingAmount")
    totalAmount: Decimal = Field(validation_alias="total_amount", serialization_alias="totalAmount")
    currencyCode: str = Field(validation_alias="currency_code", serialization_alias="currencyCode")
    customerNote: Optional[str] = Field(default=None, validation_alias="customer_note", serialization_alias="customerNote")
    placedAt: Optional[datetime] = Field(default=None, validation_alias="placed_at", serialization_alias="placedAt")
    createdAt: Optional[datetime] = Field(default=None, validation_alias="created_at", serialization_alias="createdAt")
    updatedAt: Optional[datetime] = Field(default=None, validation_alias="updated_at", serialization_alias="updatedAt")
    items: List[OrderItemResponse] = []

    model_config = {"from_attributes": True, "populate_by_name": True}


class UpdateOrderStatusRequest(BaseModel):
    status: OrderStatus
    reason: Optional[str] = Field(default=None, max_length=500)


class OrderStatusEventResponse(BaseModel):
    oldStatus: Optional[str] = Field(default=None, validation_alias="old_status", serialization_alias="oldStatus")
    newStatus: str = Field(validation_alias="new_status", serialization_alias="newStatus")
    changeReason: Optional[str] = Field(default=None, validation_alias="change_reason", serialization_alias="changeReason")
    changedAt: Optional[datetime] = Field(default=None, validation_alias="changed_at", serialization_alias="changedAt")

    model_config = {"from_attributes": True, "populate_by_name": True}


# ═══════════════════════════════════════════════
# PAYMENTS / RAZORPAY
# ═══════════════════════════════════════════════
class CreateRazorpayOrderRequest(BaseModel):
    tenantId: UUID
    storeId: UUID
    orderId: UUID


class CreateRazorpayOrderResponse(BaseModel):
    razorpayOrderId: str
    razorpayKeyId: str
    amount: int = Field(description="Amount in paise, matching what Razorpay Checkout.js expects")
    currency: str
    paymentId: UUID


class VerifyRazorpayPaymentRequest(BaseModel):
    razorpayOrderId: str
    razorpayPaymentId: str
    razorpaySignature: str


class VerifyRazorpayPaymentResponse(BaseModel):
    verified: bool
    order: OrderResponse


class CreateRefundRequest(BaseModel):
    razorpayPaymentId: str = Field(
        ...,
        description=(
            "The Razorpay payment id (pay_xxx) to refund. Required explicitly rather than "
            "looked up server-side: Payment.payment_reference_number (the one free-form "
            "reference column on this table) is used as the idempotency key for Razorpay "
            "*order* creation and must stay stable, so it can't also double as the payment id."
        ),
    )
    amount: Optional[Decimal] = Field(default=None, ge=0, description="Omit for a full refund")
    reason: Optional[str] = Field(default=None, max_length=500)


class RefundResponse(BaseModel):
    id: UUID
    paymentId: UUID = Field(validation_alias="payment_id", serialization_alias="paymentId")
    refundReference: Optional[str] = Field(default=None, validation_alias="refund_reference", serialization_alias="refundReference")
    refundAmount: Decimal = Field(validation_alias="refund_amount", serialization_alias="refundAmount")
    refundReason: Optional[str] = Field(default=None, validation_alias="refund_reason", serialization_alias="refundReason")
    refundStatus: str = Field(validation_alias="refund_status", serialization_alias="refundStatus")
    refundedAt: Optional[datetime] = Field(default=None, validation_alias="refunded_at", serialization_alias="refundedAt")

    model_config = {"from_attributes": True, "populate_by_name": True}
