import hmac
from datetime import datetime, timezone

from fastapi import APIRouter, Body, Depends, Header, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers.github.shiprocketController import (
    shiprocketController,
)
from app.core.config import getSettings
from app.core.configGithub import SHIPROCKET_WEBHOOK_TOKEN
from app.core.exceptions import UnauthorizedError
from app.db.models.approvals import StatusHistory
from app.db.models.github.order import Order
from app.db.models.github.shipment import Shipment
from app.db.session import getDb

from app.schemas.github.shiprocketSchema import (
    CreateOrderRequest,
    ServiceabilityRequest,
    CourierRecommendationRequest,
    GenerateAwbRequest,
    PickupRequest,
    LabelRequest,
    InvoiceRequest,
    ManifestRequest,
    UpdateOrderRequest,
    PickupLocationRequest,
    NdrActionRequest,
    ShiprocketWebhookPayload,
)

router = APIRouter(
    prefix="/shiprocket",
    tags=["Shiprocket"],
)

# Shiprocket's own status vocabulary -> the 5-step canonical timeline the
# frontend renders (Ordered -> Packed -> In Transit -> Out for Delivery ->
# Delivered). Unmapped/unexpected values pass through unchanged rather than
# being dropped, so a status this table doesn't know about is still recorded
# (just won't map onto one of the 5 timeline steps).
SHIPROCKET_STATUS_MAP: dict[str, str] = {
    "NEW": "ORDERED",
    "INVOICED": "ORDERED",
    "READY TO SHIP": "PACKED",
    "PICKUP SCHEDULED": "PACKED",
    "PICKUP GENERATED": "PACKED",
    "PICKED UP": "PACKED",
    "IN TRANSIT": "IN_TRANSIT",
    "SHIPPED": "IN_TRANSIT",
    "OUT FOR DELIVERY": "OUT_FOR_DELIVERY",
    "DELIVERED": "DELIVERED",
    "CANCELLED": "CANCELLED",
    "RTO INITIATED": "RTO",
    "RTO DELIVERED": "RTO",
}


@router.post("/login")
async def login():
    return await shiprocketController.login()


@router.post("/order")
async def createOrder(
    order: CreateOrderRequest
):
    return await shiprocketController.createOrder(order)


@router.get("/serviceability")
async def checkServiceability(
    request: ServiceabilityRequest
):
    return await shiprocketController.checkServiceability(
        request
    )


@router.get("/couriers")
async def getAvailableCouriers(
    request: CourierRecommendationRequest
):
    return await shiprocketController.getAvailableCouriers(
        request
    )


@router.post("/awb")
async def generateAwb(
    request: GenerateAwbRequest
):
    return await shiprocketController.generateAwb(
        request
    )


@router.post("/pickup")
async def requestPickup(
    request: PickupRequest
):
    return await shiprocketController.requestPickup(
        request
    )


@router.post("/label")
async def generateLabel(
    request: LabelRequest
):
    return await shiprocketController.generateLabel(
        request
    )


@router.post("/invoice")
async def generateInvoice(
    request: InvoiceRequest
):
    return await shiprocketController.generateInvoice(
        request
    )


@router.post("/manifest")
async def generateManifest(
    request: ManifestRequest
):
    return await shiprocketController.generateManifest(
        request
    )


@router.get("/track/{awbCode}")
async def trackShipment(
    awbCode: str
):
    return await shiprocketController.trackShipment(
        awbCode
    )


@router.post("/cancel")
async def cancelOrder(
    orderIds: list[int] = Body(...)
):
    return await shiprocketController.cancelOrder(
        orderIds
    )
    
@router.get("/orders")
async def getOrders():

    return await shiprocketController.getOrders()


@router.get("/orders/{orderId}")
async def getOrderById(
    orderId: int
):

    return await shiprocketController.getOrderById(
        orderId
    )


@router.put("/orders")
async def updateOrder(
    request: UpdateOrderRequest
):

    return await shiprocketController.updateOrder(
        request
    )
@router.get("/pickup-locations")
async def getPickupLocations():

    return await shiprocketController.getPickupLocations()


@router.post("/pickup-location")
async def addPickupLocation(
    request: PickupLocationRequest
):

    return await shiprocketController.addPickupLocation(
        request
    )
@router.get("/channels")
async def getChannels():

    return await shiprocketController.getChannels()


@router.get("/courier-companies")
async def getCourierCompanies():

    return await shiprocketController.getCourierCompanies()
@router.get("/ndr")
async def getNdrShipments():

    return await shiprocketController.getNdrShipments()


@router.post("/ndr")
async def updateNdr(
    request: NdrActionRequest
):

    return await shiprocketController.updateNdr(
        request
    )


# ── LIVE TRACKING WEBHOOK ──────────────────────
# The only endpoint on this router that touches the local DB — every other
# one above is a pure proxy to Shiprocket's API. Configure this URL in the
# Shiprocket dashboard's webhook settings alongside SHIPROCKET_WEBHOOK_TOKEN.
@router.post("/webhook", status_code=status.HTTP_200_OK)
async def shiprocketWebhook(
    payload: ShiprocketWebhookPayload,
    db: AsyncSession = Depends(getDb),
    xShiprocketWebhookToken: str | None = Header(default=None, alias="X-Shiprocket-Webhook-Token"),
):
    if not SHIPROCKET_WEBHOOK_TOKEN:
        # Fails closed, not open — see the note on razorpayClient.py's
        # PaymentGatewayNotConfigured for why an unconfigured secret must
        # never be treated as "accept anything".
        raise UnauthorizedError("Shiprocket webhook is not configured on this server")
    if not xShiprocketWebhookToken or not hmac.compare_digest(xShiprocketWebhookToken, SHIPROCKET_WEBHOOK_TOKEN):
        raise UnauthorizedError("Invalid Shiprocket webhook token")

    if not payload.awb:
        return {"status": "ignored", "reason": "no awb in payload"}

    result = await db.execute(select(Shipment).where(Shipment.tracking_number == payload.awb))
    shipment = result.scalars().first()
    if not shipment:
        # Shiprocket retries on non-2xx, and an AWB we don't know about isn't
        # this server's fault to keep retrying — acknowledge and move on.
        return {"status": "ignored", "reason": "unknown awb"}

    rawStatus = (payload.current_status or payload.shipment_status or "").strip().upper()
    canonicalStatus = SHIPROCKET_STATUS_MAP.get(rawStatus, rawStatus or shipment.shipment_status)
    oldStatus = shipment.shipment_status

    if canonicalStatus == oldStatus:
        return {"status": "no_change"}

    shipment.shipment_status = canonicalStatus
    now = datetime.now(timezone.utc)
    if canonicalStatus in ("IN_TRANSIT", "PACKED") and not shipment.shipped_at:
        shipment.shipped_at = now
    if canonicalStatus == "DELIVERED":
        shipment.delivered_at = now

    # StatusHistory.tenantId/changedBy are both NOT NULL, and Shipment itself
    # carries no tenant_id — only its parent Order does.
    order = await db.get(Order, shipment.order_id)
    settings = getSettings()
    db.add(
        StatusHistory(
            tenantId=order.tenant_id if order else settings.defaultTenantId,
            entityType="SHIPMENT",
            entityId=shipment.id,
            oldStatus=oldStatus,
            newStatus=canonicalStatus,
            changeReason=f"Shiprocket webhook: {rawStatus or 'status update'}",
            changedBy=settings.defaultUserId,  # no human actor for a gateway webhook
        )
    )
    await db.commit()
    return {"status": "processed", "shipmentId": str(shipment.id), "newStatus": canonicalStatus}