from uuid import UUID

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from app.controllers.github.offerCustomerSegmentController import (
    offerCustomerSegmentController,
)
from app.db.session import getSyncDb
from app.schemas.github.schemas import (
    OfferCustomerSegmentCreate,
    OfferCustomerSegmentUpdate,
    OfferCustomerSegmentResponse,
)

router = APIRouter(
    prefix="/offer-customer-segments",
    tags=["Offer Customer Segments"],
)


@router.post(
    "/",
    response_model=OfferCustomerSegmentResponse,
    status_code=201,
)
def createOfferCustomerSegment(
    segment: OfferCustomerSegmentCreate,
    db: Session = Depends(getSyncDb),
):
    return offerCustomerSegmentController.create(
        db,
        segment,
    )


@router.get(
    "/",
    response_model=list[OfferCustomerSegmentResponse],
)
def getOfferCustomerSegments(
    db: Session = Depends(getSyncDb),
):
    return offerCustomerSegmentController.getAll(db)


@router.get(
    "/{segmentId}",
    response_model=OfferCustomerSegmentResponse,
)
def getOfferCustomerSegment(
    segmentId: UUID,
    db: Session = Depends(getSyncDb),
):
    return offerCustomerSegmentController.getById(
        db,
        segmentId,
    )


@router.put(
    "/{segmentId}",
    response_model=OfferCustomerSegmentResponse,
)
def updateOfferCustomerSegment(
    segmentId: UUID,
    segment: OfferCustomerSegmentUpdate,
    db: Session = Depends(getSyncDb),
):
    return offerCustomerSegmentController.update(
        db,
        segmentId,
        segment,
    )


@router.delete(
    "/{segmentId}",
)
def deleteOfferCustomerSegment(
    segmentId: UUID,
    db: Session = Depends(getSyncDb),
):
    return offerCustomerSegmentController.delete(
        db,
        segmentId,
    )