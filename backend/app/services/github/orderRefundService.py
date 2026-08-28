from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.github.orderRefundRepository import orderRefundRepository
from app.repositories.github.orderRepository import orderRepository
from app.schemas.github.schemas import (
    OrderRefundCreate,
    OrderRefundUpdate,
    OrderRefundStatus,
    PaymentStatus,
)


class OrderRefundService:

    def updateOrderPaymentStatus(
        self,
        db: Session,
        orderId: UUID,
    ):
        order = orderRepository.get(
            db,
            orderId,
            orderRepository.model.id,
        )

        if order is None:
            return

        refunds = orderRefundRepository.get_all(
            db,
            orderRefundRepository.model.order_id,
            orderId,
        )

        totalRefund = sum(
            float(r.refund_amount)
            for r in refunds
            if r.refund_status == OrderRefundStatus.SUCCESS
        )

        if totalRefund <= 0:
            return

        if totalRefund >= float(order.total_amount):
            order.payment_status = PaymentStatus.REFUNDED
        else:
            order.payment_status = PaymentStatus.PARTIALLY_REFUNDED

        db.commit()

    def create(
        self,
        db: Session,
        orderRefund: OrderRefundCreate,
    ):
        order = orderRepository.get(
            db,
            orderRefund.order_id,
            orderRepository.model.id,
        )

        if order is None:
            return None

        return orderRefundRepository.create(
            db,
            orderRefund,
        )

    def getAll(
        self,
        db: Session,
        orderId=None,
        refundStatus=None,
    ):
        refunds = orderRefundRepository.get_all(db)

        if orderId is not None:
            refunds = [
                r for r in refunds
                if r.order_id == orderId
            ]

        if refundStatus is not None:
            refunds = [
                r for r in refunds
                if r.refund_status == refundStatus
            ]

        return refunds

    def getById(
        self,
        db: Session,
        orderRefundId: UUID,
    ):
        return orderRefundRepository.get(
            db,
            orderRefundId,
            orderRefundRepository.model.id,
        )

    def getByOrderId(
        self,
        db: Session,
        orderId: UUID,
    ):
        return orderRefundRepository.get_all(
            db,
            orderRefundRepository.model.order_id,
            orderId,
        )

    def update(
        self,
        db: Session,
        orderRefundId: UUID,
        orderRefund: OrderRefundUpdate,
    ):
        dbRefund = self.getById(
            db,
            orderRefundId,
        )

        if dbRefund is None:
            return None

        data = orderRefund.model_dump(exclude_unset=True)

        if (
            data.get("refund_status")
            == OrderRefundStatus.SUCCESS
            and "refunded_at" not in data
        ):
            data["refunded_at"] = datetime.now()

        updated = orderRefundRepository.update(
            db,
            dbRefund,
            data,
        )

        if "refund_status" in data:
            self.updateOrderPaymentStatus(
                db,
                updated.order_id,
            )

        return updated

    def delete(
        self,
        db: Session,
        orderRefundId: UUID,
    ):
        dbRefund = self.getById(
            db,
            orderRefundId,
        )

        if dbRefund is None:
            return False

        orderRefundRepository.delete(
            db,
            dbRefund,
        )

        return True


orderRefundService = OrderRefundService()