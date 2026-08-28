from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controllers.github.orderController import (
    orderController,
)
from app.db.session import getSyncDb
from app.schemas.github.orderSchema import (
    OrderCreate,
    OrderUpdate,
    OrderResponse,
)

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


@router.post(
    "/",
    response_model=OrderResponse,
    status_code=201
)
def createOrder(
    order: OrderCreate,
    db: Session = Depends(getSyncDb)
):
    return orderController.create(
        db,
        order
    )


@router.get(
    "/",
    response_model=List[OrderResponse]
)
def getOrders(
    db: Session = Depends(getSyncDb)
):
    return orderController.getAll(db)


@router.get(
    "/{orderId}",
    response_model=OrderResponse
)
def getOrder(
    orderId: UUID,
    db: Session = Depends(getSyncDb)
):
    return orderController.getById(
        db,
        orderId
    )


@router.put(
    "/{orderId}",
    response_model=OrderResponse
)
def updateOrder(
    orderId: UUID,
    order: OrderUpdate,
    db: Session = Depends(getSyncDb)
):
    return orderController.update(
        db,
        orderId,
        order
    )


@router.delete(
    "/{orderId}"
)
def deleteOrder(
    orderId: UUID,
    db: Session = Depends(getSyncDb)
):
    return orderController.delete(
        db,
        orderId
    )