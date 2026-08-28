from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Query

from app.controllers.github.orderRefundController import (
    orderRefundController,
)
from app.db.session import getSyncDb
from app.schemas.github.schemas import (
    OrderRefundCreate,
    OrderRefundUpdate,
    OrderRefundResponse,
    OrderRefundStatus,
)

router = APIRouter(
    prefix="/order-refunds",
    tags=["Order Refunds"],
)


@router.post("/", response_model=OrderRefundResponse, status_code=201)
def createOrderRefund(
    orderRefund: OrderRefundCreate,
    db: Session = Depends(getSyncDb),
):
    return orderRefundController.create(db, orderRefund)


@router.get("/", response_model=list[OrderRefundResponse])
def getAllOrderRefunds(
    orderId: Optional[UUID] = Query(None),
    refundStatus: Optional[OrderRefundStatus] = Query(None),
    db: Session = Depends(getSyncDb),
):
    return orderRefundController.getAll(
        db,
        orderId,
        refundStatus,
    )


@router.get("/{orderRefundId}", response_model=OrderRefundResponse)
def getOrderRefund(
    orderRefundId: UUID,
    db: Session = Depends(getSyncDb),
):
    return orderRefundController.getById(
        db,
        orderRefundId,
    )


@router.get("/by-order/{orderId}", response_model=list[OrderRefundResponse])
def getRefundsByOrder(
    orderId: UUID,
    db: Session = Depends(getSyncDb),
):
    return orderRefundController.getByOrderId(
        db,
        orderId,
    )


@router.put("/{orderRefundId}", response_model=OrderRefundResponse)
def updateOrderRefund(
    orderRefundId: UUID,
    orderRefund: OrderRefundUpdate,
    db: Session = Depends(getSyncDb),
):
    return orderRefundController.update(
        db,
        orderRefundId,
        orderRefund,
    )


@router.delete("/{orderRefundId}")
def deleteOrderRefund(
    orderRefundId: UUID,
    db: Session = Depends(getSyncDb),
):
    return orderRefundController.delete(
        db,
        orderRefundId,
    )