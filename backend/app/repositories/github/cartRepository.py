# Owner: shlokpallav@gmail.com
"""
===============================================================================
CART REPOSITORY
===============================================================================

This repository handles all database operations related to the Cart module.

Responsibilities:
- CRUD operations
- Fetch active cart
- Fetch customer cart
- Fetch guest cart

Business logic should NOT be written here.
Only database queries should exist in this file.

===============================================================================
"""

from uuid import UUID

from sqlalchemy.orm import Session

from app.db.models.github.cart import Cart
from app.repositories.github.base import BaseRepository


class CartRepository(BaseRepository[Cart]):

    def __init__(self):
        super().__init__(Cart)

    # -------------------------------------------------------------------------
    # Returns active cart of a customer
    # -------------------------------------------------------------------------
    def getActiveCart(
        self,
        db: Session,
        customerId: UUID,
    ):
        return (
            db.query(Cart)
            .filter(
                Cart.customer_id == customerId,
                Cart.cart_status == "ACTIVE",
            )
            .first()
        )

    # -------------------------------------------------------------------------
    # Returns guest cart using session id
    # -------------------------------------------------------------------------
    def getGuestCart(
        self,
        db: Session,
        sessionId: str,
    ):
        return (
            db.query(Cart)
            .filter(
                Cart.session_id == sessionId,
                Cart.cart_status == "ACTIVE",
            )
            .first()
        )

    # -------------------------------------------------------------------------
    # Returns all carts of a customer
    # -------------------------------------------------------------------------
    def getCustomerCarts(
        self,
        db: Session,
        customerId: UUID,
    ):
        return (
            db.query(Cart)
            .filter(
                Cart.customer_id == customerId,
            )
            .all()
        )


cartRepository = CartRepository()