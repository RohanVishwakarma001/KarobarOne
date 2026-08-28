from app.db.models.github.models import WishlistItem
from app.repositories.github.base import BaseRepository


class WishlistItemRepository(BaseRepository[WishlistItem]):

    def __init__(self):
        super().__init__(WishlistItem)


wishlistItemRepository = WishlistItemRepository()