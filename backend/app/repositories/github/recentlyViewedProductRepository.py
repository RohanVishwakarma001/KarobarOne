from app.db.models.github.models import RecentlyViewedProduct
from app.repositories.github.base import BaseRepository


class RecentlyViewedProductRepository(BaseRepository[RecentlyViewedProduct]):

    def __init__(self):
        super().__init__(RecentlyViewedProduct)


recentlyViewedProductRepository = RecentlyViewedProductRepository()