from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.github.schemas import (
    OfferTargetCreate,
)
from app.services.github.offerTargetService import (
    offerTargetService,
)


class OfferTargetController:

    def create(
        self,
        db: Session,
        target: OfferTargetCreate,
    ):
        return offerTargetService.create(
            db,
            target,
        )

    def getAll(
        self,
        db: Session,
    ):
        return offerTargetService.getAll(db)

    def getById(
        self,
        db: Session,
        targetId: UUID,
    ):
        target = offerTargetService.getById(
            db,
            targetId,
        )

        if target is None:
            raise HTTPException(
                status_code=404,
                detail="Offer Target not found",
            )

        return target

    def delete(
        self,
        db: Session,
        targetId: UUID,
    ):
        deleted = offerTargetService.delete(
            db,
            targetId,
        )

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Offer Target not found",
            )

        return {
            "message": "Offer Target deleted successfully"
        }


offerTargetController = OfferTargetController()