from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.github.paymentAuditLogRepository import (
    paymentAuditLogRepository,
)
from app.schemas.github.paymentAuditLogSchema import (
    PaymentAuditLogCreate,
    PaymentAuditLogUpdate,
)


class PaymentAuditLogService:

    def create(
        self,
        db: Session,
        audit: PaymentAuditLogCreate
    ):
        return paymentAuditLogRepository.create(
            db=db,
            obj=audit
        )

    def getAll(
        self,
        db: Session
    ):
        return paymentAuditLogRepository.get_all(db)

    def getById(
        self,
        db: Session,
        auditId: UUID
    ):
        return paymentAuditLogRepository.get(
            db=db,
            obj_id=auditId,
            id_field=paymentAuditLogRepository.model.id
        )

    def update(
        self,
        db: Session,
        auditId: UUID,
        audit: PaymentAuditLogUpdate
    ):
        dbAudit = self.getById(
            db,
            auditId
        )

        if dbAudit is None:
            return None

        return paymentAuditLogRepository.update(
            db=db,
            db_obj=dbAudit,
            obj=audit
        )

    def delete(
        self,
        db: Session,
        auditId: UUID
    ):
        dbAudit = self.getById(
            db,
            auditId
        )

        if dbAudit is None:
            return False

        paymentAuditLogRepository.delete(
            db=db,
            db_obj=dbAudit
        )

        return True


paymentAuditLogService = PaymentAuditLogService()