from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.github.schemas import (
    BookingFeedbackCreate,
    BookingFeedbackUpdate,
)
from app.services.github.bookingFeedbackService import (
    bookingFeedbackService,
)


class BookingFeedbackController:

    def create(
        self,
        db: Session,
        feedback: BookingFeedbackCreate,
    ):
        return bookingFeedbackService.create(
            db,
            feedback,
        )

    def getAll(
        self,
        db: Session,
    ):
        return bookingFeedbackService.getAll(db)

    def getById(
        self,
        db: Session,
        feedbackId: UUID,
    ):
        feedback = bookingFeedbackService.getById(
            db,
            feedbackId,
        )

        if feedback is None:
            raise HTTPException(
                status_code=404,
                detail="Booking Feedback not found",
            )

        return feedback

    def update(
        self,
        db: Session,
        feedbackId: UUID,
        feedback: BookingFeedbackUpdate,
    ):
        updated = bookingFeedbackService.update(
            db,
            feedbackId,
            feedback,
        )

        if updated is None:
            raise HTTPException(
                status_code=404,
                detail="Booking Feedback not found",
            )

        return updated

    def delete(
        self,
        db: Session,
        feedbackId: UUID,
    ):
        deleted = bookingFeedbackService.delete(
            db,
            feedbackId,
        )

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Booking Feedback not found",
            )

        return {
            "message": "Booking Feedback deleted successfully"
        }


bookingFeedbackController = BookingFeedbackController()