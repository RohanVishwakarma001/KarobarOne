from uuid import UUID

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from app.controllers.github.paymentMethodController import paymentMethodController
from app.db.session import getSyncDb
from app.schemas.github.paymentMethodSchema import (
    PaymentMethodCreate,
    PaymentMethodUpdate,
)

router = APIRouter(
    prefix="/payment-methods",
    tags=["Payment Methods"],
)


@router.post("/")
def create(
    paymentMethod: PaymentMethodCreate,
    db: Session = Depends(getSyncDb)
):
    return paymentMethodController.create(
        db,
        paymentMethod
    )


@router.get("/")
def getAll(
    db: Session = Depends(getSyncDb)
):
    return paymentMethodController.getAll(db)


@router.get("/{paymentMethodId}")
def getById(
    paymentMethodId: UUID,
    db: Session = Depends(getSyncDb)
):
    return paymentMethodController.getById(
        db,
        paymentMethodId
    )


@router.put("/{paymentMethodId}")
def update(
    paymentMethodId: UUID,
    paymentMethod: PaymentMethodUpdate,
    db: Session = Depends(getSyncDb)
):
    return paymentMethodController.update(
        db,
        paymentMethodId,
        paymentMethod
    )


@router.delete("/{paymentMethodId}")
def delete(
    paymentMethodId: UUID,
    db: Session = Depends(getSyncDb)
):
    return paymentMethodController.delete(
        db,
        paymentMethodId
    )