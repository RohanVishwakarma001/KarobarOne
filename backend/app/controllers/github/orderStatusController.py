# Owner: shlokpallav@gmail.com

"""
===============================================================================
ORDER STATUS CONTROLLER
===============================================================================

Receives API requests and delegates them to the Order Status Service.

===============================================================================
"""

from sqlalchemy.orm import Session

from app.schemas.github.orderStatusSchema import (
    OrderStatusResponse,
    OrderStatusUpdateRequest,
)
from app.services.github.orderStatusService import (
    orderStatusService,
)


class OrderStatusController:

    def updateStatus(
        self,
        db: Session,
        request: OrderStatusUpdateRequest,
    ) -> OrderStatusResponse:

        return orderStatusService.updateStatus(
            db=db,
            request=request,
        )


orderStatusController = OrderStatusController()