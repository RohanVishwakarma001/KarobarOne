from uuid import UUID

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from app.controllers.github.bookingCancellationController import (
    bookingCancellationController,
)
from app.db.session import getSyncDb
from app.schemas.github.schemas import (
    BookingCancellationCreate,
    BookingCancellationUpdate,
    BookingCancellationResponse,
)

router = APIRouter(
    prefix="/booking-cancellations",
    tags=["Booking Cancellations"],
)


@router.post(
    "/",
    response_model=BookingCancellationResponse,
    status_code=201,
)
def createBookingCancellation(
    cancellation: BookingCancellationCreate,
    db: Session = Depends(getSyncDb),
):
    return bookingCancellationController.create(
        db,
        cancellation,
    )


@router.get(
    "/",
    response_model=list[BookingCancellationResponse],
)
def getBookingCancellations(
    db: Session = Depends(getSyncDb),
):
    return bookingCancellationController.getAll(db)


@router.get(
    "/{cancellationId}",
    response_model=BookingCancellationResponse,
)
def getBookingCancellation(
    cancellationId: UUID,
    db: Session = Depends(getSyncDb),
):
    return bookingCancellationController.getById(
        db,
        cancellationId,
    )


@router.put(
    "/{cancellationId}",
    response_model=BookingCancellationResponse,
)
def updateBookingCancellation(
    cancellationId: UUID,
    cancellation: BookingCancellationUpdate,
    db: Session = Depends(getSyncDb),
):
    return bookingCancellationController.update(
        db,
        cancellationId,
        cancellation,
    )


@router.delete(
    "/{cancellationId}",
)
def deleteBookingCancellation(
    cancellationId: UUID,
    db: Session = Depends(getSyncDb),
):
    return bookingCancellationController.delete(
        db,
        cancellationId,
    )