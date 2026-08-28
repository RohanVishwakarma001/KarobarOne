from uuid import UUID

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from app.controllers.github.offerController import (
    offerController,
)
from app.db.session import getSyncDb
from app.schemas.github.schemas import (
    OfferCreate,
    OfferUpdate,
    OfferResponse,
)

router = APIRouter(
    prefix="/offers",
    tags=["Offers"],
)


@router.post(
    "/",
    response_model=OfferResponse,
    status_code=201,
)
def createOffer(
    offer: OfferCreate,
    db: Session = Depends(getSyncDb),
):
    return offerController.create(
        db,
        offer,
    )


@router.get(
    "/",
    response_model=list[OfferResponse],
)
def getOffers(
    db: Session = Depends(getSyncDb),
):
    return offerController.getAll(db)


@router.get(
    "/{offerId}",
    response_model=OfferResponse,
)
def getOffer(
    offerId: UUID,
    db: Session = Depends(getSyncDb),
):
    return offerController.getById(
        db,
        offerId,
    )


@router.put(
    "/{offerId}",
    response_model=OfferResponse,
)
def updateOffer(
    offerId: UUID,
    offer: OfferUpdate,
    db: Session = Depends(getSyncDb),
):
    return offerController.update(
        db,
        offerId,
        offer,
    )


@router.delete(
    "/{offerId}",
)
def deleteOffer(
    offerId: UUID,
    db: Session = Depends(getSyncDb),
):
    return offerController.delete(
        db,
        offerId,
    )