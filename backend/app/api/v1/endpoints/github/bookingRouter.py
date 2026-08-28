from uuid import UUID

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from app.controllers.github.bookingController import (
    bookingController,
)
from app.db.session import getSyncDb
from app.schemas.github.schemas import (
    BookingCreate,
    BookingUpdate,
    BookingResponse,
)

router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"],
)


@router.post(
    "/",
    response_model=BookingResponse,
    status_code=201,
)
def createBooking(
    booking: BookingCreate,
    db: Session = Depends(getSyncDb),
):
    return bookingController.create(
        db,
        booking,
    )


@router.get(
    "/",
    response_model=list[BookingResponse],
)
def getBookings(
    db: Session = Depends(getSyncDb),
):
    return bookingController.getAll(
        db,
    )


@router.get(
    "/{bookingId}",
    response_model=BookingResponse,
)
def getBooking(
    bookingId: UUID,
    db: Session = Depends(getSyncDb),
):
    return bookingController.getById(
        db,
        bookingId,
    )


@router.put(
    "/{bookingId}",
    response_model=BookingResponse,
)
def updateBooking(
    bookingId: UUID,
    booking: BookingUpdate,
    db: Session = Depends(getSyncDb),
):
    return bookingController.update(
        db,
        bookingId,
        booking,
    )


@router.delete(
    "/{bookingId}",
)
def deleteBooking(
    bookingId: UUID,
    db: Session = Depends(getSyncDb),
):
    return bookingController.delete(
        db,
        bookingId,
    )