# Owner: shlokpallav@gmail.com
"""
===============================================================================
CART SERVICE
===============================================================================

Handles all business logic related to Cart.

Responsibilities:
- Create Cart
- Get Cart(s)
- Update Cart
- Delete Cart
- Prevent duplicate active carts
- Support guest carts
- Set cart expiry
- Update last activity timestamp

Business validations belong here.
Database queries belong in the repository layer.
===============================================================================
"""

from datetime import datetime, timedelta
from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.github.cartRepository import cartRepository
from app.schemas.github.cartSchema import CartCreate, CartUpdate


class CartService:

    # -------------------------------------------------------------------------
    # Create Cart
    # -------------------------------------------------------------------------
    def create(
        self,
        db: Session,
        cart: CartCreate,
    ):

        # Customer Cart
        if cart.customer_id:

            existingCart = cartRepository.getActiveCart(
                db,
                cart.customer_id,
            )

            if existingCart:
                return existingCart

        # Guest Cart
        else:

            if not cart.session_id:
                raise ValueError(
                    "Guest cart requires session_id."
                )

            existingCart = cartRepository.getGuestCart(
                db,
                cart.session_id,
            )

            if existingCart:
                return existingCart

        from app.db.models.github.cart import Cart

        data = cart.model_dump(mode="json")
        data["expires_at"] = datetime.utcnow() + timedelta(days=30)

        db_obj = Cart(**data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    # -------------------------------------------------------------------------
    # Get All Carts
    # -------------------------------------------------------------------------
    def getAll(
        self,
        db: Session,
    ):
        return cartRepository.get_all(db)

    # -------------------------------------------------------------------------
    # Get Cart By Id
    # -------------------------------------------------------------------------
    def getById(
        self,
        db: Session,
        cartId: UUID,
    ):
        return cartRepository.get(
            db=db,
            obj_id=cartId,
            id_field=cartRepository.model.id,
        )

    # -------------------------------------------------------------------------
    # Update Cart
    # -------------------------------------------------------------------------
    def update(
        self,
        db: Session,
        cartId: UUID,
        cart: CartUpdate,
    ):

        dbCart = self.getById(
            db,
            cartId,
        )

        if dbCart is None:
            return None

        dbCart.last_activity_at = datetime.utcnow()

        return cartRepository.update(
            db=db,
            db_obj=dbCart,
            obj=cart,
        )

    # -------------------------------------------------------------------------
    # Delete Cart
    # -------------------------------------------------------------------------
    def delete(
        self,
        db: Session,
        cartId: UUID,
    ):

        dbCart = self.getById(
            db,
            cartId,
        )

        if dbCart is None:
            return False

        cartRepository.delete(
            db=db,
            db_obj=dbCart,
        )

        return True


cartService = CartService()