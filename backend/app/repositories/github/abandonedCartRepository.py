from app.db.models.github.models import AbandonedCart
from app.repositories.github.base import BaseRepository


class AbandonedCartRepository(BaseRepository[AbandonedCart]):

    def __init__(self):
        super().__init__(AbandonedCart)


abandonedCartRepository = AbandonedCartRepository()