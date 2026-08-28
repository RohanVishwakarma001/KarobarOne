from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.github.paymentSchema import (
    PaymentCreate,
    CreateOrderRequest,
    VerifyPaymentRequest,
    RefundRequest,
    CreatePaymentOrderRequest,
)
from app.services.github.paymentService import paymentService


class PaymentController:

    def create(
        self,
        db: Session,
        payment: PaymentCreate
    ):
        return paymentService.create(
            db,
            payment
        )

    def getAll(
        self,
        db: Session
    ):
        return paymentService.getAll(db)

    def getById(
        self,
        db: Session,
        paymentId: UUID
    ):
        payment = paymentService.getById(
            db,
            paymentId
        )

        if payment is None:
            raise HTTPException(
                status_code=404,
                detail="Payment not found."
            )

        return payment

    def createOrder(
        self,
        request: CreateOrderRequest
    ):
        return paymentService.createRazorpayOrder(
            request.amount,
            request.receipt
        )

    def verify(
        self,
        request: VerifyPaymentRequest
    ):
        return paymentService.verifyPayment(
            request.model_dump()
        )

    def refund(
        self,
        request: RefundRequest
    ):
        return paymentService.refund(
            request.payment_id,
            request.amount
        )

    def createPaymentOrder(
        self,
        db: Session,
        request: CreatePaymentOrderRequest
    ):
        return paymentService.createPaymentOrder(
            db,
            request
        )


paymentController = PaymentController()