# ================================================================================
# FILE: db/modelsRegistryGithub.py — Model Registry for the /github Commerce Module
# ================================================================================
# Why this file is used:
#   - The /github commerce module's models inherit from BaseGithub, a separate
#     DeclarativeBase from the main app's Base (app/db/base.py). Alembic's
#     autogenerate only sees tables registered on a metadata object it is told
#     to target, so this file imports every github model to register its table
#     on BaseGithub.metadata — mirroring app/db/modelsRegistry.py for the main Base.
# ================================================================================
from app.db.baseGithub import BaseGithub

from app.db.models.github.appointment import Appointment
from app.db.models.github.cart import Cart
from app.db.models.github.customer import Customer as GithubCustomer
from app.db.models.github.gatewaySettlement import GatewaySettlement
from app.db.models.github.gatewaySettlementItem import GatewaySettlementItem
from app.db.models.github.gatewayWebhookEvent import GatewayWebhookEvent
from app.db.models.github.order import Order
from app.db.models.github.orderItem import OrderItem
from app.db.models.github.payment import Payment
from app.db.models.github.paymentAuditLog import PaymentAuditLog
from app.db.models.github.paymentMethod import PaymentMethod
from app.db.models.github.paymentReconciliationBatch import PaymentReconciliationBatch
from app.db.models.github.paymentReconciliationItem import PaymentReconciliationItem
from app.db.models.github.paymentRefund import PaymentRefund
from app.db.models.github.product import Product
from app.db.models.github.revenueSummary import RevenueSummary
from app.db.models.github.sellerPayout import SellerPayout
from app.db.models.github.shipment import Shipment
from app.db.models.github.shipmentRequest import ShipmentRequest
from app.db.models.github.shippingException import ShippingException
from app.db.models.github.shippingPartner import ShippingPartner
from app.db.models.github.shippingProfile import ShippingProfile
from app.db.models.github.shippingProfileZone import ShippingProfileZone
from app.db.models.github.shippingRate import ShippingRate
from app.db.models.github.shippingZone import ShippingZone
from app.db.models.github.subscriptionPayment import SubscriptionPayment
from app.db.models.github.user import User as GithubUser
from app.db.models.github.models import (
    Wishlist, WishlistItem, SavedForLater, AbandonedCart, CartCoupon,
    RecentlyViewedProduct, ProductCompareList, ProductCompareItem,
    OrderCancellation, OrderReturn, OrderRefund, Booking, BookingCancellation,
    BookingRefund, BookingFeedback, Offer, OfferTarget, Coupon, CouponRedemption,
    OfferCustomerSegment, OfferExclusion, Notification, CartItem,
)

# Tables that collide by name with tables already owned/migrated by another
# module (main app's `customers`/`users`). `orders` also collides with
# customerEngine's EngineCustomerOrder (on the main Base) but has no live
# table yet, so it isn't listed here.
#
# alembic/env.py does NOT import this module day-to-day — Base.metadata and
# BaseGithub.metadata can't be merged into one target_metadata list while the
# `orders` collision exists (Alembic raises on duplicate table keys across
# metadata objects before any include_object filter runs). To generate a
# migration for a NEW/changed table in this module, temporarily point
# alembic/env.py's target_metadata at BaseGithub.metadata alone (see the
# "add github commerce module tables" migration for the pattern used), add an
# include_object filter excluding COLLIDING_TABLE_NAMES, run
# `alembic revision --autogenerate`, hand-trim any unrelated drop_table/
# create_table noise autogenerate emits for tables outside this metadata,
# apply it, then revert env.py.
COLLIDING_TABLE_NAMES = {"customers", "users"}
