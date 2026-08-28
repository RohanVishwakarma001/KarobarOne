from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.github.wishlistItemRepository import (
    wishlistItemRepository,
)
from app.schemas.github.wishlistItemSchema import WishlistItemCreate
class WishlistItemService:

    def create(
        self,
        db: Session,
        wishlistItem: WishlistItemCreate
    ):
        return wishlistItemRepository.create(
            db,
            wishlistItem
        )

    def getById(
        self,
        db: Session,
        wishlistItemId: UUID
    ):
        return wishlistItemRepository.get(
            db,
            wishlistItemId,
            wishlistItemRepository.model.id
        )

    def getAll(
        self,
        db: Session
    ):
        return wishlistItemRepository.get_all(db)

    def delete(
        self,
        db: Session,
        wishlistItemId: UUID
    ):
        dbItem = self.getById(
            db,
            wishlistItemId
        )

        if dbItem is None:
            return False

        wishlistItemRepository.delete(
            db,
            dbItem
        )

        return True


wishlistItemService = WishlistItemService()