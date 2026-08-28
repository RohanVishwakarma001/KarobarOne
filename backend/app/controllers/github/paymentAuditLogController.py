from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.github.paymentAuditLogSchema import (
    PaymentAuditLogCreate,
    PaymentAuditLogUpdate,
)
from app.services.github.paymentAuditLogService import (
    paymentAuditLogService,
)


class PaymentAuditLogController:

    def create(
        self,
        db: Session,
        audit: PaymentAuditLogCreate
    ):
        return paymentAuditLogService.create(
            db,
            audit
        )

    def getAll(
        self,
        db: Session
    ):
        return paymentAuditLogService.getAll(db)

    def getById(
        self,
        db: Session,
        auditId: UUID
    ):
        audit = paymentAuditLogService.getById(
            db,
            auditId
        )

        if audit is None:
            raise HTTPException(
                status_code=404,
                detail="Payment audit log not found."
            )

        return audit

    def update(
        self,
        db: Session,
        auditId: UUID,
        audit: PaymentAuditLogUpdate
    ):
        dbAudit = paymentAuditLogService.update(
            db,
            auditId,
            audit
        )

        if dbAudit is None:
            raise HTTPException(
                status_code=404,
                detail="Payment audit log not found."
            )

        return dbAudit

    def delete(
        self,
        db: Session,
        auditId: UUID
    ):
        deleted = paymentAuditLogService.delete(
            db,
            auditId
        )

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Payment audit log not found."
            )

        return {
            "message": "Payment audit log deleted successfully."
        }


paymentAuditLogController = PaymentAuditLogController()