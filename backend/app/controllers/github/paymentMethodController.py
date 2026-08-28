from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.github.paymentMethodSchema import (
    PaymentMethodCreate,
    PaymentMethodUpdate,
)
from app.services.github.paymentMethodService import (
    paymentMethodService,
)


class PaymentMethodController:

    def create(
        self,
        db: Session,
        paymentMethod: PaymentMethodCreate
    ):
        return paymentMethodService.create(
            db,
            paymentMethod
        )

    def getAll(
        self,
        db: Session
    ):
        return paymentMethodService.getAll(db)

    def getById(
        self,
        db: Session,
        paymentMethodId: UUID
    ):
        paymentMethod = paymentMethodService.getById(
            db,
            paymentMethodId
        )

        if paymentMethod is None:
            raise HTTPException(
                status_code=404,
                detail="Payment Method not found."
            )

        return paymentMethod

    def update(
        self,
        db: Session,
        paymentMethodId: UUID,
        paymentMethod: PaymentMethodUpdate
    ):
        updatedPaymentMethod = paymentMethodService.update(
            db,
            paymentMethodId,
            paymentMethod
        )

        if updatedPaymentMethod is None:
            raise HTTPException(
                status_code=404,
                detail="Payment Method not found."
            )

        return updatedPaymentMethod

    def delete(
        self,
        db: Session,
        paymentMethodId: UUID
    ):
        deleted = paymentMethodService.delete(
            db,
            paymentMethodId
        )

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Payment Method not found."
            )

        return {
            "message": "Payment Method deleted successfully."
        }


paymentMethodController = PaymentMethodController()