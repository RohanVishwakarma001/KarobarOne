from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.github.bookingCancellationRepository import (
    bookingCancellationRepository,
)
from app.schemas.github.schemas import (
    BookingCancellationCreate,
    BookingCancellationUpdate,
)


class BookingCancellationService:

    def create(
        self,
        db: Session,
        cancellation: BookingCancellationCreate,
    ):
        return bookingCancellationRepository.create(
            db,
            cancellation,
        )

    def getAll(
        self,
        db: Session,
    ):
        return bookingCancellationRepository.get_all(db)

    def getById(
        self,
        db: Session,
        cancellationId: UUID,
    ):
        return bookingCancellationRepository.get(
            db,
            cancellationId,
            bookingCancellationRepository.model.id,
        )

    def update(
        self,
        db: Session,
        cancellationId: UUID,
        cancellation: BookingCancellationUpdate,
    ):
        dbItem = self.getById(
            db,
            cancellationId,
        )

        if dbItem is None:
            return None

        return bookingCancellationRepository.update(
            db,
            dbItem,
            cancellation,
        )

    def delete(
        self,
        db: Session,
        cancellationId: UUID,
    ):
        dbItem = self.getById(
            db,
            cancellationId,
        )

        if dbItem is None:
            return False

        bookingCancellationRepository.delete(
            db,
            dbItem,
        )

        return True


bookingCancellationService = BookingCancellationService()