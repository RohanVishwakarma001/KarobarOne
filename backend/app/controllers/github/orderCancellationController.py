from fastapi import HTTPException

from app.services.github.orderCancellationService import (
    orderCancellationService,
)


class OrderCancellationController:

    def create(self, db, orderCancellation):
        item = orderCancellationService.create(
            db,
            orderCancellation,
        )

        if item is None:
            raise HTTPException(
                status_code=409,
                detail="Cancellation request already exists",
            )

        return item

    def getById(self, db, orderCancellationId):
        item = orderCancellationService.getById(
            db,
            orderCancellationId,
        )

        if item is None:
            raise HTTPException(
                status_code=404,
                detail="Cancellation request not found",
            )

        return item

    def getByOrderId(self, db, orderId):
        item = orderCancellationService.getByOrderId(
            db,
            orderId,
        )

        if item is None:
            raise HTTPException(
                status_code=404,
                detail="Cancellation request not found",
            )

        return item

    def update(
        self,
        db,
        orderCancellationId,
        orderCancellation,
    ):
        item = orderCancellationService.update(
            db,
            orderCancellationId,
            orderCancellation,
        )

        if item is None:
            raise HTTPException(
                status_code=404,
                detail="Cancellation request not found",
            )

        return item

    def delete(self, db, orderCancellationId):
        deleted = orderCancellationService.delete(
            db,
            orderCancellationId,
        )

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Cancellation request not found",
            )

        return {
            "message": "Cancellation request deleted successfully"
        }


orderCancellationController = OrderCancellationController()