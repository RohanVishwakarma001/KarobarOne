from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.github.orderItemSchema import (
    OrderItemCreate,
    OrderItemUpdate,
)
from app.services.github.orderItemService import (
    orderItemService,
)


class OrderItemController:

    def create(
        self,
        db: Session,
        orderItem: OrderItemCreate
    ):
        return orderItemService.create(
            db,
            orderItem
        )

    def getAll(self, db: Session):
        return orderItemService.getAll(db)

    def getById(
        self,
        db: Session,
        orderItemId: UUID
    ):
        orderItem = orderItemService.getById(
            db,
            orderItemId
        )

        if orderItem is None:
            raise HTTPException(
                status_code=404,
                detail="Order Item not found."
            )

        return orderItem

    def update(
        self,
        db: Session,
        orderItemId: UUID,
        orderItem: OrderItemUpdate
    ):
        updated = orderItemService.update(
            db,
            orderItemId,
            orderItem
        )

        if updated is None:
            raise HTTPException(
                status_code=404,
                detail="Order Item not found."
            )

        return updated

    def delete(
        self,
        db: Session,
        orderItemId: UUID
    ):
        deleted = orderItemService.delete(
            db,
            orderItemId
        )

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Order Item not found."
            )

        return {
            "message": "Order Item deleted successfully."
        }


orderItemController = OrderItemController()