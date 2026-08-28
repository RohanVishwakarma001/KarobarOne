from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.github.paymentReconciliationItemSchema import (
    PaymentReconciliationItemCreate,
    PaymentReconciliationItemUpdate,
)
from app.services.github.paymentReconciliationItemService import (
    paymentReconciliationItemService,
)


class PaymentReconciliationItemController:

    def create(
        self,
        db: Session,
        item: PaymentReconciliationItemCreate
    ):
        return paymentReconciliationItemService.create(
            db,
            item
        )

    def getAll(
        self,
        db: Session
    ):
        return paymentReconciliationItemService.getAll(db)

    def getById(
        self,
        db: Session,
        itemId: UUID
    ):
        item = paymentReconciliationItemService.getById(
            db,
            itemId
        )

        if item is None:
            raise HTTPException(
                status_code=404,
                detail="Payment reconciliation item not found."
            )

        return item

    def update(
        self,
        db: Session,
        itemId: UUID,
        item: PaymentReconciliationItemUpdate
    ):
        dbItem = paymentReconciliationItemService.update(
            db,
            itemId,
            item
        )

        if dbItem is None:
            raise HTTPException(
                status_code=404,
                detail="Payment reconciliation item not found."
            )

        return dbItem

    def delete(
        self,
        db: Session,
        itemId: UUID
    ):
        deleted = paymentReconciliationItemService.delete(
            db,
            itemId
        )

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Payment reconciliation item not found."
            )

        return {
            "message": "Payment reconciliation item deleted successfully."
        }


paymentReconciliationItemController = (
    PaymentReconciliationItemController()
)