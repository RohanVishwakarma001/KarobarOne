from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.github.schemas import (
    BookingRefundCreate,
    BookingRefundUpdate,
)
from app.services.github.bookingRefundService import (
    bookingRefundService,
)


class BookingRefundController:

    def create(self, db: Session, refund: BookingRefundCreate):
        return bookingRefundService.create(db, refund)

    def getAll(self, db: Session):
        return bookingRefundService.getAll(db)

    def getById(self, db: Session, refundId: UUID):
        refund = bookingRefundService.getById(db, refundId)

        if refund is None:
            raise HTTPException(
                status_code=404,
                detail="Booking Refund not found",
            )

        return refund

    def update(
        self,
        db: Session,
        refundId: UUID,
        refund: BookingRefundUpdate,
    ):
        updated = bookingRefundService.update(
            db,
            refundId,
            refund,
        )

        if updated is None:
            raise HTTPException(
                status_code=404,
                detail="Booking Refund not found",
            )

        return updated

    def delete(self, db: Session, refundId: UUID):
        deleted = bookingRefundService.delete(
            db,
            refundId,
        )

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Booking Refund not found",
            )

        return {
            "message": "Booking Refund deleted successfully"
        }


bookingRefundController = BookingRefundController()