from app.db.models.github.models import ProductCompareItem
from app.repositories.github.base import BaseRepository


class ProductCompareItemRepository(BaseRepository[ProductCompareItem]):

    def __init__(self):
        super().__init__(ProductCompareItem)


productCompareItemRepository = ProductCompareItemRepository()