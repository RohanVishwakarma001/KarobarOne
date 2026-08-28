from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.github.paymentRefundRepository import (
    paymentRefundRepository,
)
from app.schemas.github.paymentRefundSchema import (
    PaymentRefundCreate,
    PaymentRefundUpdate,
)


class PaymentRefundService:

    def create(
        self,
        db: Session,
        refund: PaymentRefundCreate
    ):
        return paymentRefundRepository.create(
            db=db,
            obj=refund
        )

    def getAll(
        self,
        db: Session
    ):
        return paymentRefundRepository.get_all(db)

    def getById(
        self,
        db: Session,
        refundId: UUID
    ):
        return paymentRefundRepository.get(
            db=db,
            obj_id=refundId,
            id_field=paymentRefundRepository.model.id
        )

    def update(
        self,
        db: Session,
        refundId: UUID,
        refund: PaymentRefundUpdate
    ):
        dbRefund = self.getById(
            db,
            refundId
        )

        if dbRefund is None:
            return None

        return paymentRefundRepository.update(
            db=db,
            db_obj=dbRefund,
            obj=refund
        )

    def delete(
        self,
        db: Session,
        refundId: UUID
    ):
        dbRefund = self.getById(
            db,
            refundId
        )

        if dbRefund is None:
            return False

        paymentRefundRepository.delete(
            db=db,
            db_obj=dbRefund
        )

        return True


paymentRefundService = PaymentRefundService()