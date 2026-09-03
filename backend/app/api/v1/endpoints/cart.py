# ACTIVE cart/checkout router — see docs/api-mapping/commerce.md.
#
# Reuses the existing github-ported tables (carts, cart_items, cart_coupons,
# coupons, offers, coupon_redemptions, abandoned_carts) rather than new ones,
# through the main app's async session instead of app/api/v1/endpoints/github/
# cartRouter.py's sync, unauthenticated, unscoped one.
#
# Cart/checkout is inherently a storefront-anonymous flow (there's no
# customer JWT anywhere in this codebase — see docs/api-mapping/auth.md), so
# tenant scoping here comes from tenantId/storeId being required request
# fields, validated against every row touched, rather than a bearer token.
# Order status transitions and refunds (orders.py, payments.py) ARE
# staff-bearer-gated, since only merchants should move fulfillment state.

from datetime import datetime, timedelta, timezone
from decimal import Decimal
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import BadRequestError, ConflictError, NotFoundError
from app.db.session import getDb
from app.db.models.github.cart import Cart
from app.db.models.github.models import AbandonedCart, CartCoupon, CartItem, Coupon, CouponRedemption, Offer
from app.schemas.commerce import (
    AddCartItemRequest,
    ApplyCouponRequest,
    ApplyCouponResponse,
    CartResponse,
    UpdateCartItemRequest,
)
from app.schemas.common import APIResponse

router = APIRouter(prefix="/cart", tags=["Cart"])

DEFAULT_CART_TTL = timedelta(days=14)


async def _getOrCreateActiveCart(
    db: AsyncSession, tenantId: UUID, storeId: UUID, customerId: Optional[UUID], sessionId: Optional[str]
) -> Cart:
    if not customerId and not sessionId:
        raise BadRequestError("customerId or sessionId is required to identify a cart")

    query = select(Cart).where(
        Cart.tenant_id == tenantId, Cart.store_id == storeId, Cart.cart_status == "ACTIVE"
    )
    query = query.where(Cart.customer_id == customerId) if customerId else query.where(Cart.session_id == sessionId)
    result = await db.execute(query)
    cart = result.scalars().first()
    if cart:
        return cart

    cart = Cart(
        tenant_id=tenantId,
        store_id=storeId,
        customer_id=customerId,
        session_id=sessionId,
        cart_status="ACTIVE",
        subtotal_amount=Decimal("0.00"),
        discount_amount=Decimal("0.00"),
        tax_amount=Decimal("0.00"),
        shipping_amount=Decimal("0.00"),
        total_amount=Decimal("0.00"),
        currency_code="INR",
        expires_at=datetime.now(timezone.utc) + DEFAULT_CART_TTL,
    )
    db.add(cart)
    await db.flush()
    return cart


async def _recalculateCartTotals(db: AsyncSession, cart: Cart) -> None:
    itemsResult = await db.execute(select(CartItem).where(CartItem.cart_id == cart.id))
    items = itemsResult.scalars().all()

    subtotal = sum((item.unit_price * item.quantity for item in items), Decimal("0.00"))
    itemTax = sum((item.tax_amount or Decimal("0.00") for item in items), Decimal("0.00"))
    itemDiscount = sum((item.discount_amount or Decimal("0.00") for item in items), Decimal("0.00"))

    couponResult = await db.execute(select(CartCoupon).where(CartCoupon.cart_id == cart.id))
    coupons = couponResult.scalars().all()
    couponDiscount = sum((c.discount_amount for c in coupons), Decimal("0.00"))

    cart.subtotal_amount = subtotal
    cart.tax_amount = itemTax
    cart.discount_amount = itemDiscount + couponDiscount
    cart.total_amount = max(subtotal + itemTax - cart.discount_amount + cart.shipping_amount, Decimal("0.00"))
    cart.last_activity_at = datetime.now(timezone.utc)
    await db.flush()


async def _loadCartWithItems(db: AsyncSession, cartId: UUID) -> Cart:
    # populate_existing=True — see the identical note on
    # orders.py::_loadOrderWithItems; without it, a cart already in this
    # session's identity map (e.g. just committed) can hand back
    # expired attributes that only refresh via a lazy-load Pydantic's
    # synchronous getattr() can't await, raising MissingGreenlet instead.
    cart = await db.get(Cart, cartId, populate_existing=True)
    if not cart:
        raise NotFoundError("Cart not found")
    itemsResult = await db.execute(select(CartItem).where(CartItem.cart_id == cartId))
    cart.items = itemsResult.scalars().all()  # type: ignore[attr-defined]
    return cart


# ── GET OR CREATE ACTIVE CART ────────────────
@router.get("/", response_model=APIResponse[CartResponse])
async def getCart(
    tenantId: UUID,
    storeId: UUID,
    customerId: Optional[UUID] = Query(None),
    sessionId: Optional[str] = Query(None),
    db: AsyncSession = Depends(getDb),
):
    cart = await _getOrCreateActiveCart(db, tenantId, storeId, customerId, sessionId)
    await db.commit()
    cart = await _loadCartWithItems(db, cart.id)
    return APIResponse(data=cart)


# ── ADD ITEM ──────────────────────────────────
@router.post("/items", response_model=APIResponse[CartResponse], status_code=status.HTTP_201_CREATED)
async def addCartItem(
    payload: AddCartItemRequest,
    tenantId: UUID,
    storeId: UUID,
    customerId: Optional[UUID] = Query(None),
    sessionId: Optional[str] = Query(None),
    unitPrice: Decimal = Query(..., ge=0, description="Server trusts the caller's price snapshot here (no unified catalog price source across product systems yet — see docs/api-mapping/catalog.md); do not read this value back for anything security-sensitive."),
    db: AsyncSession = Depends(getDb),
):
    cart = await _getOrCreateActiveCart(db, tenantId, storeId, customerId, sessionId)

    existingResult = await db.execute(
        select(CartItem).where(
            CartItem.cart_id == cart.id,
            CartItem.product_id == payload.productId,
            CartItem.product_variant_id == payload.productVariantId,
        )
    )
    existingItem = existingResult.scalars().first()
    if existingItem:
        existingItem.quantity += payload.quantity
        existingItem.line_total = existingItem.unit_price * existingItem.quantity
    else:
        item = CartItem(
            cart_id=cart.id,
            product_id=payload.productId,
            product_variant_id=payload.productVariantId,
            quantity=payload.quantity,
            unit_price=unitPrice,
            discount_amount=Decimal("0.00"),
            tax_amount=Decimal("0.00"),
            line_total=unitPrice * payload.quantity,
        )
        db.add(item)

    await _recalculateCartTotals(db, cart)
    await db.commit()
    cart = await _loadCartWithItems(db, cart.id)
    return APIResponse(data=cart, message="Item added to cart")


# ── UPDATE ITEM QUANTITY ─────────────────────
@router.patch("/items/{itemId}", response_model=APIResponse[CartResponse])
async def updateCartItem(itemId: UUID, payload: UpdateCartItemRequest, db: AsyncSession = Depends(getDb)):
    item = await db.get(CartItem, itemId)
    if not item:
        raise NotFoundError("Cart item not found")

    item.quantity = payload.quantity
    item.line_total = item.unit_price * payload.quantity - (item.discount_amount or Decimal("0.00"))
    await db.flush()

    cart = await db.get(Cart, item.cart_id)
    if not cart:
        raise NotFoundError("Cart not found")
    await _recalculateCartTotals(db, cart)
    await db.commit()
    cart = await _loadCartWithItems(db, cart.id)
    return APIResponse(data=cart, message="Cart updated")


# ── REMOVE ITEM ───────────────────────────────
@router.delete("/items/{itemId}", response_model=APIResponse[CartResponse])
async def removeCartItem(itemId: UUID, db: AsyncSession = Depends(getDb)):
    item = await db.get(CartItem, itemId)
    if not item:
        raise NotFoundError("Cart item not found")
    cartId = item.cart_id
    await db.delete(item)
    await db.flush()

    cart = await db.get(Cart, cartId)
    if not cart:
        raise NotFoundError("Cart not found")
    await _recalculateCartTotals(db, cart)
    await db.commit()
    cart = await _loadCartWithItems(db, cart.id)
    return APIResponse(data=cart, message="Item removed")


# ── APPLY COUPON ──────────────────────────────
@router.post("/{cartId}/coupon", response_model=APIResponse[ApplyCouponResponse])
async def applyCoupon(cartId: UUID, payload: ApplyCouponRequest, db: AsyncSession = Depends(getDb)):
    cart = await db.get(Cart, cartId)
    if not cart:
        raise NotFoundError("Cart not found")

    couponResult = await db.execute(select(Coupon).where(Coupon.coupon_code == payload.couponCode))
    coupon = couponResult.scalars().first()
    if not coupon:
        raise NotFoundError("Coupon not found")

    offer = await db.get(Offer, coupon.offer_id)
    if not offer or offer.tenant_id != cart.tenant_id:
        raise NotFoundError("Coupon not found")

    now = datetime.now(timezone.utc).replace(tzinfo=None)
    if not offer.is_active or offer.approval_status != "APPROVED":
        raise BadRequestError("This coupon is not currently active")
    if not (offer.starts_at <= now <= offer.ends_at):
        raise BadRequestError("This coupon is not valid right now")

    # Recompute the pre-coupon subtotal fresh (don't trust cart.subtotal_amount mid-edit)
    itemsResult = await db.execute(select(CartItem).where(CartItem.cart_id == cart.id))
    subtotal = sum((i.unit_price * i.quantity for i in itemsResult.scalars().all()), Decimal("0.00"))
    if offer.minimum_order_amount and subtotal < offer.minimum_order_amount:
        raise BadRequestError(f"Minimum order amount for this coupon is {offer.minimum_order_amount}")

    if coupon.usage_limit is not None:
        usedCount = await db.scalar(
            select(func.count()).select_from(CouponRedemption).where(CouponRedemption.coupon_id == coupon.id)
        )
        if (usedCount or 0) >= coupon.usage_limit:
            raise ConflictError("This coupon has reached its usage limit")

    if coupon.usage_limit_per_customer is not None:
        perCustomerCount = await db.scalar(
            select(func.count())
            .select_from(CouponRedemption)
            .where(CouponRedemption.coupon_id == coupon.id, CouponRedemption.customer_id == payload.customerId)
        )
        if (perCustomerCount or 0) >= coupon.usage_limit_per_customer:
            raise ConflictError("You've already used this coupon the maximum number of times")

    # Server-computed discount — never trust a client-supplied amount here.
    if offer.discount_type == "PERCENTAGE":
        discount = subtotal * (offer.discount_value / Decimal("100"))
        if offer.maximum_discount_amount:
            discount = min(discount, offer.maximum_discount_amount)
    else:  # FLAT
        discount = offer.discount_value
    discount = min(discount, subtotal).quantize(Decimal("0.01"))

    existingCouponResult = await db.execute(select(CartCoupon).where(CartCoupon.cart_id == cart.id))
    for existing in existingCouponResult.scalars().all():
        await db.delete(existing)
    await db.flush()

    cartCoupon = CartCoupon(cart_id=cart.id, coupon_id=coupon.id, discount_amount=discount)
    db.add(cartCoupon)

    await _recalculateCartTotals(db, cart)
    await db.commit()

    cart = await _loadCartWithItems(db, cart.id)
    return APIResponse(data=ApplyCouponResponse(couponCode=coupon.coupon_code, discountAmount=discount, cart=cart))


# ── ABANDONED CART TRACKING ───────────────────
# Called by the frontend on checkout-page unload / cart-idle timeout — not a
# background job (this codebase has no task scheduler wired up). A cron/job
# to sweep ACTIVE carts idle past a threshold into ABANDONED would be a
# natural follow-up, out of scope here.
@router.post("/{cartId}/mark-abandoned", status_code=status.HTTP_204_NO_CONTENT)
async def markCartAbandoned(cartId: UUID, db: AsyncSession = Depends(getDb)):
    cart = await db.get(Cart, cartId)
    if not cart:
        raise NotFoundError("Cart not found")
    if cart.cart_status != "ACTIVE":
        return

    cart.cart_status = "ABANDONED"
    existingResult = await db.execute(select(AbandonedCart).where(AbandonedCart.cart_id == cartId))
    if not existingResult.scalars().first():
        db.add(AbandonedCart(cart_id=cartId, customer_id=cart.customer_id, recovery_status="PENDING"))
    await db.commit()
