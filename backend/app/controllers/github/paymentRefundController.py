from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.github.paymentRefundSchema import (
    PaymentRefundCreate,
    PaymentRefundUpdate,
)
from app.services.github.paymentRefundService import (
    paymentRefundService,
)


class PaymentRefundController:

    def create(
        self,
        db: Session,
        refund: PaymentRefundCreate
    ):
        return paymentRefundService.create(
            db,
            refund
        )

    def getAll(
        self,
        db: Session
    ):
        return paymentRefundService.getAll(db)

    def getById(
        self,
        db: Session,
        refundId: UUID
    ):
        refund = paymentRefundService.getById(
            db,
            refundId
        )

        if refund is None:
            raise HTTPException(
                status_code=404,
                detail="Refund not found."
            )

        return refund

    def update(
        self,
        db: Session,
        refundId: UUID,
        refund: PaymentRefundUpdate
    ):
        dbRefund = paymentRefundService.update(
            db,
            refundId,
            refund
        )

        if dbRefund is None:
            raise HTTPException(
                status_code=404,
                detail="Refund not found."
            )

        return dbRefund

    def delete(
        self,
        db: Session,
        refundId: UUID
    ):
        deleted = paymentRefundService.delete(
            db,
            refundId
        )

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Refund not found."
            )

        return {
            "message": "Refund deleted successfully."
        }


paymentRefundController = PaymentRefundController()