from uuid import UUID

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from app.controllers.github.paymentReconciliationItemController import (
    paymentReconciliationItemController,
)
from app.db.session import getSyncDb
from app.schemas.github.paymentReconciliationItemSchema import (
    PaymentReconciliationItemCreate,
    PaymentReconciliationItemUpdate,
)

router = APIRouter(
    prefix="/payment-reconciliation-items",
    tags=["Payment Reconciliation Items"]
)


@router.post("/")
def create(
    item: PaymentReconciliationItemCreate,
    db: Session = Depends(getSyncDb)
):
    return paymentReconciliationItemController.create(
        db,
        item
    )


@router.get("/")
def getAll(
    db: Session = Depends(getSyncDb)
):
    return paymentReconciliationItemController.getAll(db)


@router.get("/{itemId}")
def getById(
    itemId: UUID,
    db: Session = Depends(getSyncDb)
):
    return paymentReconciliationItemController.getById(
        db,
        itemId
    )


@router.put("/{itemId}")
def update(
    itemId: UUID,
    item: PaymentReconciliationItemUpdate,
    db: Session = Depends(getSyncDb)
):
    return paymentReconciliationItemController.update(
        db,
        itemId,
        item
    )


@router.delete("/{itemId}")
def delete(
    itemId: UUID,
    db: Session = Depends(getSyncDb)
):
    return paymentReconciliationItemController.delete(
        db,
        itemId
    )