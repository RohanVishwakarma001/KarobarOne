from uuid import UUID

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from app.controllers.github.bookingRefundController import (
    bookingRefundController,
)
from app.db.session import getSyncDb
from app.schemas.github.schemas import (
    BookingRefundCreate,
    BookingRefundUpdate,
    BookingRefundResponse,
)

router = APIRouter(
    prefix="/booking-refunds",
    tags=["Booking Refunds"],
)


@router.post(
    "/",
    response_model=BookingRefundResponse,
    status_code=201,
)
def createBookingRefund(
    refund: BookingRefundCreate,
    db: Session = Depends(getSyncDb),
):
    return bookingRefundController.create(
        db,
        refund,
    )


@router.get(
    "/",
    response_model=list[BookingRefundResponse],
)
def getBookingRefunds(
    db: Session = Depends(getSyncDb),
):
    return bookingRefundController.getAll(db)


@router.get(
    "/{refundId}",
    response_model=BookingRefundResponse,
)
def getBookingRefund(
    refundId: UUID,
    db: Session = Depends(getSyncDb),
):
    return bookingRefundController.getById(
        db,
        refundId,
    )


@router.put(
    "/{refundId}",
    response_model=BookingRefundResponse,
)
def updateBookingRefund(
    refundId: UUID,
    refund: BookingRefundUpdate,
    db: Session = Depends(getSyncDb),
):
    return bookingRefundController.update(
        db,
        refundId,
        refund,
    )


@router.delete(
    "/{refundId}",
)
def deleteBookingRefund(
    refundId: UUID,
    db: Session = Depends(getSyncDb),
):
    return bookingRefundController.delete(
        db,
        refundId,
    )