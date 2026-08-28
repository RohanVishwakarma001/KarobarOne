from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.github.schemas import (
    BookingCreate,
    BookingUpdate,
)
from app.services.github.bookingService import (
    bookingService,
)


class BookingController:

    def create(
        self,
        db: Session,
        booking: BookingCreate,
    ):
        return bookingService.create(
            db,
            booking,
        )

    def getAll(
        self,
        db: Session,
    ):
        return bookingService.getAll(db)

    def getById(
        self,
        db: Session,
        bookingId: UUID,
    ):
        booking = bookingService.getById(
            db,
            bookingId,
        )

        if booking is None:
            raise HTTPException(
                status_code=404,
                detail="Booking not found",
            )

        return booking

    def update(
        self,
        db: Session,
        bookingId: UUID,
        booking: BookingUpdate,
    ):
        updatedBooking = bookingService.update(
            db,
            bookingId,
            booking,
        )

        if updatedBooking is None:
            raise HTTPException(
                status_code=404,
                detail="Booking not found",
            )

        return updatedBooking

    def delete(
        self,
        db: Session,
        bookingId: UUID,
    ):
        deleted = bookingService.delete(
            db,
            bookingId,
        )

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Booking not found",
            )

        return {
            "message": "Booking deleted successfully"
        }


bookingController = BookingController()