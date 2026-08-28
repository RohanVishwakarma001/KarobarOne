from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.github.schemas import (
    OfferCreate,
    OfferUpdate,
)
from app.services.github.offerService import (
    offerService,
)


class OfferController:

    def create(
        self,
        db: Session,
        offer: OfferCreate,
    ):
        return offerService.create(
            db,
            offer,
        )

    def getAll(
        self,
        db: Session,
    ):
        return offerService.getAll(db)

    def getById(
        self,
        db: Session,
        offerId: UUID,
    ):
        offer = offerService.getById(
            db,
            offerId,
        )

        if offer is None:
            raise HTTPException(
                status_code=404,
                detail="Offer not found",
            )

        return offer

    def update(
        self,
        db: Session,
        offerId: UUID,
        offer: OfferUpdate,
    ):
        updated = offerService.update(
            db,
            offerId,
            offer,
        )

        if updated is None:
            raise HTTPException(
                status_code=404,
                detail="Offer not found",
            )

        return updated

    def delete(
        self,
        db: Session,
        offerId: UUID,
    ):
        deleted = offerService.delete(
            db,
            offerId,
        )

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Offer not found",
            )

        return {
            "message": "Offer deleted successfully"
        }


offerController = OfferController()