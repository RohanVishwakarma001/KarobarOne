from typing import List
from uuid import UUID

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from app.db.session import getSyncDb
from app.controllers.github.shippingZoneController import (
    shippingZoneController
)
from app.schemas.github.shippingZoneSchema import (
    ShippingZoneCreate,
    ShippingZoneUpdate,
    ShippingZoneResponse,
)

router = APIRouter(
    prefix="/shipping-zones",
    tags=["Shipping Zones"]
)


@router.post(
    "/",
    response_model=ShippingZoneResponse,
    status_code=201
)
def createShippingZone(
    zone: ShippingZoneCreate,
    db: Session = Depends(getSyncDb)
):
    return shippingZoneController.create(
        db,
        zone
    )


@router.get(
    "/",
    response_model=List[ShippingZoneResponse]
)
def getShippingZones(
    db: Session = Depends(getSyncDb)
):
    return shippingZoneController.getAll(db)


@router.get(
    "/{zoneId}",
    response_model=ShippingZoneResponse
)
def getShippingZone(
    zoneId: UUID,
    db: Session = Depends(getSyncDb)
):
    return shippingZoneController.getById(
        db,
        zoneId
    )


@router.put(
    "/{zoneId}",
    response_model=ShippingZoneResponse
)
def updateShippingZone(
    zoneId: UUID,
    zone: ShippingZoneUpdate,
    db: Session = Depends(getSyncDb)
):
    return shippingZoneController.update(
        db,
        zoneId,
        zone
    )


@router.delete(
    "/{zoneId}"
)
def deleteShippingZone(
    zoneId: UUID,
    db: Session = Depends(getSyncDb)
):
    return shippingZoneController.delete(
        db,
        zoneId
    )