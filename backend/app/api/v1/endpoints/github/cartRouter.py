# Owner: shlokpallav@gmail.com
"""
===============================================================================
CART ROUTER
===============================================================================

This router exposes all Cart related REST APIs.

Endpoints:
- Create Cart
- Get All Carts
- Get Cart By Id
- Update Cart
- Delete Cart

The router only handles HTTP requests.
Business logic is delegated to the Cart Controller.
===============================================================================
"""

from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controllers.github.cartController import (
    cartController,
)
from app.db.session import getSyncDb
from app.schemas.github.cartSchema import (
    CartCreate,
    CartResponse,
    CartUpdate,
)

router = APIRouter(
    prefix="/cart",
    tags=["Cart"],
)


# ---------------------------------------------------------------------------
# Create Cart
# ---------------------------------------------------------------------------
@router.post(
    "/",
    response_model=CartResponse,
    status_code=201,
)
def createCart(
    cart: CartCreate,
    db: Session = Depends(getSyncDb),
):
    return cartController.create(
        db,
        cart,
    )


# ---------------------------------------------------------------------------
# Get All Carts
# ---------------------------------------------------------------------------
@router.get(
    "/",
    response_model=List[CartResponse],
)
def getCart(
    db: Session = Depends(getSyncDb),
):
    return cartController.getAll(db)


# ---------------------------------------------------------------------------
# Get Cart By Id
# ---------------------------------------------------------------------------
@router.get(
    "/{cartId}",
    response_model=CartResponse,
)
def getCartById(
    cartId: UUID,
    db: Session = Depends(getSyncDb),
):
    return cartController.getById(
        db,
        cartId,
    )


# ---------------------------------------------------------------------------
# Update Cart
# ---------------------------------------------------------------------------
@router.put(
    "/{cartId}",
    response_model=CartResponse,
)
def updateCart(
    cartId: UUID,
    cart: CartUpdate,
    db: Session = Depends(getSyncDb),
):
    return cartController.update(
        db,
        cartId,
        cart,
    )


# ---------------------------------------------------------------------------
# Delete Cart
# ---------------------------------------------------------------------------
@router.delete(
    "/{cartId}",
)
def deleteCart(
    cartId: UUID,
    db: Session = Depends(getSyncDb),
):
    return cartController.delete(
        db,
        cartId,
    )