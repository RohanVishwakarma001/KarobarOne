from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.schemas.github.cartSchema import (
    CartCreate,
    CartUpdate,
)
from app.services.github.cartService import (
    cartService,
)


class CartController:

    def create(
        self,
        db: Session,
        cart: CartCreate
    ):
        return cartService.create(
            db,
            cart
        )

    def getAll(
        self,
        db: Session
    ):
        return cartService.getAll(db)

    def getById(
        self,
        db: Session,
        cartId: UUID
    ):
        cart = cartService.getById(
            db,
            cartId
        )

        if cart is None:
            raise HTTPException(
                status_code=404,
                detail="Cart item not found."
            )

        return cart

    def update(
        self,
        db: Session,
        cartId: UUID,
        cart: CartUpdate
    ):
        updatedCart = cartService.update(
            db,
            cartId,
            cart
        )

        if updatedCart is None:
            raise HTTPException(
                status_code=404,
                detail="Cart item not found."
            )

        return updatedCart

    def delete(
        self,
        db: Session,
        cartId: UUID
    ):
        deleted = cartService.delete(
            db,
            cartId
        )

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="Cart item not found."
            )

        return {
            "message": "Cart item deleted successfully."
        }


cartController = CartController()