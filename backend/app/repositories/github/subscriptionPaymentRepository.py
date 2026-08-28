from app.db.models.github.subscriptionPayment import SubscriptionPayment
from app.repositories.github.base import BaseRepository


class SubscriptionPaymentRepository(
    BaseRepository[SubscriptionPayment]
):

    def __init__(self):

        super().__init__(SubscriptionPayment)


subscriptionPaymentRepository = SubscriptionPaymentRepository()