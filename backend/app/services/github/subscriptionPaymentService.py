from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.github.subscriptionPaymentRepository import (
    subscriptionPaymentRepository,
)
from app.schemas.github.subscriptionPaymentSchema import (
    SubscriptionPaymentCreate,
    SubscriptionPaymentUpdate,
)


class SubscriptionPaymentService:

    def create(
        self,
        db: Session,
        payment: SubscriptionPaymentCreate
    ):
        return subscriptionPaymentRepository.create(
            db=db,
            obj=payment
        )

    def getAll(
        self,
        db: Session
    ):
        return subscriptionPaymentRepository.get_all(db)

    def getById(
        self,
        db: Session,
        paymentId: UUID
    ):
        return subscriptionPaymentRepository.get(
            db=db,
            obj_id=paymentId,
            id_field=subscriptionPaymentRepository.model.id
        )

    def update(
        self,
        db: Session,
        paymentId: UUID,
        payment: SubscriptionPaymentUpdate
    ):
        dbPayment = self.getById(
            db,
            paymentId
        )

        if dbPayment is None:
            return None

        return subscriptionPaymentRepository.update(
            db=db,
            db_obj=dbPayment,
            obj=payment
        )

    def delete(
        self,
        db: Session,
        paymentId: UUID
    ):
        dbPayment = self.getById(
            db,
            paymentId
        )

        if dbPayment is None:
            return False

        subscriptionPaymentRepository.delete(
            db=db,
            db_obj=dbPayment
        )

        return True


subscriptionPaymentService = SubscriptionPaymentService()