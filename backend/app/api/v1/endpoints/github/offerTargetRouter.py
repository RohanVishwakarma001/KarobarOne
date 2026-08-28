from uuid import UUID

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from app.controllers.github.offerTargetController import (
    offerTargetController,
)
from app.db.session import getSyncDb
from app.schemas.github.schemas import (
    OfferTargetCreate,
    OfferTargetResponse,
)

router = APIRouter(
    prefix="/offer-targets",
    tags=["Offer Targets"],
)


@router.post(
    "/",
    response_model=OfferTargetResponse,
    status_code=201,
)
def createOfferTarget(
    target: OfferTargetCreate,
    db: Session = Depends(getSyncDb),
):
    return offerTargetController.create(
        db,
        target,
    )


@router.get(
    "/",
    response_model=list[OfferTargetResponse],
)
def getOfferTargets(
    db: Session = Depends(getSyncDb),
):
    return offerTargetController.getAll(db)


@router.get(
    "/{targetId}",
    response_model=OfferTargetResponse,
)
def getOfferTarget(
    targetId: UUID,
    db: Session = Depends(getSyncDb),
):
    return offerTargetController.getById(
        db,
        targetId,
    )


@router.delete(
    "/{targetId}",
)
def deleteOfferTarget(
    targetId: UUID,
    db: Session = Depends(getSyncDb),
):
    return offerTargetController.delete(
        db,
        targetId,
    )