from uuid import UUID

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from app.controllers.github.paymentRefundController import (
    paymentRefundController,
)
from app.db.session import getSyncDb
from app.schemas.github.paymentRefundSchema import (
    PaymentRefundCreate,
    PaymentRefundUpdate,
)

router = APIRouter(
    prefix="/payment-refunds",
    tags=["Payment Refunds"]
)


@router.post("/")
def create(
    refund: PaymentRefundCreate,
    db: Session = Depends(getSyncDb)
):
    return paymentRefundController.create(
        db,
        refund
    )


@router.get("/")
def getAll(
    db: Session = Depends(getSyncDb)
):
    return paymentRefundController.getAll(db)


@router.get("/{refundId}")
def getById(
    refundId: UUID,
    db: Session = Depends(getSyncDb)
):
    return paymentRefundController.getById(
        db,
        refundId
    )


@router.put("/{refundId}")
def update(
    refundId: UUID,
    refund: PaymentRefundUpdate,
    db: Session = Depends(getSyncDb)
):
    return paymentRefundController.update(
        db,
        refundId,
        refund
    )


@router.delete("/{refundId}")
def delete(
    refundId: UUID,
    db: Session = Depends(getSyncDb)
):
    return paymentRefundController.delete(
        db,
        refundId
    )