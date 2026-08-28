from decimal import Decimal
from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.github.paymentRepository import paymentRepository
from app.schemas.github.paymentSchema import PaymentCreate
from app.services.github.razorpayService import razorpayService


class PaymentService:

    def create(
        self,
        db: Session,
        payment: PaymentCreate
    ):
        return paymentRepository.create(
            db=db,
            obj=payment
        )

    def getAll(
        self,
        db: Session
    ):
        return paymentRepository.get_all(db)

    def getById(
        self,
        db: Session,
        paymentId: UUID
    ):
        return paymentRepository.get(
            db=db,
            obj_id=paymentId,
            id_field=paymentRepository.model.id
        )

    def createRazorpayOrder(
        self,
        amount: Decimal,
        receipt: str
    ):
        return razorpayService.createOrder(
            amount,
            receipt
        )

    def verifyPayment(
        self,
        data
    ):
        return razorpayService.verifySignature(
            data
        )

    def refund(
        self,
        paymentId,
        amount=None
    ):
        return razorpayService.refundPayment(
            paymentId,
            amount
        )

    def createPaymentOrder(
        self,
        db: Session,
        request
    ):
        payment = PaymentCreate(
            tenant_id=request.tenant_id,
            store_id=request.store_id,
            entity_type=request.entity_type,
            entity_id=request.entity_id,
            payment_method_id=request.payment_method_id,
            amount=request.amount,
            currency="INR"
        )

        dbPayment = paymentRepository.create(
            db=db,
            obj=payment
        )

        razorpayOrder = razorpayService.createOrder(
            request.amount,
            request.receipt
        )

        dbPayment.payment_reference_number = razorpayOrder["id"]

        db.commit()
        db.refresh(dbPayment)

        return {
            "payment": dbPayment,
            "razorpay_order": razorpayOrder
        }


paymentService = PaymentService()