from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controllers.github.orderCancellationController import (
    orderCancellationController,
)
from app.db.session import getSyncDb
from app.schemas.github.orderCancellationSchema import (
    OrderCancellationCreate,
    OrderCancellationUpdate,
    OrderCancellationResponse,
)


router = APIRouter(
    prefix="/order-cancellations",
    tags=["Order Cancellations"],
)


@router.post(
    "/",
    response_model=OrderCancellationResponse,
    status_code=201,
)
def createOrderCancellation(
    orderCancellation: OrderCancellationCreate,
    db: Session = Depends(getSyncDb),
):
    return orderCancellationController.create(
        db,
        orderCancellation,
    )


@router.get(
    "/{orderCancellationId}",
    response_model=OrderCancellationResponse,
)
def getOrderCancellation(
    orderCancellationId: UUID,
    db: Session = Depends(getSyncDb),
):
    return orderCancellationController.getById(
        db,
        orderCancellationId,
    )


@router.get(
    "/by-order/{orderId}",
    response_model=OrderCancellationResponse,
)
def getOrderCancellationByOrder(
    orderId: UUID,
    db: Session = Depends(getSyncDb),
):
    return orderCancellationController.getByOrderId(
        db,
        orderId,
    )


@router.put(
    "/{orderCancellationId}",
    response_model=OrderCancellationResponse,
)
def updateOrderCancellation(
    orderCancellationId: UUID,
    orderCancellation: OrderCancellationUpdate,
    db: Session = Depends(getSyncDb),
):
    return orderCancellationController.update(
        db,
        orderCancellationId,
        orderCancellation,
    )


@router.delete("/{orderCancellationId}")
def deleteOrderCancellation(
    orderCancellationId: UUID,
    db: Session = Depends(getSyncDb),
):
    return orderCancellationController.delete(
        db,
        orderCancellationId,
    )