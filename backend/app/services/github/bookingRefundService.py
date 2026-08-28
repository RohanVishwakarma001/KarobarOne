from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.github.bookingRefundRepository import (
    bookingRefundRepository,
)
from app.schemas.github.schemas import (
    BookingRefundCreate,
    BookingRefundUpdate,
)


class BookingRefundService:

    def create(self, db: Session, refund: BookingRefundCreate):
        return bookingRefundRepository.create(db, refund)

    def getAll(self, db: Session):
        return bookingRefundRepository.get_all(db)

    def getById(self, db: Session, refundId: UUID):
        return bookingRefundRepository.get(
            db,
            refundId,
            bookingRefundRepository.model.id,
        )

    def update(
        self,
        db: Session,
        refundId: UUID,
        refund: BookingRefundUpdate,
    ):
        dbRefund = self.getById(db, refundId)

        if dbRefund is None:
            return None

        return bookingRefundRepository.update(
            db,
            dbRefund,
            refund,
        )

    def delete(self, db: Session, refundId: UUID):
        dbRefund = self.getById(db, refundId)

        if dbRefund is None:
            return False

        bookingRefundRepository.delete(db, dbRefund)

        return True


bookingRefundService = BookingRefundService()