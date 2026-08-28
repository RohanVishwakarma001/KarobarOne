from app.db.models.github.payment import Payment
from app.repositories.github.base import BaseRepository


class PaymentRepository(
    BaseRepository[Payment]
):

    def __init__(self):

        super().__init__(Payment)


paymentRepository = PaymentRepository()