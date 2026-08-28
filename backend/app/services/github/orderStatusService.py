# Owner: shlokpallav@gmail.com

"""
===============================================================================
ORDER STATUS ENGINE
===============================================================================

Responsible for:

- Validating order status transitions
- Updating order status
- Updating payment status
- Updating fulfillment status

===============================================================================
"""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.github.orderStatusRepository import (
    orderStatusRepository,
)
from app.schemas.github.orderStatusSchema import (
    OrderStatusResponse,
    OrderStatusUpdateRequest,
)


class OrderStatusService:

    VALID_TRANSITIONS = {

        "PENDING": [
            "PAYMENT_PENDING",
            "CANCELLED",
        ],

        "PAYMENT_PENDING": [
            "PAYMENT_SUCCESS",
            "PAYMENT_FAILED",
        ],

        "PAYMENT_SUCCESS": [
            "CONFIRMED",
        ],

        "CONFIRMED": [
            "PACKED",
            "CANCELLED",
        ],

        "PACKED": [
            "SHIPPED",
        ],

        "SHIPPED": [
            "OUT_FOR_DELIVERY",
        ],

        "OUT_FOR_DELIVERY": [
            "DELIVERED",
        ],

        "DELIVERED": [
            "RETURN_REQUESTED",
        ],

        "RETURN_REQUESTED": [
            "RETURNED",
        ],

        "RETURNED": [
            "REFUNDED",
        ],
    }

    def updateStatus(
        self,
        db: Session,
        request: OrderStatusUpdateRequest,
    ) -> OrderStatusResponse:

        order = orderStatusRepository.getById(
            db=db,
            orderId=request.order_id,
        )

        if order is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found.",
            )

        currentStatus = order.order_status

        allowedStatuses = self.VALID_TRANSITIONS.get(
            currentStatus,
            [],
        )

        if request.order_status not in allowedStatuses:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"Invalid status transition "
                    f"from {currentStatus} "
                    f"to {request.order_status}."
                ),
            )

        updatedOrder = orderStatusRepository.updateStatus(
            db=db,
            order=order,
            orderStatus=request.order_status,
            paymentStatus=request.payment_status,
            fulfillmentStatus=request.fulfillment_status,
        )

        return OrderStatusResponse(
            order_id=updatedOrder.id,
            order_status=updatedOrder.order_status,
            payment_status=updatedOrder.payment_status,
            fulfillment_status=updatedOrder.fulfillment_status,
            message="Order status updated successfully.",
        )


orderStatusService = OrderStatusService()