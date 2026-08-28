from typing import List
from uuid import UUID

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from app.controllers.github.shippingProfileZoneController import (
    shippingProfileZoneController,
)
from app.db.session import getSyncDb
from app.schemas.github.shippingProfileZoneSchema import (
    ShippingProfileZoneCreate,
    ShippingProfileZoneResponse,
)

router = APIRouter(
    prefix="/shipping-profile-zones",
    tags=["Shipping Profile Zones"]
)


@router.post(
    "/",
    response_model=ShippingProfileZoneResponse,
    status_code=201
)
def create(
    obj: ShippingProfileZoneCreate,
    db: Session = Depends(getSyncDb)
):
    return shippingProfileZoneController.create(
        db,
        obj
    )


@router.get(
    "/",
    response_model=List[ShippingProfileZoneResponse]
)
def getAll(
    db: Session = Depends(getSyncDb)
):
    return shippingProfileZoneController.getAll(db)


@router.get(
    "/{objId}",
    response_model=ShippingProfileZoneResponse
)
def getById(
    objId: UUID,
    db: Session = Depends(getSyncDb)
):
    return shippingProfileZoneController.getById(
        db,
        objId
    )


@router.delete(
    "/{objId}"
)
def delete(
    objId: UUID,
    db: Session = Depends(getSyncDb)
):
    return shippingProfileZoneController.delete(
        db,
        objId
    )