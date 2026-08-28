from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.github.paymentReconciliationBatchSchema import (
    PaymentReconciliationBatchCreate,
    PaymentReconciliationBatchUpdate,
)
from app.services.github.paymentReconciliationBatchService import (
    paymentReconciliationBatchService,
)


class PaymentReconciliationBatchController:

    def create(
        self,
        db: Session,
        batch: PaymentReconciliationBatchCreate
    ):
        return paymentReconciliationBatchService.create(
            db,
            batch
        )

    def getAll(
        self,
        db: Session
    ):
        return paymentReconciliationBatchService.getAll(db)

    def getById(
        self,
        db: Session,
        batchId: UUID
    ):
        batch = paymentReconciliationBatchService.getById(
            db,
            batchId
        )

        if batch is None:
            raise HTTPException(
                status_code=404,
                detail="Reconciliation batch not found."
            )

        return batch

    def update(
        self,
        db: Session,
        batchId: UUID,
        batch: PaymentReconciliationBatchUpdate
    ):
        dbBatch = paymentReconciliationBatchService.update(
            db,
            batchId,
            batch
        )

        if dbBatch is None:
            raise HTTPException(
                status_code=404,
                detail="Reconciliation batch not found."
            )

        return dbBatch

    def delete(
        self,
        db: Session,
        batchId: UUID
    ):
        deleted = paymentReconciliationBatchService.delete(
            db,
            batchId
        )

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Reconciliation batch not found."
            )

        return {
            "message": "Reconciliation batch deleted successfully."
        }


paymentReconciliationBatchController = (
    PaymentReconciliationBatchController()
)