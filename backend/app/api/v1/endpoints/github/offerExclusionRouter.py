from uuid import UUID

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from app.controllers.github.offerExclusionController import (
    offerExclusionController,
)
from app.db.session import getSyncDb
from app.schemas.github.schemas import (
    OfferExclusionCreate,
    OfferExclusionUpdate,
    OfferExclusionResponse,
)

router = APIRouter(
    prefix="/offer-exclusions",
    tags=["Offer Exclusions"],
)


@router.post(
    "/",
    response_model=OfferExclusionResponse,
    status_code=201,
)
def createOfferExclusion(
    exclusion: OfferExclusionCreate,
    db: Session = Depends(getSyncDb),
):
    return offerExclusionController.create(
        db,
        exclusion,
    )


@router.get(
    "/",
    response_model=list[OfferExclusionResponse],
)
def getOfferExclusions(
    db: Session = Depends(getSyncDb),
):
    return offerExclusionController.getAll(db)


@router.get(
    "/{exclusionId}",
    response_model=OfferExclusionResponse,
)
def getOfferExclusion(
    exclusionId: UUID,
    db: Session = Depends(getSyncDb),
):
    return offerExclusionController.getById(
        db,
        exclusionId,
    )


@router.put(
    "/{exclusionId}",
    response_model=OfferExclusionResponse,
)
def updateOfferExclusion(
    exclusionId: UUID,
    exclusion: OfferExclusionUpdate,
    db: Session = Depends(getSyncDb),
):
    return offerExclusionController.update(
        db,
        exclusionId,
        exclusion,
    )


@router.delete(
    "/{exclusionId}",
)
def deleteOfferExclusion(
    exclusionId: UUID,
    db: Session = Depends(getSyncDb),
):
    return offerExclusionController.delete(
        db,
        exclusionId,
    )