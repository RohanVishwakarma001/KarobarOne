from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.github.paymentReconciliationItemRepository import (
    paymentReconciliationItemRepository,
)
from app.schemas.github.paymentReconciliationItemSchema import (
    PaymentReconciliationItemCreate,
    PaymentReconciliationItemUpdate,
)


class PaymentReconciliationItemService:

    def create(
        self,
        db: Session,
        item: PaymentReconciliationItemCreate
    ):
        return paymentReconciliationItemRepository.create(
            db=db,
            obj=item
        )

    def getAll(
        self,
        db: Session
    ):
        return paymentReconciliationItemRepository.get_all(db)

    def getById(
        self,
        db: Session,
        itemId: UUID
    ):
        return paymentReconciliationItemRepository.get(
            db=db,
            obj_id=itemId,
            id_field=paymentReconciliationItemRepository.model.id
        )

    def update(
        self,
        db: Session,
        itemId: UUID,
        item: PaymentReconciliationItemUpdate
    ):
        dbItem = self.getById(
            db,
            itemId
        )

        if dbItem is None:
            return None

        return paymentReconciliationItemRepository.update(
            db=db,
            db_obj=dbItem,
            obj=item
        )

    def delete(
        self,
        db: Session,
        itemId: UUID
    ):
        dbItem = self.getById(
            db,
            itemId
        )

        if dbItem is None:
            return False

        paymentReconciliationItemRepository.delete(
            db=db,
            db_obj=dbItem
        )

        return True


paymentReconciliationItemService = (
    PaymentReconciliationItemService()
)