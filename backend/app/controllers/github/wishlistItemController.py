from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.github.wishlistItemSchema import WishlistItemCreate 
from app.services.github.wishlistItemService import (
    wishlistItemService,
)


class WishlistItemController:

    def create(
        self,
        db: Session,
        wishlistItem: WishlistItemCreate
    ):
        return wishlistItemService.create(
            db,
            wishlistItem
        )

    def getAll(
        self,
        db: Session
    ):
        return wishlistItemService.getAll(db)

    def getById(
        self,
        db: Session,
        wishlistItemId: UUID
    ):
        item = wishlistItemService.getById(
            db,
            wishlistItemId
        )

        if item is None:
            raise HTTPException(
                status_code=404,
                detail="Wishlist Item not found"
            )

        return item

    def delete(
        self,
        db: Session,
        wishlistItemId: UUID
    ):
        deleted = wishlistItemService.delete(
            db,
            wishlistItemId
        )

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Wishlist Item not found"
            )

        return {
            "message": "Wishlist Item deleted successfully"
        }


wishlistItemController = WishlistItemController()