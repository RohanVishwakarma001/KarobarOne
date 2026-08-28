from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.github.orderItemRepository import (
    orderItemRepository,
)
from app.schemas.github.orderItemSchema import (
    OrderItemCreate,
    OrderItemUpdate,
)


class OrderItemService:

    def create(
        self,
        db: Session,
        orderItem: OrderItemCreate
    ):
        return orderItemRepository.create(
            db=db,
            obj=orderItem
        )

    def getAll(
        self,
        db: Session
    ):
        return orderItemRepository.get_all(db)

    def getById(
        self,
        db: Session,
        orderItemId: UUID
    ):
        return orderItemRepository.get(
            db=db,
            obj_id=orderItemId,
            id_field=orderItemRepository.model.id
        )

    def update(
        self,
        db: Session,
        orderItemId: UUID,
        orderItem: OrderItemUpdate
    ):
        dbOrderItem = self.getById(
            db,
            orderItemId
        )

        if dbOrderItem is None:
            return None

        return orderItemRepository.update(
            db=db,
            db_obj=dbOrderItem,
            obj=orderItem
        )

    def delete(
        self,
        db: Session,
        orderItemId: UUID
    ):
        dbOrderItem = self.getById(
            db,
            orderItemId
        )

        if dbOrderItem is None:
            return False

        orderItemRepository.delete(
            db=db,
            db_obj=dbOrderItem
        )

        return True


orderItemService = OrderItemService()