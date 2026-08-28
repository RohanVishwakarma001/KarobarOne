from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.github.offerCustomerSegmentRepository import (
    offerCustomerSegmentRepository,
)
from app.schemas.github.schemas import (
    OfferCustomerSegmentCreate,
    OfferCustomerSegmentUpdate,
)


class OfferCustomerSegmentService:

    def create(
        self,
        db: Session,
        segment: OfferCustomerSegmentCreate,
    ):
        return offerCustomerSegmentRepository.create(
            db,
            segment,
        )

    def getAll(
        self,
        db: Session,
    ):
        return offerCustomerSegmentRepository.get_all(db)

    def getById(
        self,
        db: Session,
        segmentId: UUID,
    ):
        return offerCustomerSegmentRepository.get(
            db,
            segmentId,
            offerCustomerSegmentRepository.model.id,
        )

    def update(
        self,
        db: Session,
        segmentId: UUID,
        segment: OfferCustomerSegmentUpdate,
    ):
        dbSegment = self.getById(
            db,
            segmentId,
        )

        if dbSegment is None:
            return None

        return offerCustomerSegmentRepository.update(
            db,
            dbSegment,
            segment,
        )

    def delete(
        self,
        db: Session,
        segmentId: UUID,
    ):
        dbSegment = self.getById(
            db,
            segmentId,
        )

        if dbSegment is None:
            return False

        offerCustomerSegmentRepository.delete(
            db,
            dbSegment,
        )

        return True


offerCustomerSegmentService = OfferCustomerSegmentService()