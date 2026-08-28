from uuid import UUID

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from app.controllers.github.paymentReconciliationBatchController import (
    paymentReconciliationBatchController,
)
from app.db.session import getSyncDb
from app.schemas.github.paymentReconciliationBatchSchema import (
    PaymentReconciliationBatchCreate,
    PaymentReconciliationBatchUpdate,
)

router = APIRouter(
    prefix="/payment-reconciliation-batches",
    tags=["Payment Reconciliation Batches"]
)


@router.post("/")
def create(
    batch: PaymentReconciliationBatchCreate,
    db: Session = Depends(getSyncDb)
):
    return paymentReconciliationBatchController.create(
        db,
        batch
    )


@router.get("/")
def getAll(
    db: Session = Depends(getSyncDb)
):
    return paymentReconciliationBatchController.getAll(db)


@router.get("/{batchId}")
def getById(
    batchId: UUID,
    db: Session = Depends(getSyncDb)
):
    return paymentReconciliationBatchController.getById(
        db,
        batchId
    )


@router.put("/{batchId}")
def update(
    batchId: UUID,
    batch: PaymentReconciliationBatchUpdate,
    db: Session = Depends(getSyncDb)
):
    return paymentReconciliationBatchController.update(
        db,
        batchId,
        batch
    )


@router.delete("/{batchId}")
def delete(
    batchId: UUID,
    db: Session = Depends(getSyncDb)
):
    return paymentReconciliationBatchController.delete(
        db,
        batchId
    )