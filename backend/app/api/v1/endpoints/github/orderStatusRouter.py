# Owner: shlokpallav@gmail.com

"""
===============================================================================
ORDER STATUS ROUTER
===============================================================================

Order Status Engine APIs

===============================================================================
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.controllers.github.orderStatusController import (
    orderStatusController,
)
from app.db.session import getSyncDb
from app.schemas.github.orderStatusSchema import (
    OrderStatusResponse,
    OrderStatusUpdateRequest,
)

router = APIRouter(
    prefix="/order-status",
    tags=["Order Status"],
)


@router.put(
    "",
    response_model=OrderStatusResponse,
    status_code=status.HTTP_200_OK,
)
def updateOrderStatus(
    request: OrderStatusUpdateRequest,
    db: Session = Depends(getSyncDb),
):
    return orderStatusController.updateStatus(
        db=db,
        request=request,
    )