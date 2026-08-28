from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.github.bookingRepository import (
    bookingRepository,
)
from app.schemas.github.schemas import (
    BookingCreate,
    BookingUpdate,
)


class BookingService:

    def create(
        self,
        db: Session,
        booking: BookingCreate,
    ):
        import uuid
        from app.db.models.github.models import Booking

        data = booking.model_dump(mode="json")
        if not data.get("booking_number"):
            data["booking_number"] = f"BK-{uuid.uuid4().hex[:8].upper()}"
        if "total_amount" not in data or data["total_amount"] is None:
            data["total_amount"] = round(
                float(data.get("subtotal_amount") or 0.0)
                - float(data.get("discount_amount") or 0.0)
                + float(data.get("tax_amount") or 0.0),
                2,
            )
        db_obj = Booking(**data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def getAll(
        self,
        db: Session,
    ):
        return bookingRepository.get_all(db)

    def getById(
        self,
        db: Session,
        bookingId: UUID,
    ):
        return bookingRepository.get(
            db,
            bookingId,
            bookingRepository.model.id,
        )

    def update(
        self,
        db: Session,
        bookingId: UUID,
        booking: BookingUpdate,
    ):
        dbBooking = self.getById(
            db,
            bookingId,
        )

        if dbBooking is None:
            return None

        return bookingRepository.update(
            db,
            dbBooking,
            booking,
        )

    def delete(
        self,
        db: Session,
        bookingId: UUID,
    ):
        dbBooking = self.getById(
            db,
            bookingId,
        )

        if dbBooking is None:
            return False

        bookingRepository.delete(
            db,
            dbBooking,
        )

        return True


bookingService = BookingService()