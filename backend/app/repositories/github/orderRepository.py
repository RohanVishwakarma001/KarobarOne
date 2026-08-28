from app.db.models.github.order import Order
from app.repositories.github.base import BaseRepository


class OrderRepository(
    BaseRepository[Order]
):

    def __init__(self):

        super().__init__(Order)


orderRepository = OrderRepository()