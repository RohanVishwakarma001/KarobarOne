from typing import List
from uuid import UUID

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from app.db.session import getSyncDb
from app.controllers.github.shippingRateController import (
    shippingRateController,
)
from app.schemas.github.shippingRateSchema import (
    ShippingRateCreate,
    ShippingRateUpdate,
    ShippingRateResponse,
)

router = APIRouter(
    prefix="/shipping-rates",
    tags=["Shipping Rates"]
)


@router.post(
    "/",
    response_model=ShippingRateResponse,
    status_code=201
)
def createShippingRate(
    rate: ShippingRateCreate,
    db: Session = Depends(getSyncDb)
):
    return shippingRateController.create(
        db,
        rate
    )


@router.get(
    "/",
    response_model=List[ShippingRateResponse]
)
def getShippingRates(
    db: Session = Depends(getSyncDb)
):
    return shippingRateController.getAll(db)


@router.get(
    "/{rateId}",
    response_model=ShippingRateResponse
)
def getShippingRate(
    rateId: UUID,
    db: Session = Depends(getSyncDb)
):
    return shippingRateController.getById(
        db,
        rateId
    )


@router.put(
    "/{rateId}",
    response_model=ShippingRateResponse
)
def updateShippingRate(
    rateId: UUID,
    rate: ShippingRateUpdate,
    db: Session = Depends(getSyncDb)
):
    return shippingRateController.update(
        db,
        rateId,
        rate
    )


@router.delete(
    "/{rateId}"
)
def deleteShippingRate(
    rateId: UUID,
    db: Session = Depends(getSyncDb)
):
    return shippingRateController.delete(
        db,
        rateId
    )