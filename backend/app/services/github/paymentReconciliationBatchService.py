from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.github.paymentReconciliationBatchRepository import (
    paymentReconciliationBatchRepository,
)
from app.schemas.github.paymentReconciliationBatchSchema import (
    PaymentReconciliationBatchCreate,
    PaymentReconciliationBatchUpdate,
)


class PaymentReconciliationBatchService:

    def create(
        self,
        db: Session,
        batch: PaymentReconciliationBatchCreate
    ):
        return paymentReconciliationBatchRepository.create(
            db=db,
            obj=batch
        )

    def getAll(
        self,
        db: Session
    ):
        return paymentReconciliationBatchRepository.get_all(db)

    def getById(
        self,
        db: Session,
        batchId: UUID
    ):
        return paymentReconciliationBatchRepository.get(
            db=db,
            obj_id=batchId,
            id_field=paymentReconciliationBatchRepository.model.id
        )

    def update(
        self,
        db: Session,
        batchId: UUID,
        batch: PaymentReconciliationBatchUpdate
    ):
        dbBatch = self.getById(
            db,
            batchId
        )

        if dbBatch is None:
            return None

        return paymentReconciliationBatchRepository.update(
            db=db,
            db_obj=dbBatch,
            obj=batch
        )

    def delete(
        self,
        db: Session,
        batchId: UUID
    ):
        dbBatch = self.getById(
            db,
            batchId
        )

        if dbBatch is None:
            return False

        paymentReconciliationBatchRepository.delete(
            db=db,
            db_obj=dbBatch
        )

        return True


paymentReconciliationBatchService = (
    PaymentReconciliationBatchService()
)