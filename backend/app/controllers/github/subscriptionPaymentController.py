from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.github.subscriptionPaymentSchema import (
    SubscriptionPaymentCreate,
    SubscriptionPaymentUpdate,
)
from app.services.github.subscriptionPaymentService import (
    subscriptionPaymentService,
)


class SubscriptionPaymentController:

    def create(
        self,
        db: Session,
        payment: SubscriptionPaymentCreate
    ):
        return subscriptionPaymentService.create(
            db,
            payment
        )

    def getAll(
        self,
        db: Session
    ):
        return subscriptionPaymentService.getAll(db)

    def getById(
        self,
        db: Session,
        paymentId: UUID
    ):
        payment = subscriptionPaymentService.getById(
            db,
            paymentId
        )

        if payment is None:
            raise HTTPException(
                status_code=404,
                detail="Subscription payment not found."
            )

        return payment

    def update(
        self,
        db: Session,
        paymentId: UUID,
        payment: SubscriptionPaymentUpdate
    ):
        dbPayment = subscriptionPaymentService.update(
            db,
            paymentId,
            payment
        )

        if dbPayment is None:
            raise HTTPException(
                status_code=404,
                detail="Subscription payment not found."
            )

        return dbPayment

    def delete(
        self,
        db: Session,
        paymentId: UUID
    ):
        deleted = subscriptionPaymentService.delete(
            db,
            paymentId
        )

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Subscription payment not found."
            )

        return {
            "message": "Subscription payment deleted successfully."
        }


subscriptionPaymentController = SubscriptionPaymentController()