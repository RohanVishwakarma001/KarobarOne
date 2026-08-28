# This file defines the SQLAlchemy models for the e-commerce module
# Each class maps to a corresponding database table

from sqlalchemy import Column, String, Text, Numeric, DateTime, Date, Time, Integer, Boolean, SmallInteger, text, CHAR, func
from sqlalchemy.dialects.postgresql import UUID
from app.db.baseGithub import BaseGithub


class Wishlist(BaseGithub):
    __tablename__ = "wishlists"

    # Primary Key
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    customer_id = Column(UUID(as_uuid=True), nullable=False)
    store_id = Column(UUID(as_uuid=True), nullable=False)
    wishlist_name = Column(String(100), nullable=False)

    is_default = Column(
        Boolean,
        nullable=True,
        server_default=text("false")
    )

    # Timestamps
    created_at = Column(
        DateTime,
        nullable=True,
        server_default=text("now()")
    )

    updated_at = Column(
        DateTime,
        nullable=True,
        server_default=text("now()"),
        onupdate=func.now()
    )


# ---------------------------------------------------------------------------
# Wishlist Item
# ---------------------------------------------------------------------------

class WishlistItem(BaseGithub):
    __tablename__ = "wishlist_items"

    # Primary Key
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    wishlist_id = Column(UUID(as_uuid=True), nullable=False)
    product_id = Column(UUID(as_uuid=True), nullable=False)
    product_variant_id = Column(UUID(as_uuid=True), nullable=True)

    added_at = Column(
        DateTime,
        nullable=True,
        server_default=text("now()")
    )

# ---------------------------------------------------------------------------
# Saved for later
# ---------------------------------------------------------------------------

class SavedForLater(BaseGithub):
    __tablename__ = "saved_for_later"

    # Primary Key
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    customer_id = Column(UUID(as_uuid=True), nullable=False)
    product_id = Column(UUID(as_uuid=True), nullable=False)
    product_variant_id = Column(UUID(as_uuid=True), nullable=True)

    quantity = Column(
        Integer,
        nullable=True,
        server_default=text("1")
    )

    added_at = Column(
        DateTime,
        nullable=True,
        server_default=text("now()")
    )

# ---------------------------------------------------------------------------
# Abandoned Cart
# ---------------------------------------------------------------------------


class AbandonedCart(BaseGithub):
    __tablename__ = "abandoned_carts"

    # Primary Key
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    cart_id = Column(UUID(as_uuid=True), nullable=False)
    customer_id = Column(UUID(as_uuid=True), nullable=True)

    recovery_status = Column(
        String(20),
        nullable=True,
        server_default=text("'PENDING'")
    )

    reminder_sent_count = Column(
        SmallInteger,
        nullable=True,
        server_default=text("0")
    )

    last_reminder_sent_at = Column(DateTime, nullable=True)
    recovered_at = Column(DateTime, nullable=True)

    created_at = Column(
        DateTime,
        nullable=True,
        server_default=text("now()")
    )

# ---------------------------------------------------------------------------
# Cart coupon
# ---------------------------------------------------------------------------


class CartCoupon(BaseGithub):
    __tablename__ = "cart_coupons"

    # Primary Key
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    cart_id = Column(UUID(as_uuid=True), nullable=False)
    coupon_id = Column(UUID(as_uuid=True), nullable=False)

    discount_amount = Column(Numeric(12, 2), nullable=False)

    applied_at = Column(
        DateTime,
        nullable=True,
        server_default=text("now()")
    )

    
# ---------------------------------------------------------------------------
# Recently Viewed Product
# ---------------------------------------------------------------------------

class RecentlyViewedProduct(BaseGithub):
    __tablename__ = "recently_viewed_products"

    # Primary Key
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    customer_id = Column(UUID(as_uuid=True), nullable=False)
    product_id = Column(UUID(as_uuid=True), nullable=False)

    viewed_at = Column(
        DateTime,
        nullable=True,
        server_default=text("now()")
    )

# ---------------------------------------------------------------------------
# Product compare list
# ---------------------------------------------------------------------------

class ProductCompareList(BaseGithub):
    __tablename__ = "product_compare_lists"

    # Primary Key
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    customer_id = Column(UUID(as_uuid=True), nullable=False)
    store_id = Column(UUID(as_uuid=True), nullable=False)

    created_at = Column(
        DateTime,
        nullable=True,
        server_default=text("now()")
    )

# ---------------------------------------------------------------------------
# Product compare Item
# ---------------------------------------------------------------------------    

class ProductCompareItem(BaseGithub):
    __tablename__ = "product_compare_items"

    # Primary Key
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    compare_list_id = Column(UUID(as_uuid=True), nullable=False)
    product_id = Column(UUID(as_uuid=True), nullable=False)

    added_at = Column(
        DateTime,
        nullable=True,
        server_default=text("now()")
    )


# ---------------------------------------------------------------------------
# Order Cancellation
# ---------------------------------------------------------------------------

class OrderCancellation(BaseGithub):
    __tablename__ = "order_cancellations"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    order_id = Column(UUID(as_uuid=True), nullable=False)
    requested_by = Column(UUID(as_uuid=True), nullable=True)

    cancellation_reason = Column(String(100), nullable=False)
    cancellation_reason_description = Column(String(1000), nullable=True)

    status = Column(
        String(20),
        nullable=True,
        server_default=text("'PENDING'")
    )

    approved_by = Column(UUID(as_uuid=True), nullable=True)
    approved_at = Column(DateTime, nullable=True)

    created_at = Column(
        DateTime,
        nullable=True,
        server_default=text("now()")
    )


# ---------------------------------------------------------------------------
# Order return 
# ---------------------------------------------------------------------------


class OrderReturn(BaseGithub):
    __tablename__ = "order_returns"

    # Primary Key
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    order_id = Column(UUID(as_uuid=True), nullable=False)

    return_reason = Column(String(100), nullable=False)
    return_reason_description = Column(String(1000), nullable=True)

    return_status = Column(
        String(25),
        nullable=True,
        server_default=text("'REQUESTED'")
    )

    requested_at = Column(
        DateTime,
        nullable=True,
        server_default=text("now()")
    )

    processed_at = Column(DateTime, nullable=True)
    return_approved_by = Column(UUID(as_uuid=True), nullable=True)

# ---------------------------------------------------------------------------
# Order refund 
# ---------------------------------------------------------------------------

class OrderRefund(BaseGithub):
    __tablename__ = "order_refunds"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    order_id = Column(UUID(as_uuid=True), nullable=False)
    payment_refund_id = Column(UUID(as_uuid=True), nullable=True)
    refund_amount = Column(Numeric(12, 2), nullable=False)
    refund_reason = Column(String(255), nullable=False)

    refund_status = Column(
        String(25),
        nullable=True,
        server_default=text("'PENDING'")
    )

    refund_reference = Column(String(100), nullable=True)

    approved_by = Column(UUID(as_uuid=True), nullable=True)
    approved_at = Column(DateTime, nullable=True)
    refunded_at = Column(DateTime, nullable=True)

    created_at = Column(
        DateTime,
        nullable=True,
        server_default=text("now()")
    )

# ---------------------------------------------------------------------------
# Booking 
# ---------------------------------------------------------------------------

class Booking(BaseGithub):
    __tablename__ = "bookings"

    # Primary Key
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    tenant_id = Column(UUID(as_uuid=True), nullable=False)
    store_id = Column(UUID(as_uuid=True), nullable=False)
    service_id = Column(UUID(as_uuid=True), nullable=False)
    customer_id = Column(UUID(as_uuid=True), nullable=False)
    payment_id = Column(UUID(as_uuid=True), nullable=True)
    booking_number = Column(String(30), nullable=False)

    booking_status = Column(
        String(25),
        nullable=False,
        server_default=text("'PENDING'")
    )

    payment_status = Column(
        String(25),
        nullable=False,
        server_default=text("'PENDING'")
    )

    booking_mode = Column(String(30), nullable=False)

    booking_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

    attendee_count = Column(
        Integer,
        nullable=False,
        server_default=text("1")
    )

    subtotal_amount = Column(
        Numeric(12, 2),
        nullable=False,
        server_default=text("0.00")
    )

    discount_amount = Column(
        Numeric(12, 2),
        nullable=False,
        server_default=text("0.00")
    )

    tax_amount = Column(
        Numeric(12, 2),
        nullable=False,
        server_default=text("0.00")
    )

    total_amount = Column(Numeric(12, 2), nullable=False)

    currency_code = Column(
        CHAR(3),
        nullable=False,
        server_default=text("'INR'")
    )

    booking_note = Column(String(1000), nullable=True)

    approved_by = Column(UUID(as_uuid=True), nullable=True)
    approved_at = Column(DateTime, nullable=True)

    booked_at = Column(
        DateTime,
        nullable=False,
        server_default=text("now()")
    )

    created_at = Column(
        DateTime,
        nullable=False,
        server_default=text("now()")
    )

    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=text("now()"),
        onupdate=func.now()
    )


# ---------------------------------------------------------------------------
# Booking Cancellation
# ---------------------------------------------------------------------------

class BookingCancellation(BaseGithub):
    __tablename__ = "booking_cancellations"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    booking_id = Column(UUID(as_uuid=True), nullable=False)

    requested_by = Column(UUID(as_uuid=True), nullable=True)

    cancellation_reason = Column(
        String(100),
        nullable=False
    )

    cancellation_reason_description = Column(
        String(1000),
        nullable=True
    )

    cancellation_charge = Column(
        Numeric(12, 2),
        nullable=False,
        server_default=text("0.00")
    )

    status = Column(
        String(20),
        nullable=False,
        server_default=text("'PENDING'")
    )

    approved_by = Column(UUID(as_uuid=True), nullable=True)

    approved_at = Column(DateTime, nullable=True)

    created_at = Column(
        DateTime,
        nullable=False,
        server_default=text("now()")
    )


# -----------------------------------------------------------------------
# Booking Refund
# -----------------------------------------------------------------------

class BookingRefund(BaseGithub):
    __tablename__ = "booking_refunds"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    booking_id = Column(UUID(as_uuid=True), nullable=False)
    payment_refund_id = Column(UUID(as_uuid=True), nullable=True)

    refund_amount = Column(Numeric(12, 2), nullable=False)
    refund_reason = Column(String(255), nullable=False)

    refund_status = Column(
        String(25),
        nullable=False,
        server_default=text("'PENDING'")
    )

    refund_reference = Column(String(100), nullable=True)
    approved_by = Column(UUID(as_uuid=True), nullable=True)
    approved_at = Column(DateTime, nullable=True)
    refunded_at = Column(DateTime, nullable=True)

    created_at = Column(
        DateTime,
        nullable=False,
        server_default=text("now()")
    )


# -----------------------------------------------------------------------
#  Booking Feedback
# -----------------------------------------------------------------------

class BookingFeedback(BaseGithub):
    __tablename__ = "booking_feedback"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    booking_id = Column(UUID(as_uuid=True), nullable=False)
    customer_id = Column(UUID(as_uuid=True), nullable=False)


    rating = Column(SmallInteger, nullable=False)

    review_title = Column(String(150), nullable=True)
    review_text = Column(String, nullable=True)  # text type - no length limit

    is_verified_booking = Column(Boolean, nullable=True)
    is_published = Column(Boolean, nullable=True)

    created_at = Column(
        DateTime,
        nullable=False,
        server_default=text("now()")
    )

    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=text("now()"),
        onupdate=func.now()
    )


# -----------------------------------------------------------------------
#  Offer
# -----------------------------------------------------------------------


class Offer(BaseGithub):
    __tablename__ = "offers"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    tenant_id = Column(UUID(as_uuid=True), nullable=False)
    store_id = Column(UUID(as_uuid=True), nullable=False)

    offer_name = Column(String(255), nullable=False)

    offer_code = Column(String(100), nullable=False, unique=True)

    offer_type = Column(String(30), nullable=False)

    discount_type = Column(String(30), nullable=False)

    discount_value = Column(Numeric(12, 2), nullable=False)

    maximum_discount_amount = Column(Numeric(12, 2), nullable=True)

    minimum_order_amount = Column(Numeric(12, 2), nullable=True)

    starts_at = Column(DateTime, nullable=False)
    ends_at = Column(DateTime, nullable=False)

    priority = Column(SmallInteger, nullable=True)
    is_active = Column(Boolean, nullable=True)

    approval_status = Column(
        String(20),
        nullable=False,
        server_default=text("'PENDING'")
    )

    created_by = Column(UUID(as_uuid=True), nullable=False)
    approved_by = Column(UUID(as_uuid=True), nullable=True)
    approved_at = Column(DateTime, nullable=True)

    created_at = Column(
        DateTime,
        nullable=False,
        server_default=text("now()")
    )

    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=text("now()"),
        onupdate=func.now()
    )



# -----------------------------------------------------------------------
#  Offer target
# -----------------------------------------------------------------------

class OfferTarget(BaseGithub):
    __tablename__ = "offer_targets"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    offer_id = Column(UUID(as_uuid=True), nullable=False)
    target_type = Column(String(30), nullable=False)
    target_id = Column(UUID(as_uuid=True), nullable=False)

    created_at = Column(
        DateTime,
        nullable=True,
        server_default=text("now()")
    )

# ---------------------------------------------------------------------------
# Coupon
# ---------------------------------------------------------------------------

class Coupon(BaseGithub):
    __tablename__ = "coupons"

    # Primary Key
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    # Foreign Key ID (Offer model will be linked later)
    offer_id = Column(
        UUID(as_uuid=True),
        nullable=False
    )

    # Must be unique across all coupons
    coupon_code = Column(
        String(100),
        nullable=False,
        unique=True
    )

    # Maximum number of times this coupon can be used
    usage_limit = Column(
        Integer,
        nullable=True
    )

    # Maximum number of times one customer can use this coupon
    usage_limit_per_customer = Column(
        Integer,
        nullable=True
    )

    # Restrict coupon to first-time customers only
    first_time_customer_only = Column(
        Boolean,
        nullable=False,
        server_default=text("false")
    )

    created_at = Column(
        DateTime,
        nullable=False,
        server_default=text("now()")
    )

    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=text("now()"),
        onupdate=func.now()
    )

# ---------------------------------------------------------------------------
# Coupon Redemption
# ---------------------------------------------------------------------------

class CouponRedemption(BaseGithub):
    __tablename__ = "coupon_redemptions"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    coupon_id = Column(
        UUID(as_uuid=True),
        nullable=False
    )

    customer_id = Column(
        UUID(as_uuid=True),
        nullable=False
    )

    order_id = Column(
        UUID(as_uuid=True),
        nullable=True
    )

    booking_id = Column(
        UUID(as_uuid=True),
        nullable=True
    )

    discount_amount = Column(
        Numeric(12, 2),
        nullable=False
    )

    redeemed_at = Column(
        DateTime,
        nullable=False,
        server_default=text("now()")
    )


# ---------------------------------------------------------------------------
# Offer Customer Segment
# ---------------------------------------------------------------------------

class OfferCustomerSegment(BaseGithub):
    __tablename__ = "offer_customer_segments"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    offer_id = Column(
        UUID(as_uuid=True),
        nullable=False
    )

    customer_group_id = Column(
        UUID(as_uuid=True),
        nullable=False
    )

    created_at = Column(
        DateTime,
        nullable=False,
        server_default=text("now()")
    )

# ---------------------------------------------------------------------------
# Offer Exclusion
# ---------------------------------------------------------------------------

class OfferExclusion(BaseGithub):
    __tablename__ = "offer_exclusions"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    offer_id = Column(
        UUID(as_uuid=True),
        nullable=False
    )

    entity_type = Column(
        String(30),
        nullable=False
    )

    entity_id = Column(
        UUID(as_uuid=True),
        nullable=False
    )

    created_at = Column(
        DateTime,
        nullable=False,
        server_default=text("now()")
    )

# ---------------------------------------------------------------------------
# Notification
# ---------------------------------------------------------------------------

class Notification(BaseGithub):
    __tablename__ = "notifications"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    tenant_id = Column(
        UUID(as_uuid=True),
        nullable=False
    )

    store_id = Column(
        UUID(as_uuid=True),
        nullable=True
    )

    customer_id = Column(
        UUID(as_uuid=True),
        nullable=True
    )

    entity_type = Column(
        String(30),
        nullable=True
    )

    entity_id = Column(
        UUID(as_uuid=True),
        nullable=True
    )

    notification_type = Column(
        String(30),
        nullable=False
    )

    channel = Column(
        String(30),
        nullable=False
    )

    subject = Column(
        String(255),
        nullable=True
    )

    message = Column(
        Text,
        nullable=False
    )

    scheduled_at = Column(
        DateTime,
        nullable=True
    )

    sent_at = Column(
        DateTime,
        nullable=True
    )

    status = Column(
        String(20),
        nullable=False,
        server_default=text("'PENDING'")
    )

    created_at = Column(
        DateTime,
        nullable=False,
        server_default=text("now()")
    )
class CartItem(BaseGithub):
    __tablename__ = "cart_items"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    cart_id = Column(UUID(as_uuid=True), nullable=False)
    product_id = Column(UUID(as_uuid=True), nullable=False)
    product_variant_id = Column(UUID(as_uuid=True), nullable=True)

    quantity = Column(
        Integer,
        nullable=False,
        server_default=text("1")
    )

    unit_price = Column(Numeric(12, 2), nullable=False)

    discount_amount = Column(
        Numeric(12, 2),
        nullable=True,
        server_default=text("0.00")
    )

    tax_amount = Column(
        Numeric(12, 2),
        nullable=True,
        server_default=text("0.00")
    )

    line_total = Column(Numeric(12, 2), nullable=False)

    added_at = Column(
        DateTime,
        nullable=True,
        server_default=text("now()")
    )

    updated_at = Column(
        DateTime,
        nullable=True,
        server_default=text("now()"),
        onupdate=func.now()
    )