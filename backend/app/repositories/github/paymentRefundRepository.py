from app.db.models.github.paymentRefund import PaymentRefund
from app.repositories.github.base import BaseRepository


class PaymentRefundRepository(
    BaseRepository[PaymentRefund]
):

    def __init__(self):

        super().__init__(PaymentRefund)


paymentRefundRepository = PaymentRefundRepository()