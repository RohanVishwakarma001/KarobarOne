from app.db.models.github.paymentAuditLog import PaymentAuditLog
from app.repositories.github.base import BaseRepository


class PaymentAuditLogRepository(
    BaseRepository[PaymentAuditLog]
):

    def __init__(self):

        super().__init__(PaymentAuditLog)


paymentAuditLogRepository = PaymentAuditLogRepository()