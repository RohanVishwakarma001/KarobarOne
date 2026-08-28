from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.github.schemas import (
    OfferExclusionCreate,
    OfferExclusionUpdate,
)
from app.services.github.offerExclusionService import (
    offerExclusionService,
)


class OfferExclusionController:

    def create(
        self,
        db: Session,
        exclusion: OfferExclusionCreate,
    ):
        return offerExclusionService.create(
            db,
            exclusion,
        )

    def getAll(
        self,
        db: Session,
    ):
        return offerExclusionService.getAll(db)

    def getById(
        self,
        db: Session,
        exclusionId: UUID,
    ):
        item = offerExclusionService.getById(
            db,
            exclusionId,
        )

        if item is None:
            raise HTTPException(
                status_code=404,
                detail="Offer Exclusion not found",
            )

        return item

    def update(
        self,
        db: Session,
        exclusionId: UUID,
        exclusion: OfferExclusionUpdate,
    ):
        item = offerExclusionService.update(
            db,
            exclusionId,
            exclusion,
        )

        if item is None:
            raise HTTPException(
                status_code=404,
                detail="Offer Exclusion not found",
            )

        return item

    def delete(
        self,
        db: Session,
        exclusionId: UUID,
    ):
        deleted = offerExclusionService.delete(
            db,
            exclusionId,
        )

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Offer Exclusion not found",
            )

        return {
            "message": "Offer Exclusion deleted successfully"
        }


offerExclusionController = OfferExclusionController()