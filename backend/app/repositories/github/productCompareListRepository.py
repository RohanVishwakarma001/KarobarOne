from app.db.models.github.models import ProductCompareList
from app.repositories.github.base import BaseRepository


class ProductCompareListRepository(BaseRepository[ProductCompareList]):

    def __init__(self):
        super().__init__(ProductCompareList)


productCompareListRepository = ProductCompareListRepository()