from fastapi import APIRouter

githubRouter = APIRouter(
    prefix="/github",
    tags=["GitHub Ported Modules"],
)

# ── Carts & Checkout ──
from .cartRouter import router as cartRouter
from .cartItemRouter import router as cartItemRouter
from .cartCouponRouter import router as cartCouponRouter
from .abandonedCartRouter import router as abandonedCartRouter
from .checkoutRouter import router as checkoutRouter

# ── Orders & Statuses ──
from .orderRouter import router as orderRouter
from .orderItemRouter import router as orderItemRouter
from .orderStatusRouter import router as orderStatusRouter
from .orderCancellationRouter import router as orderCancellationRouter
from .orderReturnRouter import router as orderReturnRouter
from .orderRefundRouter import router as orderRefundRouter

# ── Payments, Methods & Audits ──
from .paymentRouter import router as paymentRouter
from .paymentMethodRouter import router as paymentMethodRouter
from .paymentRefundRouter import router as paymentRefundRouter
from .paymentAuditLogRouter import router as paymentAuditLogRouter
from .subscriptionPaymentRouter import router as subscriptionPaymentRouter

# ── Gateway & Reconciliation ──
from .gatewaySettlementRouter import router as gatewaySettlementRouter
from .gatewaySettlementItemRouter import router as gatewaySettlementItemRouter
from .gatewayWebhookEventRouter import router as gatewayWebhookEventRouter
from .paymentReconciliationBatchRouter import router as paymentReconciliationBatchRouter
from .paymentReconciliationItemRouter import router as paymentReconciliationItemRouter
from .revenueSummaryRouter import router as revenueSummaryRouter

# ── Commission & Seller Payouts ──
from .commissionRouter import router as commissionRouter
from .sellerPayoutRouter import router as sellerPayoutRouter

# ── Shipping & Fulfillment ──
from .shippingProfileRouter import router as shippingProfileRouter
from .shippingZoneRouter import router as shippingZoneRouter
from .shippingRateRouter import router as shippingRateRouter
from .shippingProfileZoneRouter import router as shippingProfileZoneRouter
from .shippingPartnerRouter import router as shippingPartnerRouter
from .shipmentRouter import router as shipmentRouter
from .shipmentRequestRouter import router as shipmentRequestRouter
from .shippingExceptionRouter import router as shippingExceptionRouter
from .shiprocketRouter import router as shiprocketRouter

# ── Bookings & Appointments ──
from .bookingRouter import router as bookingRouter
from .bookingCancellationRouter import router as bookingCancellationRouter
from .bookingRefundRouter import router as bookingRefundRouter
from .bookingFeedbackRouter import router as bookingFeedbackRouter
from .appointmentRouter import router as appointmentRouter
from .calendarRouter import router as calendarRouter

# ── Offers & Coupons ──
from .offerRouter import router as offerRouter
from .offerTargetRouter import router as offerTargetRouter
from .offerCustomerSegmentRouter import router as offerCustomerSegmentRouter
from .offerExclusionRouter import router as offerExclusionRouter
from .couponRouter import router as couponRouter
from .couponRedemptionRouter import router as couponRedemptionRouter

# ── Customers, Auth & Notifications ──
from .customerRouter import router as customerRouter
from .authRouter import router as authRouter
from .notificationRouter import router as notificationRouter
from .otpRouter import router as otpRouter

# ── Wishlist & Product Engagement ──
from .wishlistRouter import router as wishlistRouter
from .wishlistItemRouter import router as wishlistItemRouter
from .savedForLaterRouter import router as savedForLaterRouter
from .recentlyViewedProductRouter import router as recentlyViewedProductRouter
from .productCompareListRouter import router as productCompareListRouter
from .productCompareItemRouter import router as productCompareItemRouter
from .productRouter import router as productRouter

# ── Mount Routers ──
# customerRouter, authRouter, and the cart/order/payment routers below are
# intentionally NOT in this list — see the two deprecated blocks at the
# bottom. customerRouter/authRouter: independent duplicates of the ACTIVE
# /api/v1/customers and /api/v1/auth routers (customerRouter maps its own
# SQLAlchemy model onto the *same* physical `customers` table via a separate
# declarative base — see app/db/models/github/customer.py vs
# app/db/models/customers.py — and authRouter runs a fully synchronous
# session path against its own `users` table). Neither is enforced by a DB
# foreign key from cart/order (customer_id there is a bare UUID column), so
# they're not load-bearing for the rest of this module. See
# docs/api-mapping/customers.md and docs/api-mapping/auth.md.
routers = [
    orderReturnRouter,
    paymentAuditLogRouter, subscriptionPaymentRouter,
    gatewaySettlementRouter, gatewaySettlementItemRouter, gatewayWebhookEventRouter,
    paymentReconciliationBatchRouter, paymentReconciliationItemRouter, revenueSummaryRouter,
    commissionRouter, sellerPayoutRouter,
    shippingProfileRouter, shippingZoneRouter, shippingRateRouter, shippingProfileZoneRouter,
    shippingPartnerRouter, shipmentRouter, shipmentRequestRouter, shippingExceptionRouter, shiprocketRouter,
    bookingRouter, bookingCancellationRouter, bookingRefundRouter, bookingFeedbackRouter, appointmentRouter, calendarRouter,
    offerRouter, offerTargetRouter, offerCustomerSegmentRouter, offerExclusionRouter,
    couponRouter, couponRedemptionRouter,
    notificationRouter, otpRouter,
    wishlistRouter, wishlistItemRouter, savedForLaterRouter, recentlyViewedProductRouter,
    productCompareListRouter, productCompareItemRouter, productRouter,
]

for r in routers:
    githubRouter.include_router(r)

# DEPRECATED — duplicate customer/auth data paths, see block comment above.
githubRouter.include_router(customerRouter, deprecated=True)
githubRouter.include_router(authRouter, deprecated=True)

# DEPRECATED — superseded by the ACTIVE /api/v1/{cart,orders,payments}
# routers (app/api/v1/endpoints/{cart,orders,payments}.py): async, tenant-
# validated, staff-bearer-gated status transitions, a real Razorpay webhook
# with HMAC verification and idempotency, and no silent mock-fallback on
# gateway failure (see app/services/razorpayClient.py vs the sync/unscoped/
# fail-open app/services/github/razorpayService.py these used). Kept mounted
# — not removed — since existing carts/orders/payments created through these
# read/write the same physical tables the ACTIVE routers use, so in-flight
# data isn't orphaned. orderReturnRouter, paymentAuditLogRouter,
# subscriptionPaymentRouter and the gateway/reconciliation routers above are
# NOT superseded (no ACTIVE equivalent exists yet) and stay ACTIVE.
# See docs/api-mapping/commerce.md.
for r in [
    cartRouter, cartItemRouter, cartCouponRouter, abandonedCartRouter, checkoutRouter,
    orderRouter, orderItemRouter, orderStatusRouter, orderCancellationRouter,
    paymentRouter, paymentMethodRouter, paymentRefundRouter,
]:
    githubRouter.include_router(r, deprecated=True)