from typing import List
from uuid import UUID

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from app.controllers.github.shipmentRequestController import (
    shipmentRequestController,
)
from app.db.session import getSyncDb
from app.schemas.github.shipmentRequestSchema import (
    ShipmentRequestCreate,
    ShipmentRequestUpdate,
    ShipmentRequestResponse,
)

router = APIRouter(
    prefix="/shipment-requests",
    tags=["Shipment Requests"]
)


@router.post(
    "/",
    response_model=ShipmentRequestResponse,
    status_code=201
)
def createShipmentRequest(
    request: ShipmentRequestCreate,
    db: Session = Depends(getSyncDb)
):
    return shipmentRequestController.create(
        db,
        request
    )


@router.get(
    "/",
    response_model=List[ShipmentRequestResponse]
)
def getShipmentRequests(
    db: Session = Depends(getSyncDb)
):
    return shipmentRequestController.getAll(db)


@router.get(
    "/{requestId}",
    response_model=ShipmentRequestResponse
)
def getShipmentRequest(
    requestId: UUID,
    db: Session = Depends(getSyncDb)
):
    return shipmentRequestController.getById(
        db,
        requestId
    )


@router.put(
    "/{requestId}",
    response_model=ShipmentRequestResponse
)
def updateShipmentRequest(
    requestId: UUID,
    request: ShipmentRequestUpdate,
    db: Session = Depends(getSyncDb)
):
    return shipmentRequestController.update(
        db,
        requestId,
        request
    )


@router.delete(
    "/{requestId}"
)
def deleteShipmentRequest(
    requestId: UUID,
    db: Session = Depends(getSyncDb)
):
    return shipmentRequestController.delete(
        db,
        requestId
    )