from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.github.wishlistRepository import wishlistRepository
from app.schemas.github.schemas import WishlistCreate, WishlistUpdate


class WishlistService:

    def create(
        self,
        db: Session,
        wishlist: WishlistCreate
    ):
        return wishlistRepository.create(
            db,
            wishlist
        )

    def getAll(
        self,
        db: Session
    ):
        return wishlistRepository.get_all(db)

    def getById(
        self,
        db: Session,
        wishlistId: UUID
    ):
        return wishlistRepository.get(
            db,
            wishlistId,
            wishlistRepository.model.id
        )

    def update(
        self,
        db: Session,
        wishlistId: UUID,
        wishlist: WishlistUpdate
    ):
        dbWishlist = self.getById(
            db,
            wishlistId
        )

        if dbWishlist is None:
            return None

        return wishlistRepository.update(
            db,
            dbWishlist,
            wishlist
        )

    def delete(
        self,
        db: Session,
        wishlistId: UUID
    ):
        dbWishlist = self.getById(
            db,
            wishlistId
        )

        if dbWishlist is None:
            return False

        wishlistRepository.delete(
            db,
            dbWishlist
        )

        return True


wishlistService = WishlistService()