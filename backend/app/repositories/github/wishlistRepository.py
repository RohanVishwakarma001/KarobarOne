from app.db.models.github.models import Wishlist
from app.repositories.github.base import BaseRepository


class WishlistRepository(
    BaseRepository[Wishlist]
):

    def __init__(self):

        super().__init__(Wishlist)


wishlistRepository = WishlistRepository()