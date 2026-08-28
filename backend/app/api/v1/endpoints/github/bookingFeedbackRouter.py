from uuid import UUID

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from app.controllers.github.bookingFeedbackController import (
    bookingFeedbackController,
)
from app.db.session import getSyncDb
from app.schemas.github.schemas import (
    BookingFeedbackCreate,
    BookingFeedbackUpdate,
    BookingFeedbackResponse,
)

router = APIRouter(
    prefix="/booking-feedbacks",
    tags=["Booking Feedbacks"],
)


@router.post(
    "/",
    response_model=BookingFeedbackResponse,
    status_code=201,
)
def createBookingFeedback(
    feedback: BookingFeedbackCreate,
    db: Session = Depends(getSyncDb),
):
    return bookingFeedbackController.create(
        db,
        feedback,
    )


@router.get(
    "/",
    response_model=list[BookingFeedbackResponse],
)
def getBookingFeedbacks(
    db: Session = Depends(getSyncDb),
):
    return bookingFeedbackController.getAll(db)


@router.get(
    "/{feedbackId}",
    response_model=BookingFeedbackResponse,
)
def getBookingFeedback(
    feedbackId: UUID,
    db: Session = Depends(getSyncDb),
):
    return bookingFeedbackController.getById(
        db,
        feedbackId,
    )


@router.put(
    "/{feedbackId}",
    response_model=BookingFeedbackResponse,
)
def updateBookingFeedback(
    feedbackId: UUID,
    feedback: BookingFeedbackUpdate,
    db: Session = Depends(getSyncDb),
):
    return bookingFeedbackController.update(
        db,
        feedbackId,
        feedback,
    )


@router.delete(
    "/{feedbackId}",
)
def deleteBookingFeedback(
    feedbackId: UUID,
    db: Session = Depends(getSyncDb),
):
    return bookingFeedbackController.delete(
        db,
        feedbackId,
    )