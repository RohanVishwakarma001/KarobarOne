from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.github.orderSchema import (
    OrderCreate,
    OrderUpdate,
)
from app.services.github.orderService import (
    orderService,
)


class OrderController:

    def create(
        self,
        db: Session,
        order: OrderCreate
    ):
        return orderService.create(
            db,
            order
        )

    def getAll(
        self,
        db: Session
    ):
        return orderService.getAll(db)

    def getById(
        self,
        db: Session,
        orderId: UUID
    ):

        order = orderService.getById(
            db,
            orderId
        )

        if order is None:
            raise HTTPException(
                status_code=404,
                detail="Order not found."
            )

        return order

    def update(
        self,
        db: Session,
        orderId: UUID,
        order: OrderUpdate
    ):

        updatedOrder = orderService.update(
            db,
            orderId,
            order
        )

        if updatedOrder is None:
            raise HTTPException(
                status_code=404,
                detail="Order not found."
            )

        return updatedOrder

    def delete(
        self,
        db: Session,
        orderId: UUID
    ):

        deleted = orderService.delete(
            db,
            orderId
        )

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Order not found."
            )

        return {
            "message": "Order deleted successfully."
        }


orderController = OrderController()