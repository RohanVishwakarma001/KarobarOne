# This file defines the Pydantic schemas for carts
# It contains request, response, and validation models

from pydantic import BaseModel, Field, model_validator
from uuid import UUID
from datetime import datetime, date, time
from typing import Optional
from enum import Enum



# Defines the available cart status values
class CartStatus(str, Enum):
    ACTIVE = "ACTIVE"
    CHECKED_OUT = "CHECKED_OUT"
    ABANDONED = "ABANDONED"
    EXPIRED = "EXPIRED"


class CartCreate(BaseModel):
    tenant_id : UUID
    store_id : UUID
    customer_id : Optional[UUID] = None
    session_id : str

class CartUpdate(BaseModel):
    customer_id: Optional[UUID] = None
    session_id: Optional[str] = None
    cart_status: Optional[CartStatus] = None
    currency_code: Optional[str] = Field(default=None, min_length=3, max_length=3)

class CartResponse(BaseModel):
    id : UUID
    tenant_id : UUID
    store_id : UUID
    customer_id: Optional[UUID]
    session_id : str
    cart_status : CartStatus
    subtotal_amount : float
    discount_amount : float
    tax_amount : float
    shipping_amount : float
    total_amount : float
    currency_code : str 
    last_activity_at : datetime
    expires_at : Optional[datetime]
    created_at : datetime
    updated_at : datetime

    class Config:
        from_attributes = True


# ---------------------------------------------------------------------------
# Cart Item
# ---------------------------------------------------------------------------

# Cart item schemas
class CartItemCreate(BaseModel):
    cart_id: UUID
    product_id: UUID
    product_variant_id: Optional[UUID] = None 
    quantity: int = Field(default=1, gt=0)    
    unit_price: float = Field(ge=0)           
    discount_amount: Optional[float] = Field(default=0.00, ge=0)
    tax_amount: Optional[float] = Field(default=0.00, ge=0)
    

class CartItemUpdate(BaseModel):
    quantity: Optional[int] = Field(default=None, gt=0)
    discount_amount: Optional[float] = Field(default=None, ge=0)
    tax_amount: Optional[float] = Field(default=None, ge=0)


class CartItemResponse(BaseModel):
    id: UUID
    cart_id: UUID
    product_id: UUID
    product_variant_id: Optional[UUID]
    quantity: int
    unit_price: float
    discount_amount: Optional[float]
    tax_amount: Optional[float]
    line_total: float
    added_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


# ---------------------------------------------------------------------------
# Wishlist
# ---------------------------------------------------------------------------

# Wishlist schemas
class WishlistCreate(BaseModel):
    customer_id: UUID
    store_id: UUID
    wishlist_name: str = Field(min_length=1, max_length=100)
    is_default: Optional[bool] = False


class WishlistUpdate(BaseModel):
    wishlist_name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    is_default: Optional[bool] = None


class WishlistResponse(BaseModel):
    id: UUID
    customer_id: UUID
    store_id: UUID
    wishlist_name: str
    is_default: Optional[bool]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


# ---------------------------------------------------------------------------
# Wishlist Item
# ---------------------------------------------------------------------------

# Wishlist item schemas
class WishlistItemCreate(BaseModel):
    wishlist_id: UUID
    product_id: UUID
    product_variant_id: Optional[UUID] = None  # optional - not every product has variants


class WishlistItemResponse(BaseModel):
    id: UUID
    wishlist_id: UUID
    product_id: UUID
    product_variant_id: Optional[UUID]
    added_at: Optional[datetime]

    class Config:
        from_attributes = True


# ---------------------------------------------------------------------------
# Saved For Later
# ---------------------------------------------------------------------------

# Saved For Later schemas
class SavedForLaterCreate(BaseModel):
    customer_id: UUID
    product_id: UUID
    product_variant_id: Optional[UUID] = None  
    quantity: Optional[int] = Field(default=1, gt=0)  

class SavedForLaterUpdate(BaseModel):
    quantity: Optional[int] = Field(default=None, gt=0)


class SavedForLaterResponse(BaseModel):
    id: UUID
    customer_id: UUID
    product_id: UUID
    product_variant_id: Optional[UUID]
    quantity: Optional[int]
    added_at: Optional[datetime]

    class Config:
        from_attributes = True


# ---------------------------------------------------------------------------
# Abandoned Cart
# ---------------------------------------------------------------------------


# Abandoned Cart Schema
class RecoveryStatus(str, Enum):
    PENDING = "PENDING"
    RECOVERED = "RECOVERED"
    EXPIRED = "EXPIRED"


class AbandonedCartCreate(BaseModel):
    cart_id: UUID
    customer_id: Optional[UUID] = None
    recovery_status: Optional[RecoveryStatus] = RecoveryStatus.PENDING


class AbandonedCartUpdate(BaseModel):
    recovery_status: Optional[RecoveryStatus] = None
    recovered_at: Optional[datetime] = None


class AbandonedCartResponse(BaseModel):
    id: UUID
    cart_id: UUID
    customer_id: Optional[UUID]
    recovery_status: Optional[RecoveryStatus]
    reminder_sent_count: Optional[int]
    last_reminder_sent_at: Optional[datetime]
    recovered_at: Optional[datetime]
    created_at: Optional[datetime]

    class Config:
        from_attributes = True


# ---------------------------------------------------------------------------
# Cart Coupon
# ---------------------------------------------------------------------------

# Cart Cupon Schema
class CartCouponCreate(BaseModel):
    cart_id: UUID
    coupon_id: UUID
    discount_amount: float = Field(ge=0) 


class CartCouponResponse(BaseModel):
    id: UUID
    cart_id: UUID
    coupon_id: UUID
    discount_amount: float
    applied_at: Optional[datetime]

    class Config:
        from_attributes = True


# ---------------------------------------------------------------------------
# Recently Viewed Product
# ---------------------------------------------------------------------------

# Recently Viewed ProductCreate Schema
class RecentlyViewedProductCreate(BaseModel):
    customer_id: UUID
    product_id: UUID


class RecentlyViewedProductResponse(BaseModel):
    id: UUID
    customer_id: UUID
    product_id: UUID
    viewed_at: Optional[datetime]

    class Config:
        from_attributes = True

# ---------------------------------------------------------------------------
# Product Compare List
# ---------------------------------------------------------------------------

# Product Compare List Schema
class ProductCompareListCreate(BaseModel):
    customer_id: UUID
    store_id: UUID


class ProductCompareListResponse(BaseModel):
    id: UUID
    customer_id: UUID
    store_id: UUID
    created_at: Optional[datetime]

    class Config:
        from_attributes = True


# ---------------------------------------------------------------------------
# Product Compare Item
# ---------------------------------------------------------------------------

# Product Compare Item Schema
class ProductCompareItemCreate(BaseModel):
    compare_list_id: UUID
    product_id: UUID


class ProductCompareItemResponse(BaseModel):
    id: UUID
    compare_list_id: UUID
    product_id: UUID
    added_at: Optional[datetime]

    class Config:
        from_attributes = True


# ---------------------------------------------------------------------------
# Order
# ---------------------------------------------------------------------------

# Order Schema
class OrderStatus(str, Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    PROCESSING = "PROCESSING"
    PACKED = "PACKED"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"
    RETURNED = "RETURNED"
    REFUNDED = "REFUNDED"


class PaymentStatus(str, Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    FAILED = "FAILED"
    PARTIALLY_REFUNDED = "PARTIALLY_REFUNDED"
    REFUNDED = "REFUNDED"


class FulfillmentStatus(str, Enum):
    UNFULFILLED = "UNFULFILLED"
    PARTIALLY_FULFILLED = "PARTIALLY_FULFILLED"
    FULFILLED = "FULFILLED"


class OrderCreate(BaseModel):
    tenant_id: UUID
    store_id: UUID
    customer_id: UUID
    cart_id: Optional[UUID] = None
    payment_id: Optional[UUID] = None
    shipping_profile_id: Optional[UUID] = None
    billing_address_id: UUID
    shipping_address_id: UUID
    customer_note: Optional[str] = Field(default=None, max_length=1000)


class OrderUpdate(BaseModel):
    payment_id: Optional[UUID] = None
    shipping_profile_id: Optional[UUID] = None
    billing_address_id: Optional[UUID] = None
    shipping_address_id: Optional[UUID] = None
    order_status: Optional[OrderStatus] = None
    payment_status: Optional[PaymentStatus] = None
    fulfillment_status: Optional[FulfillmentStatus] = None
    customer_note: Optional[str] = Field(default=None, max_length=1000)


class OrderResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    store_id: UUID
    customer_id: UUID
    cart_id: Optional[UUID]
    payment_id: Optional[UUID]
    shipping_profile_id: Optional[UUID]
    billing_address_id: UUID
    shipping_address_id: UUID
    order_number: str
    order_status: OrderStatus
    payment_status: PaymentStatus
    fulfillment_status: FulfillmentStatus
    subtotal_amount: float
    discount_amount: float
    tax_amount: float
    shipping_amount: float
    total_amount: float
    currency_code: str
    customer_note: Optional[str]
    placed_at: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ---------------------------------------------------------------------------
# Order Item
# ---------------------------------------------------------------------------

# Order Item Schema
class OrderItemCreate(BaseModel):
    order_id: UUID
    product_id: UUID
    product_variant_id: Optional[UUID] = None
    sku: str = Field(min_length=1, max_length=100)
    product_name: str = Field(min_length=1, max_length=255)
    variant_name: Optional[str] = Field(default=None, max_length=255)
    hsn_code: Optional[str] = Field(default=None, max_length=20)
    gst_rate: Optional[float] = Field(default=None, ge=0, le=100)  
    quantity: int = Field(gt=0)                                   
    unit_price: float = Field(ge=0)                               
    discount_amount: Optional[float] = Field(default=0.00, ge=0)
    tax_amount: Optional[float] = Field(default=0.00, ge=0)
    shipping_amount: Optional[float] = Field(default=0.00, ge=0)
    # line_total is NOT accepted here - the backend calculates it


class OrderItemUpdate(BaseModel):
    sku: Optional[str] = Field(default=None, min_length=1, max_length=100)
    product_name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    variant_name: Optional[str] = Field(default=None, max_length=255)
    hsn_code: Optional[str] = Field(default=None, max_length=20)
    gst_rate: Optional[float] = Field(default=None, ge=0, le=100)
    quantity: Optional[int] = Field(default=None, gt=0)
    unit_price: Optional[float] = Field(default=None, ge=0)
    discount_amount: Optional[float] = Field(default=None, ge=0)
    tax_amount: Optional[float] = Field(default=None, ge=0)
    shipping_amount: Optional[float] = Field(default=None, ge=0)


class OrderItemResponse(BaseModel):
    id: UUID
    order_id: UUID
    product_id: UUID
    product_variant_id: Optional[UUID]
    sku: str
    product_name: str
    variant_name: Optional[str]
    hsn_code: Optional[str]
    gst_rate: Optional[float]
    quantity: int
    unit_price: float
    discount_amount: Optional[float]
    tax_amount: Optional[float]
    shipping_amount: Optional[float]
    line_total: float
    created_at: Optional[datetime]

    class Config:
        from_attributes = True


# ---------------------------------------------------------------------------
# Order Cancellation
# ---------------------------------------------------------------------------

# Order Cancellation Schema
class OrderCancellationStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class OrderCancellationCreate(BaseModel):
    order_id: UUID
    requested_by: Optional[UUID] = None
    cancellation_reason: str = Field(min_length=1, max_length=100)
    cancellation_reason_description: Optional[str] = Field(default=None, max_length=1000)


class OrderCancellationUpdate(BaseModel):
    status: Optional[OrderCancellationStatus] = None
    approved_by: Optional[UUID] = None
    approved_at: Optional[datetime] = None


class OrderCancellationResponse(BaseModel):
    id: UUID
    order_id: UUID
    requested_by: Optional[UUID]
    cancellation_reason: str
    cancellation_reason_description: Optional[str]
    status: Optional[OrderCancellationStatus]
    approved_by: Optional[UUID]
    approved_at: Optional[datetime]
    created_at: Optional[datetime]

    class Config:
        from_attributes = True


# ---------------------------------------------------------------------------
# Order Return
# ---------------------------------------------------------------------------

# Order Retrun Schema
class OrderReturnStatus(str, Enum):
    REQUESTED = "REQUESTED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    RECEIVED = "RECEIVED"
    COMPLETED = "COMPLETED"


class OrderReturnCreate(BaseModel):
    order_id: UUID
    return_reason: str = Field(min_length=1, max_length=100)
    return_reason_description: Optional[str] = Field(default=None, max_length=1000)


class OrderReturnUpdate(BaseModel):
    return_status: Optional[OrderReturnStatus] = None
    processed_at: Optional[datetime] = None
    return_approved_by: Optional[UUID] = None


class OrderReturnResponse(BaseModel):
    id: UUID
    order_id: UUID
    return_reason: str
    return_reason_description: Optional[str]
    return_status: Optional[OrderReturnStatus]
    requested_at: Optional[datetime]
    processed_at: Optional[datetime]
    return_approved_by: Optional[UUID]

    class Config:
        from_attributes = True

# ---------------------------------------------------------------------------
# Order Refund
# ---------------------------------------------------------------------------


# Order Refund Schema
class OrderRefundStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class OrderRefundCreate(BaseModel):
    order_id: UUID
    payment_refund_id: Optional[UUID] = None
    refund_amount: float = Field(ge=0)  
    refund_reason: str = Field(min_length=1, max_length=255)
    refund_reference: Optional[str] = Field(default=None, max_length=100)
    

class OrderRefundUpdate(BaseModel):
    payment_refund_id: Optional[UUID] = None
    refund_status: Optional[OrderRefundStatus] = None
    refund_reference: Optional[str] = Field(default=None, max_length=100)
    approved_by: Optional[UUID] = None
    approved_at: Optional[datetime] = None
    refunded_at: Optional[datetime] = None


class OrderRefundResponse(BaseModel):
    id: UUID
    order_id: UUID
    payment_refund_id: Optional[UUID]
    refund_amount: float
    refund_reason: str
    refund_status: Optional[OrderRefundStatus]
    refund_reference: Optional[str]
    approved_by: Optional[UUID]
    approved_at: Optional[datetime]
    refunded_at: Optional[datetime]
    created_at: Optional[datetime]

    class Config:
        from_attributes = True

# ---------------------------------------------------------------------------
# Booking
# ---------------------------------------------------------------------------

# Booking Schema
class BookingStatus(str, Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    NO_SHOW = "NO_SHOW"
    REFUNDED = "REFUNDED"


class BookingPaymentStatus(str, Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    FAILED = "FAILED"
    PARTIALLY_REFUNDED = "PARTIALLY_REFUNDED"
    REFUNDED = "REFUNDED"


class BookingMode(str, Enum):
    BOOK_ONLY = "BOOK_ONLY"
    BOOK_AND_PAY = "BOOK_AND_PAY"


class BookingCreate(BaseModel):
    tenant_id: UUID
    store_id: UUID
    service_id: UUID
    customer_id: UUID
    payment_id: Optional[UUID] = None
    booking_mode: BookingMode
    booking_date: date
    start_time: time
    end_time: time
    attendee_count: int = Field(default=1, gt=0)  
    subtotal_amount: float = Field(default=0.00, ge=0)
    discount_amount: float = Field(default=0.00, ge=0) 
    tax_amount: float = Field(default=0.00, ge=0) 
    currency_code: Optional[str] = Field(default="INR", min_length=3, max_length=3)
    booking_note: Optional[str] = Field(default=None, max_length=1000)

    @model_validator(mode="after")
    def checkTimeRange(self):
        if self.start_time >= self.end_time:
            raise ValueError("start_time must be before end_time")
        return self


class BookingUpdate(BaseModel):
    payment_id: Optional[UUID] = None
    booking_status: Optional[BookingStatus] = None
    payment_status: Optional[BookingPaymentStatus] = None
    attendee_count: Optional[int] = Field(default=None, gt=0)
    subtotal_amount: Optional[float] = Field(default=None, ge=0)
    discount_amount: Optional[float] = Field(default=None, ge=0)
    tax_amount: Optional[float] = Field(default=None, ge=0)
    booking_note: Optional[str] = Field(default=None, max_length=1000)
    approved_by: Optional[UUID] = None
    approved_at: Optional[datetime] = None
    
class BookingResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    store_id: UUID
    service_id: UUID
    customer_id: UUID
    payment_id: Optional[UUID]
    booking_number: str
    booking_status: BookingStatus
    payment_status: BookingPaymentStatus
    booking_mode: BookingMode
    booking_date: date
    start_time: time
    end_time: time
    attendee_count: int
    subtotal_amount: float
    discount_amount: float
    tax_amount: float
    total_amount: float
    currency_code: Optional[str]
    booking_note: Optional[str]
    approved_by: Optional[UUID]
    approved_at: Optional[datetime]
    booked_at: Optional[datetime]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

# ---------------------------------------------------------------------------
# Booking Cancellation
# ---------------------------------------------------------------------------

# Booking Cancellation Schema
class BookingCancellationStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class BookingCancellationCreate(BaseModel):
    booking_id: UUID
    requested_by: Optional[UUID] = None
    cancellation_reason: str = Field(min_length=1, max_length=100)
    cancellation_reason_description: Optional[str] = Field(default=None, max_length=1000)
    cancellation_charge: float = Field(default=0.00, ge=0)

    

class BookingCancellationUpdate(BaseModel):
    cancellation_reason: Optional[str] = Field(default=None, min_length=1, max_length=100)
    cancellation_reason_description: Optional[str] = Field(default=None, max_length=1000)
    cancellation_charge: Optional[float] = Field(default=None, ge=0)
    status: Optional[BookingCancellationStatus] = None
    approved_by: Optional[UUID] = None
    approved_at: Optional[datetime] = None


class BookingCancellationResponse(BaseModel):
    id: UUID
    booking_id: UUID
    requested_by: Optional[UUID]
    cancellation_reason: str
    cancellation_reason_description: Optional[str]
    cancellation_charge: float
    status: BookingCancellationStatus
    approved_by: Optional[UUID]
    approved_at: Optional[datetime]
    created_at: Optional[datetime]

    class Config:
        from_attributes = True



# ---------------------------------------------------------------------------
# Booking Refund
# ---------------------------------------------------------------------------

# Booking Refund Schema
class BookingRefundStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"


class BookingRefundCreate(BaseModel):
    booking_id: UUID
    payment_refund_id: Optional[UUID] = None
    refund_amount: float = Field(ge=0)     
    refund_reason: str = Field(min_length=1, max_length=255)
    refund_reference: Optional[str] = Field(default=None, max_length=100)


class BookingRefundUpdate(BaseModel):
    refund_status: Optional[BookingRefundStatus] = None
    refund_reference: Optional[str] = Field(default=None, max_length=100)
    approved_by: Optional[UUID] = None
    approved_at: Optional[datetime] = None
    refunded_at: Optional[datetime] = None


class BookingRefundResponse(BaseModel):
    id: UUID
    booking_id: UUID
    payment_refund_id: Optional[UUID]
    refund_amount: float
    refund_reason: str
    refund_status: BookingRefundStatus
    refund_reference: Optional[str]
    approved_by: Optional[UUID]
    approved_at: Optional[datetime]
    refunded_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


# ---------------------------------------------------------------------------
# Booking Feedback
# ---------------------------------------------------------------------------

# Booking Feedback Schema
class BookingFeedbackCreate(BaseModel):
    booking_id: UUID
    customer_id: UUID
    rating: int = Field(ge=1, le=5)         
    review_title: Optional[str] = Field(default=None, max_length=150)
    review_text: Optional[str] = None
    is_verified_booking: Optional[bool] = None
    is_published: Optional[bool] = None


class BookingFeedbackUpdate(BaseModel):
    rating: Optional[int] = Field(default=None, ge=1, le=5)
    review_title: Optional[str] = Field(default=None, max_length=150)
    review_text: Optional[str] = None
    is_verified_booking: Optional[bool] = None
    is_published: Optional[bool] = None


class BookingFeedbackResponse(BaseModel):
    id: UUID
    booking_id: UUID
    customer_id: UUID
    rating: int
    review_title: Optional[str]
    review_text: Optional[str]
    is_verified_booking: Optional[bool]
    is_published: Optional[bool]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ---------------------------------------------------------------------------
# Offer
# ---------------------------------------------------------------------------

# Offer Schema
class OfferType(str, Enum):
    PRODUCT = "PRODUCT"
    SERVICE = "SERVICE"
    CATEGORY = "CATEGORY"
    STORE = "STORE"
    COUPON = "COUPON"


class OfferDiscountType(str, Enum):
    PERCENTAGE = "PERCENTAGE"
    FLAT = "FLAT"


class OfferApprovalStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class OfferCreate(BaseModel):
    tenant_id: UUID
    store_id: UUID
    offer_name: str = Field(min_length=1, max_length=255)
    offer_code: str = Field(min_length=1, max_length=100)
    offer_type: OfferType
    discount_type: OfferDiscountType
    discount_value: float = Field(gt=0)                             
    maximum_discount_amount: Optional[float] = Field(default=None, ge=0) 
    minimum_order_amount: Optional[float] = Field(default=None, ge=0)   
    starts_at: datetime
    ends_at: datetime
    priority: Optional[int] = None
    is_active: Optional[bool] = True
    created_by: UUID
   
    @model_validator(mode="after")
    def validateDateRange(self):
        if self.starts_at and self.ends_at and self.starts_at >= self.ends_at:
            raise ValueError("starts_at must be before ends_at")
        return self


class OfferUpdate(BaseModel):
    offer_name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    offer_code: Optional[str] = Field(default=None, min_length=1, max_length=100)
    offer_type: Optional[OfferType] = None
    discount_type: Optional[OfferDiscountType] = None
    discount_value: Optional[float] = Field(default=None, gt=0)
    maximum_discount_amount: Optional[float] = Field(default=None, ge=0)
    minimum_order_amount: Optional[float] = Field(default=None, ge=0)
    starts_at: Optional[datetime] = None
    ends_at: Optional[datetime] = None
    priority: Optional[int] = None
    is_active: Optional[bool] = None
    approval_status: Optional[OfferApprovalStatus] = None
    approved_by: Optional[UUID] = None
    approved_at: Optional[datetime] = None

    @model_validator(mode="after")
    def validateDateRange(self):
        if self.starts_at and self.ends_at and self.starts_at >= self.ends_at:
            raise ValueError("starts_at must be before ends_at")
        return self


class OfferResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    store_id: UUID
    offer_name: str
    offer_code: str
    offer_type: OfferType
    discount_type: OfferDiscountType
    discount_value: float
    maximum_discount_amount: Optional[float]
    minimum_order_amount: Optional[float]
    starts_at: datetime
    ends_at: datetime
    priority: Optional[int]
    is_active: Optional[bool]
    approval_status: OfferApprovalStatus
    created_by: UUID
    approved_by: Optional[UUID]
    approved_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ---------------------------------------------------------------------------
# Offer Target
# ---------------------------------------------------------------------------

# Offer Target Schema
class OfferTargetType(str, Enum):
    PRODUCT = "PRODUCT"
    SERVICE = "SERVICE"
    CATEGORY = "CATEGORY"
    STORE = "STORE"


class OfferTargetCreate(BaseModel):
    offer_id: UUID
    target_type: OfferTargetType
    target_id: UUID


class OfferTargetResponse(BaseModel):
    id: UUID
    offer_id: UUID
    target_type: OfferTargetType
    target_id: UUID
    created_at: Optional[datetime]

    class Config:
        from_attributes = True

# ---------------------------------------------------------------------------
# Coupon
# ---------------------------------------------------------------------------

# Cupon Schema
class CouponCreate(BaseModel):
    offer_id: UUID
    coupon_code: str = Field(min_length=1, max_length=100)
    usage_limit: Optional[int] = Field(default=None, gt=0)
    usage_limit_per_customer: Optional[int] = Field(default=None, gt=0)
    first_time_customer_only: bool = False


class CouponUpdate(BaseModel):
    offer_id: Optional[UUID] = None
    coupon_code: Optional[str] = Field(default=None, min_length=1, max_length=100)
    usage_limit: Optional[int] = Field(default=None, gt=0)
    usage_limit_per_customer: Optional[int] = Field(default=None, gt=0)
    first_time_customer_only: Optional[bool] = None


class CouponResponse(BaseModel):
    id: UUID
    offer_id: UUID
    coupon_code: str
    usage_limit: Optional[int]
    usage_limit_per_customer: Optional[int]
    first_time_customer_only: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# ---------------------------------------------------------------------------
# Coupon Redemption
# ---------------------------------------------------------------------------

# Cupon Redemption Schema
class CouponRedemptionCreate(BaseModel):
    coupon_id: UUID
    customer_id: UUID
    order_id: Optional[UUID] = None
    booking_id: Optional[UUID] = None
    discount_amount: float = Field(ge=0)

    @model_validator(mode="after")
    def validateRedemptionTarget(self):
        # At least one target must be provided
        if self.order_id is None and self.booking_id is None:
            raise ValueError("Either order_id or booking_id must be provided")
        return self


class CouponRedemptionUpdate(BaseModel):
    order_id: Optional[UUID] = None
    booking_id: Optional[UUID] = None
    discount_amount: Optional[float] = Field(default=None, ge=0)

    @model_validator(mode="after")
    def validateRedemptionTarget(self):
        if self.order_id is None and self.booking_id is None:
            return self
        return self


class CouponRedemptionResponse(BaseModel):
    id: UUID
    coupon_id: UUID
    customer_id: UUID
    order_id: Optional[UUID]
    booking_id: Optional[UUID]
    discount_amount: float
    redeemed_at: datetime

    class Config:
        from_attributes = True

# ---------------------------------------------------------------------------
# Offer Customer Segment
# ---------------------------------------------------------------------------

# Offer Customer Segment Schema
class OfferCustomerSegmentCreate(BaseModel):
    offer_id: UUID
    customer_group_id: UUID


class OfferCustomerSegmentUpdate(BaseModel):
    offer_id: Optional[UUID] = None
    customer_group_id: Optional[UUID] = None


class OfferCustomerSegmentResponse(BaseModel):
    id: UUID
    offer_id: UUID
    customer_group_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

# ---------------------------------------------------------------------------
# Offer Exclusion
# ---------------------------------------------------------------------------

# Offer Exclusion Schema
class EntityType(str, Enum):
    PRODUCT = "PRODUCT"
    SERVICE = "SERVICE"
    CATEGORY = "CATEGORY"
    CUSTOMER_GROUP = "CUSTOMER_GROUP"


class OfferExclusionCreate(BaseModel):
    offer_id: UUID
    entity_type: EntityType
    entity_id: UUID


class OfferExclusionUpdate(BaseModel):
    offer_id: Optional[UUID] = None
    entity_type: Optional[EntityType] = None
    entity_id: Optional[UUID] = None


class OfferExclusionResponse(BaseModel):
    id: UUID
    offer_id: UUID
    entity_type: EntityType
    entity_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True

# ---------------------------------------------------------------------------
# Notification
# ---------------------------------------------------------------------------

# Notification Schema
class NotificationType(str, Enum):
    OFFER = "OFFER"
    ORDER = "ORDER"
    BOOKING = "BOOKING"
    PAYMENT = "PAYMENT"
    SYSTEM = "SYSTEM"


class NotificationChannel(str, Enum):
    EMAIL = "EMAIL"
    SMS = "SMS"
    WHATSAPP = "WHATSAPP"
    IN_APP = "IN_APP"


class NotificationStatus(str, Enum):
    PENDING = "PENDING"
    QUEUED = "QUEUED"
    SENT = "SENT"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class NotificationCreate(BaseModel):
    tenant_id: UUID
    store_id: Optional[UUID] = None
    customer_id: Optional[UUID] = None
    entity_type: Optional[str] = None
    entity_id: Optional[UUID] = None
    notification_type: NotificationType
    channel: NotificationChannel
    subject: Optional[str] = Field(default=None, max_length=255)
    message: str
    scheduled_at: Optional[datetime] = None


class NotificationUpdate(BaseModel):
    store_id: Optional[UUID] = None
    customer_id: Optional[UUID] = None
    entity_type: Optional[str] = None
    entity_id: Optional[UUID] = None
    notification_type: Optional[NotificationType] = None
    channel: Optional[NotificationChannel] = None
    subject: Optional[str] = Field(default=None, max_length=255)
    message: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    sent_at: Optional[datetime] = None
    status: Optional[NotificationStatus] = None


class NotificationResponse(BaseModel):
    id: UUID
    tenant_id: UUID
    store_id: Optional[UUID]
    customer_id: Optional[UUID]
    entity_type: Optional[str]
    entity_id: Optional[UUID]
    notification_type: NotificationType
    channel: NotificationChannel
    subject: Optional[str]
    message: str
    scheduled_at: Optional[datetime]
    sent_at: Optional[datetime]
    status: NotificationStatus
    created_at: datetime

    class Config:
        from_attributes = True