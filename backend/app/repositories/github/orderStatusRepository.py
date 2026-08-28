# Owner: shlokpallav@gmail.com

"""
===============================================================================
ORDER STATUS REPOSITORY
===============================================================================

Responsible for database operations related to updating order status.

Business logic must NOT exist here.

===============================================================================
"""

from sqlalchemy.orm import Session

from app.db.models.github.order import Order


class OrderStatusRepository:

    def getById(
        self,
        db: Session,
        orderId,
    ) -> Order | None:

        return (
            db.query(Order)
            .filter(Order.id == orderId)
            .first()
        )

    def updateStatus(
        self,
        db: Session,
        order: Order,
        orderStatus: str,
        paymentStatus: str | None = None,
        fulfillmentStatus: str | None = None,
    ) -> Order:

        order.order_status = orderStatus

        if paymentStatus is not None:
            order.payment_status = paymentStatus

        if fulfillmentStatus is not None:
            order.fulfillment_status = fulfillmentStatus

        db.commit()
        db.refresh(order)

        return order


orderStatusRepository = OrderStatusRepository()