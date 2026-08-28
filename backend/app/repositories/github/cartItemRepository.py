# Owner: shlokpallav@gmail.com
"""
===============================================================================
CART ITEM REPOSITORY
===============================================================================

Handles all database operations related to Cart Items.

Responsibilities:
- CRUD operations
- Get items by cart
- Find product in cart
- Delete all cart items

Business logic should NOT be written here.
Only database queries should exist in this file.
===============================================================================
"""

from uuid import UUID

from sqlalchemy.orm import Session

from app.db.models.github.models import CartItem
from app.repositories.github.base import BaseRepository


class CartItemRepository(BaseRepository[CartItem]):

    def __init__(self):
        super().__init__(CartItem)

    # -------------------------------------------------------------------------
    # Returns all items of a cart
    # -------------------------------------------------------------------------
    def getByCart(
        self,
        db: Session,
        cartId: UUID,
    ):
        return (
            db.query(CartItem)
            .filter(
                CartItem.cart_id == cartId,
            )
            .all()
        )

    # -------------------------------------------------------------------------
    # Returns a product if it already exists in cart
    # -------------------------------------------------------------------------
    def getByCartAndProduct(
        self,
        db: Session,
        cartId: UUID,
        productId: UUID,
    ):
        return (
            db.query(CartItem)
            .filter(
                CartItem.cart_id == cartId,
                CartItem.product_id == productId,
            )
            .first()
        )

    # -------------------------------------------------------------------------
    # Deletes all items of a cart
    # -------------------------------------------------------------------------
    def deleteByCart(
        self,
        db: Session,
        cartId: UUID,
    ):
        (
            db.query(CartItem)
            .filter(
                CartItem.cart_id == cartId,
            )
            .delete()
        )

        db.commit()


cartItemRepository = CartItemRepository()