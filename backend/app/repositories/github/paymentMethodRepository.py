from app.db.models.github.paymentMethod import PaymentMethod
from app.repositories.github.base import BaseRepository


class PaymentMethodRepository(
    BaseRepository[PaymentMethod]
):

    def __init__(self):

        super().__init__(PaymentMethod)


paymentMethodRepository = PaymentMethodRepository()