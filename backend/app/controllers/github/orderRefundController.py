from fastapi import HTTPException

from app.services.github.orderRefundService import orderRefundService


class OrderRefundController:

    def create(self, db, orderRefund):
        item = orderRefundService.create(
            db,
            orderRefund,
        )

        if item is None:
            raise HTTPException(
                status_code=404,
                detail="Order not found",
            )

        return item

    def getAll(self, db, orderId=None, refundStatus=None):
        return orderRefundService.getAll(
            db,
            orderId,
            refundStatus,
        )

    def getById(self, db, orderRefundId):
        item = orderRefundService.getById(
            db,
            orderRefundId,
        )

        if item is None:
            raise HTTPException(
                status_code=404,
                detail="Order refund not found",
            )

        return item

    def getByOrderId(self, db, orderId):
        return orderRefundService.getByOrderId(
            db,
            orderId,
        )

    def update(
        self,
        db,
        orderRefundId,
        orderRefund,
    ):
        item = orderRefundService.update(
            db,
            orderRefundId,
            orderRefund,
        )

        if item is None:
            raise HTTPException(
                status_code=404,
                detail="Order refund not found",
            )

        return item

    def delete(self, db, orderRefundId):
        deleted = orderRefundService.delete(
            db,
            orderRefundId,
        )

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Order refund not found",
            )

        return {
            "message": "Order refund deleted successfully"
        }


orderRefundController = OrderRefundController()