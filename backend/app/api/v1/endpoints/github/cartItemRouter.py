# Owner: shlokpallav@gmail.com
"""
===============================================================================
CART ITEM ROUTER
===============================================================================

Handles all HTTP endpoints related to Cart Items.

Endpoints:
- Add Item To Cart
- Get Items By Cart
- Get Cart Item By Id
- Update Cart Item
- Delete Cart Item

The router only handles HTTP requests.
Business logic is delegated to the Controller layer.
===============================================================================
"""

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controllers.github.cartItemController import (
    cartItemController,
)
from app.db.session import getSyncDb
from app.schemas.github.schemas import (
    CartItemCreate,
    CartItemResponse,
    CartItemUpdate,
)

router = APIRouter(
    prefix="/cart-items",
    tags=["Cart Items"],
)


# ---------------------------------------------------------------------------
# Add Item To Cart
# ---------------------------------------------------------------------------
@router.post(
    "/",
    response_model=CartItemResponse,
    status_code=201,
)
def createCartItem(
    cartItem: CartItemCreate,
    db: Session = Depends(getSyncDb),
):
    return cartItemController.create(
        db,
        cartItem,
    )


# ---------------------------------------------------------------------------
# Get All Items Of A Cart
# ---------------------------------------------------------------------------
@router.get(
    "/by-cart/{cartId}",
    response_model=List[CartItemResponse],
)
def getCartItemsByCart(
    cartId: UUID,
    db: Session = Depends(getSyncDb),
):
    return cartItemController.getAllByCart(
        db,
        cartId,
    )


# ---------------------------------------------------------------------------
# Get Cart Item By Id
# ---------------------------------------------------------------------------
@router.get(
    "/{cartItemId}",
    response_model=CartItemResponse,
)
def getCartItem(
    cartItemId: UUID,
    db: Session = Depends(getSyncDb),
):
    return cartItemController.getById(
        db,
        cartItemId,
    )


# ---------------------------------------------------------------------------
# Update Cart Item
# ---------------------------------------------------------------------------
@router.put(
    "/{cartItemId}",
    response_model=CartItemResponse,
)
def updateCartItem(
    cartItemId: UUID,
    cartItem: CartItemUpdate,
    db: Session = Depends(getSyncDb),
):
    return cartItemController.update(
        db,
        cartItemId,
        cartItem,
    )


# ---------------------------------------------------------------------------
# Delete Cart Item
# ---------------------------------------------------------------------------
@router.delete(
    "/{cartItemId}",
)
def deleteCartItem(
    cartItemId: UUID,
    db: Session = Depends(getSyncDb),
):
    return cartItemController.delete(
        db,
        cartItemId,
    )