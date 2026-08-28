from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.github.orderRepository import orderRepository
from app.schemas.github.orderSchema import (
    OrderCreate,
    OrderUpdate,
)


class OrderService:

    def create(
        self,
        db: Session,
        order: OrderCreate
    ):
        return orderRepository.create(
            db=db,
            obj=order
        )

    def getAll(
        self,
        db: Session
    ):
        return orderRepository.get_all(db)

    def getById(
        self,
        db: Session,
        orderId: UUID
    ):
        return orderRepository.get(
            db=db,
            obj_id=orderId,
            id_field=orderRepository.model.id
        )

    def update(
        self,
        db: Session,
        orderId: UUID,
        order: OrderUpdate
    ):
        dbOrder = self.getById(
            db,
            orderId
        )

        if dbOrder is None:
            return None

        return orderRepository.update(
            db=db,
            db_obj=dbOrder,
            obj=order
        )

    def delete(
        self,
        db: Session,
        orderId: UUID
    ):
        dbOrder = self.getById(
            db,
            orderId
        )

        if dbOrder is None:
            return False

        orderRepository.delete(
            db=db,
            db_obj=dbOrder
        )

        return True


orderService = OrderService()