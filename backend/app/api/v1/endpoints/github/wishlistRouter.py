#  owner = shlokpallav@gmail.com 
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controllers.github.wishlistController import (
    wishlistController,
)
from app.db.session import getSyncDb
from app.schemas.github.wishlistSchema import (
    WishlistCreate,
    WishlistUpdate,
    WishlistResponse,
)

router = APIRouter(
    prefix="/wishlists",
    tags=["Wishlists"]
)


@router.post(
    "/",
    response_model=WishlistResponse,
    status_code=201
)
def createWishlist(
    wishlist: WishlistCreate,
    db: Session = Depends(getSyncDb)
):
    return wishlistController.create(
        db,
        wishlist
    )


@router.get(
    "/",
    response_model=list[WishlistResponse]
)
def getWishlists(
    db: Session = Depends(getSyncDb)
):
    return wishlistController.getAll(
        db
    )


@router.get(
    "/{wishlistId}",
    response_model=WishlistResponse
)
def getWishlist(
    wishlistId: UUID,
    db: Session = Depends(getSyncDb)
):
    return wishlistController.getById(
        db,
        wishlistId
    )


@router.put(
    "/{wishlistId}",
    response_model=WishlistResponse
)
def updateWishlist(
    wishlistId: UUID,
    wishlist: WishlistUpdate,
    db: Session = Depends(getSyncDb)
):
    return wishlistController.update(
        db,
        wishlistId,
        wishlist
    )


@router.delete(
    "/{wishlistId}"
)
def deleteWishlist(
    wishlistId: UUID,
    db: Session = Depends(getSyncDb)
):
    return wishlistController.delete(
        db,
        wishlistId
    )