from uuid import UUID

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from app.controllers.github.paymentAuditLogController import (
    paymentAuditLogController,
)
from app.db.session import getSyncDb
from app.schemas.github.paymentAuditLogSchema import (
    PaymentAuditLogCreate,
    PaymentAuditLogUpdate,
)

router = APIRouter(
    prefix="/payment-audit-logs",
    tags=["Payment Audit Logs"]
)


@router.post("/")
def create(
    audit: PaymentAuditLogCreate,
    db: Session = Depends(getSyncDb)
):
    return paymentAuditLogController.create(
        db,
        audit
    )


@router.get("/")
def getAll(
    db: Session = Depends(getSyncDb)
):
    return paymentAuditLogController.getAll(db)


@router.get("/{auditId}")
def getById(
    auditId: UUID,
    db: Session = Depends(getSyncDb)
):
    return paymentAuditLogController.getById(
        db,
        auditId
    )


@router.put("/{auditId}")
def update(
    auditId: UUID,
    audit: PaymentAuditLogUpdate,
    db: Session = Depends(getSyncDb)
):
    return paymentAuditLogController.update(
        db,
        auditId,
        audit
    )


@router.delete("/{auditId}")
def delete(
    auditId: UUID,
    db: Session = Depends(getSyncDb)
):
    return paymentAuditLogController.delete(
        db,
        auditId
    )