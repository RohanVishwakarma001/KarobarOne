from uuid import UUID

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from app.controllers.github.paymentController import paymentController
from app.db.session import getSyncDb
from app.schemas.github.paymentSchema import (
    PaymentCreate,
    CreateOrderRequest,
    VerifyPaymentRequest,
    RefundRequest,
    CreatePaymentOrderRequest,
)

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)


@router.post("/")
def create(
    payment: PaymentCreate,
    db: Session = Depends(getSyncDb)
):
    return paymentController.create(
        db,
        payment
    )


@router.get("/")
def getAll(
    db: Session = Depends(getSyncDb)
):
    return paymentController.getAll(db)


@router.get("/{paymentId}")
def getById(
    paymentId: UUID,
    db: Session = Depends(getSyncDb)
):
    return paymentController.getById(
        db,
        paymentId
    )


@router.post("/create-order")
def createOrder(
    request: CreateOrderRequest
):
    return paymentController.createOrder(
        request
    )


@router.post("/verify")
def verify(
    request: VerifyPaymentRequest
):
    return paymentController.verify(
        request
    )


@router.post("/refund")
def refund(
    request: RefundRequest
):
    return paymentController.refund(
        request
    )
@router.post("/create-payment-order")
def createPaymentOrder(
    request: CreatePaymentOrderRequest,
    db: Session = Depends(getSyncDb)
):

    return paymentController.createPaymentOrder(
        db,
        request
    )