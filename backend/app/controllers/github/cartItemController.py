# Owner: shlokpallav@gmail.com
"""
===============================================================================
CART ITEM CONTROLLER
===============================================================================

Handles incoming HTTP requests for Cart Item APIs.

Responsibilities:
- Receive request from Router
- Call Service Layer
- Handle HTTP Exceptions
- Return API Response

No business logic should be written here.
===============================================================================
"""

from fastapi import HTTPException

from app.services.github.cartItemService import cartItemService


class CartItemController:

    # -------------------------------------------------------------------------
    # Create Cart Item
    # -------------------------------------------------------------------------
    def create(
        self,
        db,
        cartItem,
    ):
        try:

            item = cartItemService.create(
                db,
                cartItem,
            )

            if item is None:
                raise HTTPException(
                    status_code=404,
                    detail="Cart not found.",
                )

            return item

        except ValueError as error:
            raise HTTPException(
                status_code=400,
                detail=str(error),
            )

    # -------------------------------------------------------------------------
    # Get All Cart Items
    # -------------------------------------------------------------------------
    def getAllByCart(
        self,
        db,
        cartId,
    ):
        return cartItemService.getAllByCart(
            db,
            cartId,
        )

    # -------------------------------------------------------------------------
    # Get Cart Item By Id
    # -------------------------------------------------------------------------
    def getById(
        self,
        db,
        cartItemId,
    ):
        item = cartItemService.getById(
            db,
            cartItemId,
        )

        if item is None:
            raise HTTPException(
                status_code=404,
                detail="Cart item not found.",
            )

        return item

    # -------------------------------------------------------------------------
    # Update Cart Item
    # -------------------------------------------------------------------------
    def update(
        self,
        db,
        cartItemId,
        cartItem,
    ):
        item = cartItemService.update(
            db,
            cartItemId,
            cartItem,
        )

        if item is None:
            raise HTTPException(
                status_code=404,
                detail="Cart item not found.",
            )

        return item

    # -------------------------------------------------------------------------
    # Delete Cart Item
    # -------------------------------------------------------------------------
    def delete(
        self,
        db,
        cartItemId,
    ):
        deleted = cartItemService.delete(
            db,
            cartItemId,
        )

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Cart item not found.",
            )

        return {
            "message": "Cart item removed successfully."
        }


cartItemController = CartItemController()