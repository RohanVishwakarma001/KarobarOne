from typing import List
from uuid import UUID

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from app.controllers.github.orderItemController import (
    orderItemController,
)
from app.db.session import getSyncDb
from app.schemas.github.orderItemSchema import (
    OrderItemCreate,
    OrderItemUpdate,
    OrderItemResponse,
)

router = APIRouter(
    prefix="/order-items",
    tags=["Order Items"]
)


@router.post(
    "/",
    response_model=OrderItemResponse,
    status_code=201
)
def createOrderItem(
    orderItem: OrderItemCreate,
    db: Session = Depends(getSyncDb)
):
    return orderItemController.create(
        db,
        orderItem
    )


@router.get(
    "/",
    response_model=List[OrderItemResponse]
)
def getOrderItems(
    db: Session = Depends(getSyncDb)
):
    return orderItemController.getAll(db)


@router.get(
    "/{orderItemId}",
    response_model=OrderItemResponse
)
def getOrderItem(
    orderItemId: UUID,
    db: Session = Depends(getSyncDb)
):
    return orderItemController.getById(
        db,
        orderItemId
    )


@router.put(
    "/{orderItemId}",
    response_model=OrderItemResponse
)
def updateOrderItem(
    orderItemId: UUID,
    orderItem: OrderItemUpdate,
    db: Session = Depends(getSyncDb)
):
    return orderItemController.update(
        db,
        orderItemId,
        orderItem
    )


@router.delete(
    "/{orderItemId}"
)
def deleteOrderItem(
    orderItemId: UUID,
    db: Session = Depends(getSyncDb)
):
    return orderItemController.delete(
        db,
        orderItemId
    )