from app.db.models.github.paymentReconciliationItem import (
    PaymentReconciliationItem,
)
from app.repositories.github.base import BaseRepository


class PaymentReconciliationItemRepository(
    BaseRepository[PaymentReconciliationItem]
):

    def __init__(self):

        super().__init__(
            PaymentReconciliationItem
        )


paymentReconciliationItemRepository = (
    PaymentReconciliationItemRepository()
)