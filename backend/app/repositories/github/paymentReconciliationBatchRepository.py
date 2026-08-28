from app.db.models.github.paymentReconciliationBatch import (
    PaymentReconciliationBatch,
)
from app.repositories.github.base import BaseRepository


class PaymentReconciliationBatchRepository(
    BaseRepository[PaymentReconciliationBatch]
):

    def __init__(self):

        super().__init__(
            PaymentReconciliationBatch
        )


paymentReconciliationBatchRepository = (
    PaymentReconciliationBatchRepository()
)