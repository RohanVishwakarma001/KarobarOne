from uuid import UUID

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from app.db.session import getSyncDb
from app.controllers.github.shippingPartnerController import (
    shippingPartnerController
)
from app.schemas.github.shippingPartnerSchema import (
    ShippingPartnerCreate,
    ShippingPartnerUpdate,
    ShippingPartnerResponse,
)

router = APIRouter(
    prefix="/shipping-partners",
    tags=["Shipping Partners"]
)


@router.post(
    "/",
    response_model=ShippingPartnerResponse,
    status_code=201
)
def createShippingPartner(
    partner: ShippingPartnerCreate,
    db: Session = Depends(getSyncDb)
):
    return shippingPartnerController.create(
        db,
        partner
    )


@router.get(
    "/",
    response_model=list[ShippingPartnerResponse]
)
def getShippingPartners(
    db: Session = Depends(getSyncDb)
):
    return shippingPartnerController.getAll(db)


@router.get(
    "/{partnerId}",
    response_model=ShippingPartnerResponse
)
def getShippingPartner(
    partnerId: UUID,
    db: Session = Depends(getSyncDb)
):
    return shippingPartnerController.getById(
        db,
        partnerId
    )


@router.put(
    "/{partnerId}",
    response_model=ShippingPartnerResponse
)
def updateShippingPartner(
    partnerId: UUID,
    partner: ShippingPartnerUpdate,
    db: Session = Depends(getSyncDb)
):
    return shippingPartnerController.update(
        db,
        partnerId,
        partner
    )


@router.delete(
    "/{partnerId}"
)
def deleteShippingPartner(
    partnerId: UUID,
    db: Session = Depends(getSyncDb)
):
    return shippingPartnerController.delete(
        db,
        partnerId
    )