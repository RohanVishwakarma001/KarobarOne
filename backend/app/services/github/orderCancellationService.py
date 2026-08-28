from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.github.orderCancellationRepository import (
    orderCancellationRepository,
)
from app.schemas.github.orderCancellationSchema import (
    OrderCancellationCreate,
    OrderCancellationUpdate,
)

class OrderCancellationService:

    def create(
        self,
        db: Session,
        orderCancellation: OrderCancellationCreate,
    ):
        existing = orderCancellationRepository.get(
            db,
            orderCancellation.order_id,
            orderCancellationRepository.model.order_id,
        )

        if existing:
            return None

        return orderCancellationRepository.create(
            db,
            orderCancellation,
        )

    def getById(
        self,
        db: Session,
        orderCancellationId: UUID,
    ):
        return orderCancellationRepository.get(
            db,
            orderCancellationId,
            orderCancellationRepository.model.id,
        )

    def getByOrderId(
        self,
        db: Session,
        orderId: UUID,
    ):
        return orderCancellationRepository.get(
            db,
            orderId,
            orderCancellationRepository.model.order_id,
        )

    def update(
        self,
        db: Session,
        orderCancellationId: UUID,
        orderCancellation: OrderCancellationUpdate,
    ):
        dbCancellation = self.getById(
            db,
            orderCancellationId,
        )

        if dbCancellation is None:
            return None

        updateData = orderCancellation.model_dump(exclude_unset=True)

        if (
        updateData.get("status")
        in ("APPROVED", "REJECTED")
        and "approved_at" not in updateData
):
         updateData["approved_at"] = datetime.now()
        return orderCancellationRepository.update(
            db,
            dbCancellation,
            updateData,
        )

    def delete(
        self,
        db: Session,
        orderCancellationId: UUID,
    ):
        dbCancellation = self.getById(
            db,
            orderCancellationId,
        )

        if dbCancellation is None:
            return False

        orderCancellationRepository.delete(
            db,
            dbCancellation,
        )

        return True


orderCancellationService = OrderCancellationService()