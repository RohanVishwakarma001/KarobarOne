from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.github.orderReturnRepository import orderReturnRepository
from app.schemas.github.schemas import (
    OrderReturnCreate,
    OrderReturnUpdate,
    OrderReturnStatus,
)


class OrderReturnService:

    def create(self, db: Session, orderReturn: OrderReturnCreate):
        existing = orderReturnRepository.get(
            db,
            orderReturn.order_id,
            orderReturnRepository.model.order_id,
        )

        if existing:
            return None

        return orderReturnRepository.create(db, orderReturn)

    def getById(self, db: Session, orderReturnId: UUID):
        return orderReturnRepository.get(
            db,
            orderReturnId,
            orderReturnRepository.model.id,
        )

    def getByOrderId(self, db: Session, orderId: UUID):
        return orderReturnRepository.get(
            db,
            orderId,
            orderReturnRepository.model.order_id,
        )

    def update(
        self,
        db: Session,
        orderReturnId: UUID,
        orderReturn: OrderReturnUpdate,
    ):
        dbReturn = self.getById(db, orderReturnId)

        if dbReturn is None:
            return None

        data = orderReturn.model_dump(exclude_unset=True)

        if (
            data.get("return_status")
            in (
                OrderReturnStatus.APPROVED,
                OrderReturnStatus.REJECTED,
                OrderReturnStatus.RECEIVED,
                OrderReturnStatus.COMPLETED,
            )
            and "processed_at" not in data
        ):
            data["processed_at"] = datetime.now()

        return orderReturnRepository.update(
            db,
            dbReturn,
            data,
        )

    def delete(
        self,
        db: Session,
        orderReturnId: UUID,
    ):
        dbReturn = self.getById(db, orderReturnId)

        if dbReturn is None:
            return False

        orderReturnRepository.delete(db, dbReturn)

        return True


orderReturnService = OrderReturnService()