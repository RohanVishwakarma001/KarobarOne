from uuid import UUID

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from app.controllers.github.subscriptionPaymentController import (
    subscriptionPaymentController,
)
from app.db.session import getSyncDb
from app.schemas.github.subscriptionPaymentSchema import (
    SubscriptionPaymentCreate,
    SubscriptionPaymentUpdate,
)

router = APIRouter(
    prefix="/subscription-payments",
    tags=["Subscription Payments"]
)


@router.post("/")
def create(
    payment: SubscriptionPaymentCreate,
    db: Session = Depends(getSyncDb)
):
    return subscriptionPaymentController.create(
        db,
        payment
    )


@router.get("/")
def getAll(
    db: Session = Depends(getSyncDb)
):
    return subscriptionPaymentController.getAll(db)


@router.get("/{paymentId}")
def getById(
    paymentId: UUID,
    db: Session = Depends(getSyncDb)
):
    return subscriptionPaymentController.getById(
        db,
        paymentId
    )


@router.put("/{paymentId}")
def update(
    paymentId: UUID,
    payment: SubscriptionPaymentUpdate,
    db: Session = Depends(getSyncDb)
):
    return subscriptionPaymentController.update(
        db,
        paymentId,
        payment
    )


@router.delete("/{paymentId}")
def delete(
    paymentId: UUID,
    db: Session = Depends(getSyncDb)
):
    return subscriptionPaymentController.delete(
        db,
        paymentId
    )