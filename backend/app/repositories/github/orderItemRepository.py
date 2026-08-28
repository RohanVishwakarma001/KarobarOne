from app.db.models.github.orderItem import OrderItem
from app.repositories.github.base import BaseRepository


class OrderItemRepository(
    BaseRepository[OrderItem]
):

    def __init__(self):
        super().__init__(OrderItem)


orderItemRepository = OrderItemRepository()