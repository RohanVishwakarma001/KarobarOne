from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.github.schemas import (
    OfferCustomerSegmentCreate,
    OfferCustomerSegmentUpdate,
)
from app.services.github.offerCustomerSegmentService import (
    offerCustomerSegmentService,
)


class OfferCustomerSegmentController:

    def create(
        self,
        db: Session,
        segment: OfferCustomerSegmentCreate,
    ):
        return offerCustomerSegmentService.create(
            db,
            segment,
        )

    def getAll(
        self,
        db: Session,
    ):
        return offerCustomerSegmentService.getAll(db)

    def getById(
        self,
        db: Session,
        segmentId: UUID,
    ):
        item = offerCustomerSegmentService.getById(
            db,
            segmentId,
        )

        if item is None:
            raise HTTPException(
                status_code=404,
                detail="Offer Customer Segment not found",
            )

        return item

    def update(
        self,
        db: Session,
        segmentId: UUID,
        segment: OfferCustomerSegmentUpdate,
    ):
        item = offerCustomerSegmentService.update(
            db,
            segmentId,
            segment,
        )

        if item is None:
            raise HTTPException(
                status_code=404,
                detail="Offer Customer Segment not found",
            )

        return item

    def delete(
        self,
        db: Session,
        segmentId: UUID,
    ):
        deleted = offerCustomerSegmentService.delete(
            db,
            segmentId,
        )

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Offer Customer Segment not found",
            )

        return {
            "message": "Offer Customer Segment deleted successfully"
        }


offerCustomerSegmentController = OfferCustomerSegmentController()