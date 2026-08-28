# Owner: shlokpallav@gmail.com

"""
===============================================================================
CHECKOUT SERVICE
===============================================================================

This service handles the complete checkout workflow.

Responsibilities:
- Validate active cart
- Fetch cart items
- Validate coupon (Phase 2)
- Calculate totals
- Prepare checkout summary

Business rules belong here.

===============================================================================
"""

from decimal import Decimal

from sqlalchemy.orm import Session

from app.repositories.github.cartRepository import cartRepository
from app.repositories.github.cartItemRepository import cartItemRepository
from app.schemas.github.checkoutSchema import (
    CheckoutRequest,
    CheckoutResponse,
)


class CheckoutService:

    # -------------------------------------------------------------------------
    # Checkout Summary
    # -------------------------------------------------------------------------
    def checkout(
        self,
        db: Session,
        request: CheckoutRequest,
    ) -> CheckoutResponse:

        # -------------------------------------------------------------
        # Get active cart
        # -------------------------------------------------------------
        cart = cartRepository.getActiveCart(
            db=db,
            customerId=request.customer_id,
        )

        if cart is None:
            from fastapi import HTTPException, status
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Active cart not found.")

        # -------------------------------------------------------------
        # Fetch cart items
        # -------------------------------------------------------------
        cartItems = cartItemRepository.getByCart(
            db=db,
            cartId=cart.id,
        )

        if not cartItems:
            from fastapi import HTTPException, status
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cart is empty.")

        # -------------------------------------------------------------
        # Calculate item count
        # -------------------------------------------------------------
        totalItems = sum(item.quantity for item in cartItems)

        # -------------------------------------------------------------
        # Phase 1
        # Use already stored values from Cart
        # -------------------------------------------------------------
        return CheckoutResponse(
            cart_id=cart.id,
            total_items=totalItems,

            subtotal=Decimal(cart.subtotal_amount),
            discount=Decimal(cart.discount_amount),
            shipping=Decimal(cart.shipping_amount),
            tax=Decimal(cart.tax_amount),
            grand_total=Decimal(cart.total_amount),

            currency=cart.currency_code,
        )


checkoutService = CheckoutService()