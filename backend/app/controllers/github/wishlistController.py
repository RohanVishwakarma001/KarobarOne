from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.github.schemas import (
    WishlistCreate,
    WishlistUpdate,
)
from app.services.github.wishlistService import (
    wishlistService,
)


class WishlistController:

    def create(
        self,
        db: Session,
        wishlist: WishlistCreate
    ):
        return wishlistService.create(
            db,
            wishlist
        )

    def getAll(
        self,
        db: Session
    ):
        return wishlistService.getAll(
            db
        )

    def getById(
        self,
        db: Session,
        wishlistId: UUID
    ):
        wishlist = wishlistService.getById(
            db,
            wishlistId
        )

        if wishlist is None:
            raise HTTPException(
                status_code=404,
                detail="Wishlist not found"
            )

        return wishlist

    def update(
        self,
        db: Session,
        wishlistId: UUID,
        wishlist: WishlistUpdate
    ):
        updatedWishlist = wishlistService.update(
            db,
            wishlistId,
            wishlist
        )

        if updatedWishlist is None:
            raise HTTPException(
                status_code=404,
                detail="Wishlist not found"
            )

        return updatedWishlist

    def delete(
        self,
        db: Session,
        wishlistId: UUID
    ):
        deleted = wishlistService.delete(
            db,
            wishlistId
        )

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Wishlist not found"
            )

        return {
            "message": "Wishlist deleted successfully"
        }


wishlistController = WishlistController()