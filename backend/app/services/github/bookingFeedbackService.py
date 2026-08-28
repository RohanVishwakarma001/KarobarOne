from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.github.bookingFeedbackRepository import (
    bookingFeedbackRepository,
)
from app.schemas.github.schemas import (
    BookingFeedbackCreate,
    BookingFeedbackUpdate,
)


class BookingFeedbackService:

    def create(
        self,
        db: Session,
        feedback: BookingFeedbackCreate,
    ):
        return bookingFeedbackRepository.create(
            db,
            feedback,
        )

    def getAll(
        self,
        db: Session,
    ):
        return bookingFeedbackRepository.get_all(db)

    def getById(
        self,
        db: Session,
        feedbackId: UUID,
    ):
        return bookingFeedbackRepository.get(
            db,
            feedbackId,
            bookingFeedbackRepository.model.id,
        )

    def update(
        self,
        db: Session,
        feedbackId: UUID,
        feedback: BookingFeedbackUpdate,
    ):
        dbFeedback = self.getById(
            db,
            feedbackId,
        )

        if dbFeedback is None:
            return None

        return bookingFeedbackRepository.update(
            db,
            dbFeedback,
            feedback,
        )

    def delete(
        self,
        db: Session,
        feedbackId: UUID,
    ):
        dbFeedback = self.getById(
            db,
            feedbackId,
        )

        if dbFeedback is None:
            return False

        bookingFeedbackRepository.delete(
            db,
            dbFeedback,
        )

        return True


bookingFeedbackService = BookingFeedbackService()