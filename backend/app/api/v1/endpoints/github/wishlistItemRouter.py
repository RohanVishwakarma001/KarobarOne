from uuid import UUID

from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controllers.github.wishlistItemController import (
    wishlistItemController,
)
from app.db.session import getSyncDb
from app.schemas.github.wishlistItemSchema import (
    WishlistItemCreate,
    WishlistItemResponse,
)

router = APIRouter(
    prefix="/wishlist-items",
    tags=["Wishlist Items"],
)


@router.post(
    "/",
    response_model=WishlistItemResponse,
    status_code=201,
)
def createWishlistItem(
    wishlistItem: WishlistItemCreate,
    db: Session = Depends(getSyncDb),
):
    return wishlistItemController.create(
        db,
        wishlistItem,
    )


@router.get(
    "/",
    response_model=list[WishlistItemResponse],
)
def getWishlistItems(
    db: Session = Depends(getSyncDb),
):
    return wishlistItemController.getAll(db)


@router.get(
    "/{wishlistItemId}",
    response_model=WishlistItemResponse,
)
def getWishlistItem(
    wishlistItemId: UUID,
    db: Session = Depends(getSyncDb),
):
    return wishlistItemController.getById(
        db,
        wishlistItemId,
    )


@router.delete(
    "/{wishlistItemId}",
)
def deleteWishlistItem(
    wishlistItemId: UUID,
    db: Session = Depends(getSyncDb),
):
    return wishlistItemController.delete(
        db,
        wishlistItemId,
    )