from uuid import UUID

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from app.controllers.github.orderReturnController import (
    orderReturnController,
)
from app.db.session import getSyncDb
from app.schemas.github.schemas import (
    OrderReturnCreate,
    OrderReturnUpdate,
    OrderReturnResponse,
)

router = APIRouter(
    prefix="/order-returns",
    tags=["Order Returns"],
)


@router.post(
    "/",
    response_model=OrderReturnResponse,
    status_code=201,
)
def createOrderReturn(
    orderReturn: OrderReturnCreate,
    db: Session = Depends(getSyncDb),
):
    return orderReturnController.create(
        db,
        orderReturn,
    )


@router.get(
    "/{orderReturnId}",
    response_model=OrderReturnResponse,
)
def getOrderReturn(
    orderReturnId: UUID,
    db: Session = Depends(getSyncDb),
):
    return orderReturnController.getById(
        db,
        orderReturnId,
    )


@router.get(
    "/by-order/{orderId}",
    response_model=OrderReturnResponse,
)
def getOrderReturnByOrder(
    orderId: UUID,
    db: Session = Depends(getSyncDb),
):
    return orderReturnController.getByOrderId(
        db,
        orderId,
    )


@router.put(
    "/{orderReturnId}",
    response_model=OrderReturnResponse,
)
def updateOrderReturn(
    orderReturnId: UUID,
    orderReturn: OrderReturnUpdate,
    db: Session = Depends(getSyncDb),
):
    return orderReturnController.update(
        db,
        orderReturnId,
        orderReturn,
    )


@router.delete("/{orderReturnId}")
def deleteOrderReturn(
    orderReturnId: UUID,
    db: Session = Depends(getSyncDb),
):
    return orderReturnController.delete(
        db,
        orderReturnId,
    )