from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.github.schemas import (
    BookingCancellationCreate,
    BookingCancellationUpdate,
)
from app.services.github.bookingCancellationService import (
    bookingCancellationService,
)


class BookingCancellationController:

    def create(self, db: Session, cancellation: BookingCancellationCreate):
        return bookingCancellationService.create(
            db,
            cancellation,
        )

    def getAll(self, db: Session):
        return bookingCancellationService.getAll(db)

    def getById(self, db: Session, cancellationId: UUID):
        item = bookingCancellationService.getById(
            db,
            cancellationId,
        )

        if item is None:
            raise HTTPException(
                status_code=404,
                detail="Booking Cancellation not found",
            )

        return item

    def update(
        self,
        db: Session,
        cancellationId: UUID,
        cancellation: BookingCancellationUpdate,
    ):
        item = bookingCancellationService.update(
            db,
            cancellationId,
            cancellation,
        )

        if item is None:
            raise HTTPException(
                status_code=404,
                detail="Booking Cancellation not found",
            )

        return item

    def delete(
        self,
        db: Session,
        cancellationId: UUID,
    ):
        deleted = bookingCancellationService.delete(
            db,
            cancellationId,
        )

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Booking Cancellation not found",
            )

        return {
            "message": "Booking Cancellation deleted successfully"
        }


bookingCancellationController = BookingCancellationController()