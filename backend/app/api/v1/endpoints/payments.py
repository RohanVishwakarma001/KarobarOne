# ACTIVE payments router — see docs/api-mapping/commerce.md.
#
# Three endpoints, three different trust models:
#   - create-order: customer-facing (checkout trigger), no bearer
#   - verify:       customer-facing (Razorpay Checkout.js success callback),
#                   its ENTIRE security is the HMAC checkout signature
#   - webhook:      Razorpay's own servers call this directly — there is no
#                   user session here at all; its entire security is the
#                   HMAC webhook signature over the raw body
#
# Idempotency: create-order reuses an existing PENDING Payment row for the
# same order instead of minting a second Razorpay order (idempotent create).
# verify short-circuits if the Payment is already SUCCESS (idempotent
# retries from the frontend). webhook relies on GatewayWebhookEvent.event_id
# being UNIQUE — a duplicate delivery hits that constraint and is treated as
# already-processed rather than reapplied.

import uuid
from datetime import datetime, timezone
from decimal import Decimal
from uuid import UUID

from fastapi import APIRouter, Depends, Header, Request, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import getCurrentUserId
from app.core.exceptions import BadRequestError, NotFoundError, UnauthorizedError
from app.core.tenantResolver import getTenantIdAsUUID
from app.db.models.approvals import AuditLog, StatusHistory
from app.db.models.github.gatewayWebhookEvent import GatewayWebhookEvent
from app.db.models.github.order import Order
from app.db.models.github.payment import Payment
from app.db.models.github.paymentMethod import PaymentMethod
from app.db.models.github.paymentRefund import PaymentRefund
from app.db.session import getDb
from app.schemas.commerce import (
    CreateRazorpayOrderRequest,
    CreateRazorpayOrderResponse,
    CreateRefundRequest,
    OrderResponse,
    RefundResponse,
    VerifyRazorpayPaymentRequest,
    VerifyRazorpayPaymentResponse,
)
from app.schemas.common import APIResponse
from app.services.razorpayClient import RazorpayClient, getRazorpayClient

router = APIRouter(prefix="/payments/razorpay", tags=["Payments"])


async def _getOrCreateRazorpayPaymentMethod(db: AsyncSession) -> PaymentMethod:
    result = await db.execute(select(PaymentMethod).where(PaymentMethod.method_code == "RAZORPAY"))
    method = result.scalars().first()
    if method:
        return method
    method = PaymentMethod(method_code="RAZORPAY", method_name="Razorpay", is_online=True, is_active=True)
    db.add(method)
    await db.flush()
    return method


# ── CREATE RAZORPAY ORDER ─────────────────────
@router.post("/create-order", response_model=APIResponse[CreateRazorpayOrderResponse], status_code=status.HTTP_201_CREATED)
async def createRazorpayOrder(
    payload: CreateRazorpayOrderRequest,
    razorpay: RazorpayClient = Depends(getRazorpayClient),
    db: AsyncSession = Depends(getDb),
):
    order = await db.get(Order, payload.orderId)
    if not order or order.tenant_id != payload.tenantId or order.store_id != payload.storeId:
        raise NotFoundError("Order not found")
    if order.order_status != "PENDING":
        raise BadRequestError(f"Order is {order.order_status}, not awaiting payment")

    existingResult = await db.execute(
        select(Payment).where(
            Payment.entity_type == "ORDER", Payment.entity_id == order.id, Payment.payment_status == "PENDING"
        )
    )
    existingPayment = existingResult.scalars().first()
    if existingPayment and existingPayment.payment_reference_number:
        return APIResponse(
            data=CreateRazorpayOrderResponse(
                razorpayOrderId=existingPayment.payment_reference_number,
                razorpayKeyId=razorpay.keyId or "",
                amount=int(round(float(order.total_amount) * 100)),
                currency=order.currency_code,
                paymentId=existingPayment.id,
            ),
            message="Reusing existing pending payment for this order",
        )

    razorpayOrder = razorpay.createOrder(amountRupees=order.total_amount, receipt=order.order_number)
    method = await _getOrCreateRazorpayPaymentMethod(db)

    payment = existingPayment or Payment(
        tenant_id=order.tenant_id,
        store_id=order.store_id,
        entity_type="ORDER",
        entity_id=order.id,
        payment_method_id=method.id,
        currency=order.currency_code,
        payment_status="PENDING",
    )
    payment.amount = order.total_amount
    payment.payment_reference_number = razorpayOrder["id"]
    db.add(payment)
    await db.flush()

    order.payment_id = payment.id
    await db.commit()

    return APIResponse(
        data=CreateRazorpayOrderResponse(
            razorpayOrderId=razorpayOrder["id"],
            razorpayKeyId=razorpay.keyId or "",
            amount=razorpayOrder["amount"],
            currency=razorpayOrder["currency"],
            paymentId=payment.id,
        )
    )


# ── VERIFY CHECKOUT SIGNATURE ──────────────────
@router.post("/verify", response_model=APIResponse[VerifyRazorpayPaymentResponse])
async def verifyRazorpayPayment(
    payload: VerifyRazorpayPaymentRequest,
    razorpay: RazorpayClient = Depends(getRazorpayClient),
    db: AsyncSession = Depends(getDb),
):
    paymentResult = await db.execute(select(Payment).where(Payment.payment_reference_number == payload.razorpayOrderId))
    payment = paymentResult.scalars().first()
    if not payment:
        raise NotFoundError("No payment found for this Razorpay order")

    order = await db.get(Order, payment.entity_id) if payment.entity_type == "ORDER" else None
    if not order:
        raise NotFoundError("Order not found for this payment")

    if payment.payment_status == "SUCCESS":
        # Idempotent: the frontend retried a verify call that already succeeded — don't reprocess.
        return APIResponse(data=VerifyRazorpayPaymentResponse(verified=True, order=order))

    if not razorpay.verifyCheckoutSignature(payload.razorpayOrderId, payload.razorpayPaymentId, payload.razorpaySignature):
        raise UnauthorizedError("Payment signature verification failed")

    payment.payment_status = "SUCCESS"
    payment.payment_date = datetime.now(timezone.utc)

    oldStatus = order.order_status
    order.order_status = "PAID"
    order.payment_status = "SUCCESS"
    db.add(
        StatusHistory(
            tenantId=order.tenant_id,
            entityType="ORDER",
            entityId=order.id,
            oldStatus=oldStatus,
            newStatus="PAID",
            changeReason="Razorpay payment verified",
            changedBy=order.customer_id,
        )
    )
    await db.commit()

    # populate_existing=True + eager model_validate — see the note on
    # orders.py::_loadOrderWithItems for why a plain db.get() here can hand
    # Pydantic an object whose attributes need an unawaited lazy-load.
    order = await db.get(Order, order.id, populate_existing=True)
    return APIResponse(
        data=VerifyRazorpayPaymentResponse(verified=True, order=OrderResponse.model_validate(order)),
        message="Payment verified",
    )


# ── WEBHOOK (Razorpay -> us, server-to-server) ─
@router.post("/webhook", status_code=status.HTTP_200_OK)
async def razorpayWebhook(
    request: Request,
    razorpay: RazorpayClient = Depends(getRazorpayClient),
    db: AsyncSession = Depends(getDb),
    xRazorpaySignature: str = Header(..., alias="X-Razorpay-Signature"),
):
    rawBody = await request.body()
    if not razorpay.verifyWebhookSignature(rawBody, xRazorpaySignature):
        raise UnauthorizedError("Invalid webhook signature")

    payload = await request.json()
    eventId = payload.get("id")
    if not eventId:
        raise BadRequestError("Webhook payload missing 'id'")

    event = GatewayWebhookEvent(
        gateway_name="RAZORPAY",
        event_type=payload.get("event", "unknown"),
        event_id=eventId,
        payload=payload,
        processed=False,
    )
    db.add(event)
    try:
        await db.commit()
    except IntegrityError:
        # event_id is UNIQUE — this delivery was already recorded (Razorpay
        # retries webhooks on any non-2xx, so duplicates are expected).
        await db.rollback()
        return {"status": "already_processed"}

    eventType = payload.get("event", "")
    if eventType in ("payment.captured", "order.paid"):
        entity = payload.get("payload", {}).get("payment", {}).get("entity", {})
        razorpayOrderId = entity.get("order_id")
        if razorpayOrderId:
            paymentResult = await db.execute(select(Payment).where(Payment.payment_reference_number == razorpayOrderId))
            payment = paymentResult.scalars().first()
            if payment and payment.payment_status != "SUCCESS":
                payment.payment_status = "SUCCESS"
                payment.payment_date = datetime.now(timezone.utc)
                order = await db.get(Order, payment.entity_id) if payment.entity_type == "ORDER" else None
                if order and order.order_status == "PENDING":
                    oldStatus = order.order_status
                    order.order_status = "PAID"
                    order.payment_status = "SUCCESS"
                    db.add(
                        StatusHistory(
                            tenantId=order.tenant_id, entityType="ORDER", entityId=order.id,
                            oldStatus=oldStatus, newStatus="PAID", changeReason="Razorpay webhook: payment captured",
                            changedBy=order.customer_id,
                        )
                    )

    event.processed = True
    event.processed_at = datetime.now(timezone.utc)
    await db.commit()
    return {"status": "processed"}


# ── REFUND (staff only) ───────────────────────
@router.post("/{paymentId}/refund", response_model=APIResponse[RefundResponse], status_code=status.HTTP_201_CREATED)
async def refundPayment(
    paymentId: UUID,
    payload: CreateRefundRequest,
    razorpay: RazorpayClient = Depends(getRazorpayClient),
    tenantId: UUID = Depends(getTenantIdAsUUID),
    staffUserId: str = Depends(getCurrentUserId),
    db: AsyncSession = Depends(getDb),
):
    payment = await db.get(Payment, paymentId)
    if not payment or payment.tenant_id != tenantId:
        raise NotFoundError("Payment not found")
    if payment.payment_status != "SUCCESS":
        raise BadRequestError("Only a successful payment can be refunded")

    razorpayRefund = razorpay.refund(payload.razorpayPaymentId, float(payload.amount) if payload.amount else None)

    refund = PaymentRefund(
        payment_id=payment.id,
        refund_reference=razorpayRefund["id"],
        refund_amount=payload.amount or payment.amount,
        refund_reason=payload.reason,
        refund_status="PROCESSED" if razorpayRefund.get("status") == "processed" else "PENDING",
        refunded_at=datetime.now(timezone.utc) if razorpayRefund.get("status") == "processed" else None,
    )
    db.add(refund)

    order = None
    if payment.entity_type == "ORDER":
        order = await db.get(Order, payment.entity_id)
        if order:
            order.payment_status = "REFUNDED" if refund.refund_amount >= payment.amount else "PARTIALLY_REFUNDED"

    await db.commit()
    await db.refresh(refund)
    # Eagerly validate before the audit log's own nested commit — see the
    # matching comment in orders.py::updateOrderStatus for why.
    response = APIResponse(data=RefundResponse.model_validate(refund), message="Refund processed")

    try:
        db.add(
            AuditLog(
                tenantId=tenantId, entityType="ORDER", entityId=order.id if order else payment.id,
                actionType="REFUND", newValue={"refundAmount": str(refund.refund_amount), "reason": payload.reason},
                performedBy=uuid.UUID(staffUserId),
            )
        )
        await db.commit()
    except Exception:
        await db.rollback()

    return response
