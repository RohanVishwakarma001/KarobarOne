# ACTIVE orders router — see docs/api-mapping/commerce.md.
# Order creation is customer-facing (same no-customer-JWT reasoning as
# cart.py); status transitions and the refund log are staff-bearer-gated,
# matching app/api/v1/endpoints/customers.py's admin-vs-storefront split.

import uuid
from datetime import datetime, timezone
from decimal import Decimal
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import getCurrentUserId
from app.core.exceptions import BadRequestError, NotFoundError
from app.core.tenantResolver import getTenantIdAsUUID
from app.db.models.approvals import AuditLog, StatusHistory
from app.db.models.github.cart import Cart
from app.db.models.github.order import Order
from app.db.models.github.orderItem import OrderItem
from app.db.session import getDb
from app.schemas.commerce import (
    ORDER_STATUS_TRANSITIONS,
    CreateOrderRequest,
    OrderItemResponse,
    OrderResponse,
    OrderStatusEventResponse,
    UpdateOrderStatusRequest,
)
from app.schemas.common import APIResponse

router = APIRouter(prefix="/orders", tags=["Orders"])


async def _loadOrderWithItems(db: AsyncSession, orderId: UUID) -> Order:
    # populate_existing=True: without it, db.get() on an identity-mapped
    # instance that's expired (e.g. right after a commit — expire_on_commit
    # defaults to True) can hand back an object whose attributes only
    # refresh via SQLAlchemy's normal lazy-load path. That path needs an
    # awaited greenlet; Pydantic's plain getattr() during response
    # validation can't provide one, so it dies with "MissingGreenlet"
    # instead of the SELECT that should have run right here.
    order = await db.get(Order, orderId, populate_existing=True)
    if not order:
        raise NotFoundError("Order not found")
    itemsResult = await db.execute(select(OrderItem).where(OrderItem.order_id == orderId))
    order.items = itemsResult.scalars().all()  # type: ignore[attr-defined]
    return order


async def _logAuditEntry(db: AsyncSession, *, tenantId: UUID, entityId: UUID, actionType: str, oldValue: dict | None, newValue: dict | None, performedBy: UUID) -> None:
    """Best-effort — see the note on this same pattern in productsPorted/routers/products.py; must never break the actual order operation."""
    try:
        db.add(AuditLog(tenantId=tenantId, entityType="ORDER", entityId=entityId, actionType=actionType, oldValue=oldValue, newValue=newValue, performedBy=performedBy))
        await db.commit()
    except Exception:
        await db.rollback()


# ── CREATE ORDER (checkout) ──────────────────
@router.post("/", response_model=APIResponse[OrderResponse], status_code=status.HTTP_201_CREATED)
async def createOrder(payload: CreateOrderRequest, db: AsyncSession = Depends(getDb)):
    subtotal = sum((i.unitPrice * i.quantity for i in payload.items), Decimal("0.00"))
    itemTax = sum((i.taxAmount for i in payload.items), Decimal("0.00"))
    itemDiscount = sum((i.discountAmount for i in payload.items), Decimal("0.00"))
    total = max(subtotal + itemTax - itemDiscount + payload.shippingAmount, Decimal("0.00"))

    order = Order(
        tenant_id=payload.tenantId,
        store_id=payload.storeId,
        customer_id=payload.customerId,
        cart_id=payload.cartId,
        order_number=f"ORD-{uuid.uuid4().hex[:10].upper()}",
        billing_address_id=payload.billingAddressId,
        shipping_address_id=payload.shippingAddressId,
        order_status="PENDING",
        payment_status="PENDING",
        fulfillment_status="PENDING",
        subtotal_amount=subtotal,
        discount_amount=itemDiscount,
        tax_amount=itemTax,
        shipping_amount=payload.shippingAmount,
        total_amount=total,
        currency_code="INR",
        customer_note=payload.customerNote,
        placed_at=datetime.now(timezone.utc),
    )
    db.add(order)
    await db.flush()

    for i in payload.items:
        db.add(
            OrderItem(
                order_id=order.id,
                product_id=i.productId,
                product_variant_id=i.productVariantId,
                sku=i.sku,
                product_name=i.productName,
                variant_name=i.variantName,
                quantity=i.quantity,
                unit_price=i.unitPrice,
                discount_amount=i.discountAmount,
                tax_amount=i.taxAmount,
                line_total=(i.unitPrice * i.quantity) + i.taxAmount - i.discountAmount,
            )
        )

    if payload.cartId:
        cart = await db.get(Cart, payload.cartId)
        if cart:
            cart.cart_status = "CONVERTED"

    db.add(StatusHistory(tenantId=payload.tenantId, entityType="ORDER", entityId=order.id, oldStatus=None, newStatus="PENDING", changedBy=payload.customerId))

    await db.commit()
    order = await _loadOrderWithItems(db, order.id)
    return APIResponse(data=order, message="Order placed")


# ── GET ORDER (guest-trackable by id, no bearer required) ────
@router.get("/{orderId}", response_model=APIResponse[OrderResponse])
async def getOrder(orderId: UUID, db: AsyncSession = Depends(getDb)):
    order = await _loadOrderWithItems(db, orderId)
    return APIResponse(data=order)


# ── ORDER STATUS TIMELINE (public — powers the frontend's tracking widget) ────
@router.get("/{orderId}/history", response_model=APIResponse[list[OrderStatusEventResponse]])
async def getOrderStatusHistory(orderId: UUID, db: AsyncSession = Depends(getDb)):
    result = await db.execute(
        select(StatusHistory)
        .where(StatusHistory.entityType == "ORDER", StatusHistory.entityId == orderId)
        .order_by(StatusHistory.changedAt.asc())
    )
    return APIResponse(data=result.scalars().all())


# ── LIST ORDERS (staff, tenant-scoped) ────────
@router.get("/", response_model=APIResponse[list[OrderResponse]])
async def listOrders(
    storeId: Optional[UUID] = Query(None),
    customerId: Optional[UUID] = Query(None),
    orderStatus: Optional[str] = Query(None, alias="status"),
    tenantId: UUID = Depends(getTenantIdAsUUID),
    _staffUserId: str = Depends(getCurrentUserId),
    db: AsyncSession = Depends(getDb),
):
    query = select(Order).where(Order.tenant_id == tenantId)
    if storeId:
        query = query.where(Order.store_id == storeId)
    if customerId:
        query = query.where(Order.customer_id == customerId)
    if orderStatus:
        query = query.where(Order.order_status == orderStatus)
    query = query.order_by(Order.created_at.desc())

    result = await db.execute(query)
    orders = result.scalars().all()
    for order in orders:
        itemsResult = await db.execute(select(OrderItem).where(OrderItem.order_id == order.id))
        order.items = itemsResult.scalars().all()  # type: ignore[attr-defined]
    return APIResponse(data=orders)


# ── UPDATE ORDER STATUS (staff, validated state machine) ────
@router.patch("/{orderId}/status", response_model=APIResponse[OrderResponse])
async def updateOrderStatus(
    orderId: UUID,
    payload: UpdateOrderStatusRequest,
    tenantId: UUID = Depends(getTenantIdAsUUID),
    staffUserId: str = Depends(getCurrentUserId),
    db: AsyncSession = Depends(getDb),
):
    order = await db.get(Order, orderId)
    if not order or order.tenant_id != tenantId:
        raise NotFoundError("Order not found")

    allowedNext = ORDER_STATUS_TRANSITIONS.get(order.order_status, set())
    if payload.status not in allowedNext:
        raise BadRequestError(f"Cannot move an order from {order.order_status} to {payload.status}")

    oldStatus = order.order_status
    order.order_status = payload.status
    if payload.status == "PAID":
        order.payment_status = "SUCCESS"
    elif payload.status == "PROCESSING":
        order.fulfillment_status = "PROCESSING"
    elif payload.status == "SHIPPED":
        order.fulfillment_status = "SHIPPED"
    elif payload.status == "DELIVERED":
        order.fulfillment_status = "DELIVERED"
    elif payload.status == "CANCELLED":
        order.fulfillment_status = "CANCELLED"
        if order.payment_status == "PENDING":
            order.payment_status = "CANCELLED"

    db.add(
        StatusHistory(
            tenantId=tenantId,
            entityType="ORDER",
            entityId=order.id,
            oldStatus=oldStatus,
            newStatus=payload.status,
            changeReason=payload.reason,
            changedBy=uuid.UUID(staffUserId),
        )
    )
    await db.commit()

    # Eagerly validate into OrderResponse BEFORE the best-effort audit log
    # below — that helper does its own commit/rollback, which expires every
    # ORM instance in this session (SQLAlchemy's default expire_on_commit).
    # `APIResponse(data=order, ...)` alone would just carry the *ORM object*
    # through unvalidated — FastAPI only reads its attributes later, when
    # serializing the return value, by which point the audit log's commit
    # may have expired them. model_validate() here forces every attribute
    # read to happen now, while the session is definitely still open.
    order = await _loadOrderWithItems(db, orderId)
    response = APIResponse(data=OrderResponse.model_validate(order), message=f"Order moved to {payload.status}")

    await _logAuditEntry(
        db,
        tenantId=tenantId,
        entityId=order.id,
        actionType="UPDATE",
        oldValue={"orderStatus": oldStatus},
        newValue={"orderStatus": payload.status, "reason": payload.reason},
        performedBy=uuid.UUID(staffUserId),
    )

    return response
