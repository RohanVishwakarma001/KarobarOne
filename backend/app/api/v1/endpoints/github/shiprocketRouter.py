from fastapi import APIRouter, Body

from app.controllers.github.shiprocketController import (
    shiprocketController,
)

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
)

router = APIRouter(
    prefix="/shiprocket",
    tags=["Shiprocket"],
)


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