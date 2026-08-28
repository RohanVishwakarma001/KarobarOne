from typing import List
from uuid import UUID

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from app.controllers.github.shipmentController import (
    shipmentController,
)
from app.db.session import getSyncDb
from app.schemas.github.shipmentSchema import (
    ShipmentCreate,
    ShipmentUpdate,
    ShipmentResponse,
)

router = APIRouter(
    prefix="/shipments",
    tags=["Shipments"]
)


@router.post(
    "/",
    response_model=ShipmentResponse,
    status_code=201
)
def createShipment(
    shipment: ShipmentCreate,
    db: Session = Depends(getSyncDb)
):
    return shipmentController.create(
        db,
        shipment
    )


@router.get(
    "/",
    response_model=List[ShipmentResponse]
)
def getShipments(
    db: Session = Depends(getSyncDb)
):
    return shipmentController.getAll(db)


@router.get(
    "/{shipmentId}",
    response_model=ShipmentResponse
)
def getShipment(
    shipmentId: UUID,
    db: Session = Depends(getSyncDb)
):
    return shipmentController.getById(
        db,
        shipmentId
    )


@router.put(
    "/{shipmentId}",
    response_model=ShipmentResponse
)
def updateShipment(
    shipmentId: UUID,
    shipment: ShipmentUpdate,
    db: Session = Depends(getSyncDb)
):
    return shipmentController.update(
        db,
        shipmentId,
        shipment
    )


@router.delete(
    "/{shipmentId}"
)
def deleteShipment(
    shipmentId: UUID,
    db: Session = Depends(getSyncDb)
):
    return shipmentController.delete(
        db,
        shipmentId
    )