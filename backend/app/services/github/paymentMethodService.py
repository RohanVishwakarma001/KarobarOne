from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.github.paymentMethodRepository import paymentMethodRepository
from app.schemas.github.paymentMethodSchema import (
    PaymentMethodCreate,
    PaymentMethodUpdate,
)


class PaymentMethodService:

    def create(
        self,
        db: Session,
        paymentMethod: PaymentMethodCreate
    ):
        return paymentMethodRepository.create(
            db=db,
            obj=paymentMethod
        )

    def getAll(
        self,
        db: Session
    ):
        return paymentMethodRepository.get_all(db)

    def getById(
        self,
        db: Session,
        paymentMethodId: UUID
    ):
        return paymentMethodRepository.get(
            db=db,
            obj_id=paymentMethodId,
            id_field=paymentMethodRepository.model.id
        )

    def update(
        self,
        db: Session,
        paymentMethodId: UUID,
        paymentMethod: PaymentMethodUpdate
    ):
        dbPaymentMethod = self.getById(
            db,
            paymentMethodId
        )

        if dbPaymentMethod is None:
            return None

        return paymentMethodRepository.update(
            db=db,
            db_obj=dbPaymentMethod,
            obj=paymentMethod
        )

    def delete(
        self,
        db: Session,
        paymentMethodId: UUID
    ):
        dbPaymentMethod = self.getById(
            db,
            paymentMethodId
        )

        if dbPaymentMethod is None:
            return False

        paymentMethodRepository.delete(
            db=db,
            db_obj=dbPaymentMethod
        )

        return True


paymentMethodService = PaymentMethodService()